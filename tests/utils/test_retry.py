"""Tests for the retry mechanism."""

import logging
import time
from unittest.mock import MagicMock, call, patch

import pytest
import requests

from pyvisionai.utils.retry import (
    ConnectionError,
    RateLimitError,
    RetryableError,
    RetryManager,
    RetryStrategy,
    TemporaryError,
)
from tests.utils.conftest import MockRetryableError


@pytest.fixture
def mock_logger():
    """Create a mock logger for testing."""
    return MagicMock(spec=logging.Logger)


@pytest.fixture
def retry_manager(mock_logger):
    """Create a RetryManager instance for testing."""
    return RetryManager(
        max_attempts=3,
        strategy=RetryStrategy.EXPONENTIAL,
        base_delay=0.1,  # Small delay for faster tests
        max_delay=1.0,
        logger=mock_logger,
    )


def test_successful_first_attempt(retry_manager):
    """Test operation succeeds on first attempt."""
    operation = MagicMock(return_value="success")
    result = retry_manager.execute(operation)

    assert result == "success"
    operation.assert_called_once()
    retry_manager.logger.warning.assert_not_called()


def test_successful_retry(retry_manager):
    """Test operation succeeds after initial failures."""
    operation = MagicMock(
        side_effect=[
            MockRetryableError("First failure"),
            MockRetryableError("Second failure"),
            "success",
        ]
    )

    result = retry_manager.execute(operation)

    assert result == "success"
    assert operation.call_count == 3
    assert retry_manager.logger.warning.call_count == 2


def test_max_retries_exceeded(retry_manager):
    """Test operation fails after max retries."""
    error = MockRetryableError("Persistent failure")
    operation = MagicMock(side_effect=error)

    with pytest.raises(MockRetryableError) as exc_info:
        retry_manager.execute(operation)

    assert exc_info.value == error
    assert operation.call_count == retry_manager.max_attempts
    assert retry_manager.logger.warning.call_count == 2


def test_non_retryable_error(retry_manager):
    """Test non-retryable error is raised immediately."""
    error = ValueError("Non-retryable error")
    operation = MagicMock(side_effect=error)

    with pytest.raises(ValueError) as exc_info:
        retry_manager.execute(operation)

    assert exc_info.value == error
    operation.assert_called_once()
    retry_manager.logger.warning.assert_not_called()


@pytest.mark.parametrize(
    "strategy,expected_delays",
    [
        (
            RetryStrategy.EXPONENTIAL,
            [0.1, 0.2],  # base_delay * (2 ** attempt)
        ),
        (
            RetryStrategy.LINEAR,
            [0.1, 0.2],  # base_delay * (attempt + 1)
        ),
        (RetryStrategy.CONSTANT, [0.1, 0.1]),  # always base_delay
    ],
)
def test_retry_strategies(mock_logger, strategy, expected_delays):
    """Test different retry delay strategies."""
    manager = RetryManager(
        max_attempts=3,
        strategy=strategy,
        base_delay=0.1,
        max_delay=1.0,
        logger=mock_logger,
    )

    # Mock time.sleep to track delays
    sleep_times = []

    def mock_sleep(seconds):
        sleep_times.append(seconds)

    operation = MagicMock(
        side_effect=[
            MockRetryableError("First failure"),
            MockRetryableError("Second failure"),
            "success",
        ]
    )

    with patch("time.sleep", mock_sleep):
        result = manager.execute(operation)

    assert result == "success"
    assert sleep_times == expected_delays


def test_max_delay_limit(mock_logger):
    """Test delay is capped at max_delay."""
    manager = RetryManager(
        max_attempts=3,
        strategy=RetryStrategy.EXPONENTIAL,
        base_delay=1.0,
        max_delay=2.0,
        logger=mock_logger,
    )

    # Mock time.sleep to track delays
    sleep_times = []

    def mock_sleep(seconds):
        sleep_times.append(seconds)

    operation = MagicMock(
        side_effect=[
            MockRetryableError("First failure"),
            MockRetryableError("Second failure"),
            "success",
        ]
    )

    with patch("time.sleep", mock_sleep):
        result = manager.execute(operation)

    assert result == "success"
    # Second delay should be capped at max_delay
    assert sleep_times == [1.0, 2.0]


def test_logging_messages(retry_manager):
    """Test retry logging messages."""
    operation = MagicMock(
        side_effect=[
            MockRetryableError("First failure"),
            MockRetryableError("Second failure"),
            "success",
        ]
    )

    result = retry_manager.execute(operation)

    assert result == "success"
    retry_manager.logger.warning.assert_has_calls(
        [
            call(
                "Attempt 1 failed: First failure. " "Retrying in 0.1s"
            ),
            call(
                "Attempt 2 failed: Second failure. " "Retrying in 0.2s"
            ),
        ]
    )


def test_rate_limit_retry(retry_manager):
    """Test retry on rate limit error."""
    response = MagicMock()
    response.status_code = 429
    error = requests.exceptions.HTTPError(response=response)

    operation = MagicMock(side_effect=[error, error, "success"])

    result = retry_manager.execute(operation)

    assert result == "success"
    assert operation.call_count == 3
    assert retry_manager.logger.warning.call_count == 2
    # Verify errors were converted
    retry_manager.logger.warning.assert_has_calls(
        [
            call("Attempt 1 failed: . Retrying in 0.1s"),
            call("Attempt 2 failed: . Retrying in 0.2s"),
        ]
    )


def test_server_error_retry(retry_manager):
    """Test retry on server error."""
    response = MagicMock()
    response.status_code = 503
    error = requests.exceptions.HTTPError(response=response)

    operation = MagicMock(side_effect=[error, "success"])

    result = retry_manager.execute(operation)

    assert result == "success"
    assert operation.call_count == 2
    assert retry_manager.logger.warning.call_count == 1


def test_connection_error_retry(retry_manager):
    """Test retry on connection error."""
    error = requests.exceptions.ConnectionError("Connection refused")

    operation = MagicMock(side_effect=[error, "success"])

    result = retry_manager.execute(operation)

    assert result == "success"
    assert operation.call_count == 2
    assert retry_manager.logger.warning.call_count == 1


def test_timeout_error_retry(retry_manager):
    """Test retry on timeout error."""
    error = requests.exceptions.Timeout("Request timed out")

    operation = MagicMock(side_effect=[error, "success"])

    result = retry_manager.execute(operation)

    assert result == "success"
    assert operation.call_count == 2
    assert retry_manager.logger.warning.call_count == 1


def test_non_retryable_http_error(retry_manager):
    """Test non-retryable HTTP error (4xx except 429)."""
    response = MagicMock()
    response.status_code = 404
    error = requests.exceptions.HTTPError(response=response)

    operation = MagicMock(side_effect=error)

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        retry_manager.execute(operation)

    assert exc_info.value == error
    operation.assert_called_once()
    retry_manager.logger.warning.assert_not_called()
