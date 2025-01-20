"""Tests for the base image description functionality."""

import os
from unittest.mock import patch

import pytest

from pyvisionai.describers.base import describe_image
from pyvisionai.utils.config import DEFAULT_IMAGE_MODEL


def test_describe_image_with_default_model():
    """Test image description with default model."""
    test_image = "test.jpg"
    expected_description = "A test image description"

    with (
        patch(
            "pyvisionai.describers.base.describe_image_ollama"
        ) as mock_ollama,
        patch(
            "pyvisionai.describers.base.describe_image_openai"
        ) as mock_openai,
    ):

        # Set up the mock based on default model
        if DEFAULT_IMAGE_MODEL == "llama":
            mock_ollama.return_value = expected_description
            mock_openai.return_value = "Should not be called"
        else:  # gpt4
            mock_openai.return_value = expected_description
            mock_ollama.return_value = "Should not be called"

        result = describe_image(test_image)
        assert result == expected_description

        # Verify correct model was called
        if DEFAULT_IMAGE_MODEL == "llama":
            mock_ollama.assert_called_once_with(test_image)
            mock_openai.assert_not_called()
        else:  # gpt4
            mock_openai.assert_called_once_with(test_image)
            mock_ollama.assert_not_called()


def test_describe_image_with_llama():
    """Test image description with llama model."""
    test_image = "test.jpg"
    expected_description = "A test image description"

    with patch(
        "pyvisionai.describers.base.describe_image_ollama"
    ) as mock_ollama:
        mock_ollama.return_value = expected_description
        result = describe_image(test_image, model="llama")
        assert result == expected_description
        mock_ollama.assert_called_once_with(test_image)


def test_describe_image_with_gpt4():
    """Test image description with GPT-4 model."""
    test_image = "test.jpg"
    expected_description = "A test image description"

    with patch(
        "pyvisionai.describers.base.describe_image_openai"
    ) as mock_openai:
        mock_openai.return_value = expected_description
        result = describe_image(test_image, model="gpt4")
        assert result == expected_description
        mock_openai.assert_called_once_with(test_image)


def test_describe_image_with_unsupported_model():
    """Test image description with an unsupported model."""
    test_image = "test.jpg"
    unsupported_model = "unsupported_model"

    with pytest.raises(
        ValueError, match=f"Unsupported model: {unsupported_model}"
    ):
        describe_image(test_image, model=unsupported_model)


def test_describe_image_with_nonexistent_file():
    """Test image description with a file that doesn't exist."""
    test_image = "nonexistent.jpg"

    # Both models should raise FileNotFoundError for missing files
    with patch(
        "pyvisionai.describers.base.describe_image_ollama"
    ) as mock_ollama:
        mock_ollama.side_effect = FileNotFoundError(
            f"File not found: {test_image}"
        )
        with pytest.raises(
            FileNotFoundError, match=f"File not found: {test_image}"
        ):
            describe_image(test_image, model="llama")

    with patch(
        "pyvisionai.describers.base.describe_image_openai"
    ) as mock_openai:
        mock_openai.side_effect = FileNotFoundError(
            f"File not found: {test_image}"
        )
        with pytest.raises(
            FileNotFoundError, match=f"File not found: {test_image}"
        ):
            describe_image(test_image, model="gpt4")
