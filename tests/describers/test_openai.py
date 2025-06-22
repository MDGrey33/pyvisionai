"""Unit tests for OpenAI image describer."""

import base64
import os
from unittest.mock import MagicMock, Mock, patch

import pytest
from openai import OpenAI, OpenAIError

from pyvisionai.describers.openai import GPT4VisionModel


@pytest.mark.unit
class TestGPT4VisionModel:
    """Test GPT-4 Vision model functionality."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock OpenAI client."""
        with patch('pyvisionai.describers.openai.OpenAI') as mock_class:
            mock_instance = MagicMock()
            mock_class.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def describer(self, mock_client):
        """Create a GPT-4 Vision model with mocked client."""
        return GPT4VisionModel(api_key='test-key')

    @pytest.fixture
    def sample_image_path(self, tmp_path):
        """Create a sample image file."""
        image_path = tmp_path / "test.jpg"
        # Minimal JPEG header
        image_path.write_bytes(
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9'
        )
        return str(image_path)

    def test_initialization_with_api_key(self):
        """Test initialization with API key."""
        model = GPT4VisionModel(api_key='test-key')
        assert model.api_key == 'test-key'
        assert model.max_tokens == 300

    def test_initialization_without_api_key(self):
        """Test initialization without explicit API key - it doesn't auto-read from env."""
        model = GPT4VisionModel()
        # Model doesn't automatically read from environment
        assert model.api_key is None

    def test_describe_image_success(
        self, describer, mock_client, sample_image_path
    ):
        """Test successful image description."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content="A beautiful sunset over the ocean"
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response

        # Test image description
        result = describer.describe_image(sample_image_path)
        assert result == "A beautiful sunset over the ocean"

        # Verify API call
        mock_client.chat.completions.create.assert_called_once()

    def test_describe_image_with_custom_prompt(
        self, mock_client, sample_image_path
    ):
        """Test description with custom prompt."""
        model = GPT4VisionModel(
            api_key='test-key', prompt="List the colors"
        )

        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Red, blue, and green"))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        result = model.describe_image(sample_image_path)
        assert result == "Red, blue, and green"

        # Verify custom prompt was used
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args[1]["messages"]
        assert any("List the colors" in str(msg) for msg in messages)

    def test_describe_image_api_error(
        self, describer, mock_client, sample_image_path
    ):
        """Test handling of API errors."""
        mock_client.chat.completions.create.side_effect = OpenAIError(
            "API error"
        )

        with pytest.raises(OpenAIError):
            describer.describe_image(sample_image_path)

    def test_describe_image_empty_response(
        self, describer, mock_client, sample_image_path
    ):
        """Test handling of empty API response."""
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content=""))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        with pytest.raises(
            ValueError, match="No description generated"
        ):
            describer.describe_image(sample_image_path)

    def test_validate_config_no_api_key(self):
        """Test configuration validation fails without API key."""
        model = GPT4VisionModel()
        model.api_key = None

        with pytest.raises(
            ValueError, match="OpenAI API key is required"
        ):
            model._validate_config()

    def test_retry_on_transient_error(
        self, describer, mock_client, sample_image_path
    ):
        """Test retry mechanism on transient errors."""
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            # Import the retryable error types
            from pyvisionai.utils.retry import TemporaryError

            # First two calls fail with retryable errors, third succeeds
            mock_response = MagicMock()
            mock_response.choices = [
                MagicMock(
                    message=MagicMock(content="Success after retry")
                )
            ]

            # Use retryable errors instead of generic exceptions
            mock_client.chat.completions.create.side_effect = [
                TemporaryError("Temporary error"),
                TemporaryError("Another temporary error"),
                mock_response,
            ]

            # With retry manager, it should eventually succeed
            result = describer.describe_image(sample_image_path)
            assert result == "Success after retry"
            assert mock_client.chat.completions.create.call_count == 3
