"""Unit tests for Claude Vision model."""

import logging
import os
from unittest.mock import MagicMock, patch

import pytest
from anthropic import APIError, AuthenticationError

from pyvisionai.describers.claude import ClaudeVisionModel
from pyvisionai.utils.retry import ConnectionError

logger = logging.getLogger(__name__)


@pytest.fixture
def claude_model():
    """Create a ClaudeVisionModel instance."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "test_key")
    return ClaudeVisionModel(api_key=api_key)


@pytest.fixture
def mock_anthropic_setup():
    """Set up common Anthropic mocking."""
    with (
        patch("builtins.open", create=True) as mock_open,
        patch(
            "pyvisionai.describers.claude.Anthropic"
        ) as mock_anthropic_class,
    ):
        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = b"mock_image_bytes"
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock Anthropic client
        mock_client = MagicMock()
        mock_messages = MagicMock()
        mock_client.messages = mock_messages
        mock_anthropic_class.return_value = mock_client

        yield {
            "mock_open": mock_open,
            "mock_client": mock_client,
            "mock_messages": mock_messages,
        }


def create_api_error(message: str) -> APIError:
    """Create a mock Anthropic APIError."""
    mock_response = MagicMock()
    mock_response.status_code = (
        429 if "rate limit" in message.lower() else 500
    )
    mock_response.text = message
    return APIError(
        message=message,
        request=MagicMock(),
        body={"error": {"message": message}},
    )


class TestClaudeVisionModel:
    """Test suite for Claude Vision model."""

    def test_init(self, claude_model):
        """Test model initialization."""
        assert claude_model.api_key == os.getenv(
            "ANTHROPIC_API_KEY", "test_key"
        )
        assert claude_model.prompt is None

    def test_validate_config_with_key(self, claude_model):
        """Test configuration validation with API key."""
        claude_model.validate_config()  # Should not raise

    def test_validate_config_without_key(self):
        """Test configuration validation without API key."""
        model = ClaudeVisionModel(api_key=None)
        with pytest.raises(
            ValueError, match="Anthropic API key is required"
        ):
            model.validate_config()

    def test_retry_rate_limit(
        self, claude_model, mock_anthropic_setup, test_image_path
    ):
        """Test retry on rate limit errors."""
        mock_messages = mock_anthropic_setup["mock_messages"]

        # Create mock response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Success response")]

        # Mock rate limit twice, then success
        mock_messages.create.side_effect = [
            create_api_error("Rate limit exceeded"),
            create_api_error("Rate limit exceeded"),
            mock_response,
        ]

        result = claude_model.describe_image(test_image_path)
        assert result == "Success response"
        assert mock_messages.create.call_count == 3

    def test_retry_server_error(
        self, claude_model, mock_anthropic_setup, test_image_path
    ):
        """Test retry on server errors."""
        mock_messages = mock_anthropic_setup["mock_messages"]

        # Create mock response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Success response")]

        # Mock server error twice, then success
        mock_messages.create.side_effect = [
            create_api_error("Internal server error"),
            create_api_error("Internal server error"),
            mock_response,
        ]

        result = claude_model.describe_image(test_image_path)
        assert result == "Success response"
        assert mock_messages.create.call_count == 3

    def test_retry_overloaded(
        self, claude_model, mock_anthropic_setup, test_image_path
    ):
        """Test retry on overloaded errors."""
        mock_messages = mock_anthropic_setup["mock_messages"]

        # Create mock response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Success response")]

        # Mock overloaded error twice, then success
        mock_messages.create.side_effect = [
            create_api_error("Error code: 529 - Overloaded"),
            create_api_error("Error code: 529 - Overloaded"),
            mock_response,
        ]

        result = claude_model.describe_image(test_image_path)
        assert result == "Success response"
        assert mock_messages.create.call_count == 3

    def test_max_retries_exceeded(
        self, claude_model, mock_anthropic_setup, test_image_path
    ):
        """Test failure after max retries."""
        mock_messages = mock_anthropic_setup["mock_messages"]

        # Mock consistent failure
        mock_messages.create.side_effect = create_api_error(
            "Rate limit exceeded"
        )

        with pytest.raises(
            ConnectionError, match="Rate limit exceeded"
        ):
            claude_model.describe_image(test_image_path)
        assert (
            mock_messages.create.call_count == 3
        )  # Initial attempt + 2 retries

    def test_empty_response(
        self, claude_model, mock_anthropic_setup, test_image_path
    ):
        """Test handling of empty response."""
        mock_messages = mock_anthropic_setup["mock_messages"]

        # Create mock response with empty content
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="")]
        mock_messages.create.return_value = mock_response

        with pytest.raises(
            ValueError, match="No description generated"
        ):
            claude_model.describe_image(test_image_path)

    @pytest.mark.integration
    def test_real_api_call(self, test_image_path):
        """Test actual API integration."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("Skipping test - No Anthropic API key provided")

        model = ClaudeVisionModel(api_key=api_key)
        description = model.describe_image(test_image_path)
        assert len(description) > 100, "Description seems too short"
        assert any(
            term in description.lower() for term in ["forest", "tree"]
        ), "Expected forest scene description not found"
