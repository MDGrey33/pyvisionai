"""Test fixtures and mock classes for utils tests."""

import logging
from unittest.mock import MagicMock

import pytest

from pyvisionai.utils.retry import (
    RetryableError,
    RetryManager,
    RetryStrategy,
)


class MockRetryableError(RetryableError):
    """Mock error that should trigger retry."""

    pass


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
