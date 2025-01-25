"""Tests for API retry behavior."""

from unittest.mock import MagicMock, patch

import pytest
import requests
from openai import OpenAIError

from pyvisionai.describers.ollama import LlamaVisionModel
from pyvisionai.describers.openai import GPT4VisionModel
from pyvisionai.utils.retry import ConnectionError


@pytest.fixture
def mock_image_data():
    """Mock image data for testing."""
    return b"mock_image_bytes"


@pytest.fixture
def llama_model():
    """Create a LlamaVisionModel instance."""
    return LlamaVisionModel()


@pytest.fixture
def gpt4_model():
    """Create a GPT4VisionModel instance."""
    return GPT4VisionModel(api_key="test_key")


def test_ollama_retry_connection_error(llama_model, mock_image_data):
    """Test retry on Ollama connection error."""
    with (
        patch("requests.post") as mock_post,
        patch("builtins.open", create=True) as mock_open,
    ):
        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = mock_image_data
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock connection error twice, then success
        mock_post.side_effect = [
            requests.exceptions.ConnectionError("Connection refused"),
            requests.exceptions.ConnectionError("Connection refused"),
            MagicMock(
                json=lambda: {"response": "Success response"},
                raise_for_status=lambda: None,
            ),
        ]

        result = llama_model.describe_image("test.jpg")
        assert result == "Success response"
        assert mock_post.call_count == 3


def test_ollama_retry_rate_limit(llama_model, mock_image_data):
    """Test retry on Ollama rate limit."""
    with (
        patch("requests.post") as mock_post,
        patch("builtins.open", create=True) as mock_open,
    ):
        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = mock_image_data
        mock_open.return_value.__enter__.return_value = mock_file

        # Create mock responses
        error_response = MagicMock()
        error_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError(
                response=MagicMock(status_code=429)
            )
        )
        success_response = MagicMock(
            json=lambda: {"response": "Success response"},
            raise_for_status=lambda: None,
        )

        # Mock rate limit twice, then success
        mock_post.side_effect = [
            error_response,
            error_response,
            success_response,
        ]

        result = llama_model.describe_image("test.jpg")
        assert result == "Success response"
        assert mock_post.call_count == 3


def test_gpt4_retry_rate_limit(gpt4_model, mock_image_data):
    """Test retry on OpenAI rate limit."""
    with (
        patch("builtins.open", create=True) as mock_open,
        patch(
            "pyvisionai.describers.openai.OpenAI"
        ) as mock_openai_class,
    ):
        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = mock_image_data
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock OpenAI client
        mock_client = MagicMock()
        mock_completions = MagicMock()
        mock_client.chat.completions = mock_completions
        mock_openai_class.return_value = mock_client

        # Create mock response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Success response"))
        ]

        # Mock rate limit twice, then success
        mock_completions.create.side_effect = [
            OpenAIError("Rate limit exceeded"),
            OpenAIError("Rate limit exceeded"),
            mock_response,
        ]

        result = gpt4_model.describe_image("test.jpg")
        assert result == "Success response"
        assert mock_completions.create.call_count == 3


def test_gpt4_retry_server_error(gpt4_model, mock_image_data):
    """Test retry on OpenAI server error."""
    with (
        patch("builtins.open", create=True) as mock_open,
        patch(
            "pyvisionai.describers.openai.OpenAI"
        ) as mock_openai_class,
    ):
        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = mock_image_data
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock OpenAI client
        mock_client = MagicMock()
        mock_completions = MagicMock()
        mock_client.chat.completions = mock_completions
        mock_openai_class.return_value = mock_client

        # Create mock response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Success response"))
        ]

        # Mock server error twice, then success
        mock_completions.create.side_effect = [
            OpenAIError("Internal server error"),
            OpenAIError("Internal server error"),
            mock_response,
        ]

        result = gpt4_model.describe_image("test.jpg")
        assert result == "Success response"
        assert mock_completions.create.call_count == 3


def test_max_retries_exceeded(llama_model, mock_image_data):
    """Test failure after max retries."""
    with (
        patch("requests.post") as mock_post,
        patch("builtins.open", create=True) as mock_open,
    ):
        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = mock_image_data
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock connection error consistently
        mock_post.side_effect = requests.exceptions.ConnectionError(
            "Connection refused"
        )

        with pytest.raises(ConnectionError, match="Connection refused"):
            llama_model.describe_image("test.jpg")

        assert mock_post.call_count == 3  # Initial attempt + 2 retries
