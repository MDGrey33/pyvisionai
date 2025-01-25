"""Tests for the base image description functionality."""

import os
from unittest.mock import MagicMock, patch

import pytest

from pyvisionai.describers.base import ModelFactory, describe_image
from pyvisionai.utils.config import DEFAULT_IMAGE_MODEL


def test_describe_image_with_default_model():
    """Test image description with default model."""
    test_image = "test.jpg"
    expected_description = "A test image description"

    # Create mock model
    mock_model = MagicMock()
    mock_model.describe_image.return_value = expected_description

    # Create mock model class
    mock_model_class = MagicMock()
    mock_model_class.return_value = mock_model

    # Register mock model
    if DEFAULT_IMAGE_MODEL == "llama":
        ModelFactory.register_model("llama", mock_model_class)
    else:  # gpt4
        ModelFactory.register_model("gpt4", mock_model_class)

    # Call function
    result = describe_image(test_image)
    assert result == expected_description

    # Verify model was created and called
    mock_model_class.assert_called_once()
    mock_model.describe_image.assert_called_once_with(test_image)


def test_describe_image_with_llama():
    """Test image description with llama model."""
    test_image = "test.jpg"
    expected_description = "A test image description"

    # Create mock model
    mock_model = MagicMock()
    mock_model.describe_image.return_value = expected_description

    # Create mock model class
    mock_model_class = MagicMock()
    mock_model_class.return_value = mock_model

    # Register mock model
    ModelFactory.register_model("llama", mock_model_class)

    # Call function
    result = describe_image(test_image, model="llama")
    assert result == expected_description

    # Verify model was created and called
    mock_model_class.assert_called_once()
    mock_model.describe_image.assert_called_once_with(test_image)


def test_describe_image_with_gpt4():
    """Test image description with GPT-4 model."""
    test_image = "test.jpg"
    expected_description = "A test image description"

    # Create mock model
    mock_model = MagicMock()
    mock_model.describe_image.return_value = expected_description

    # Create mock model class
    mock_model_class = MagicMock()
    mock_model_class.return_value = mock_model

    # Register mock model
    ModelFactory.register_model("gpt4", mock_model_class)

    # Call function
    result = describe_image(test_image, model="gpt4")
    assert result == expected_description

    # Verify model was created and called
    mock_model_class.assert_called_once()
    mock_model.describe_image.assert_called_once_with(test_image)


def test_describe_image_with_unsupported_model():
    """Test image description with an unsupported model."""
    test_image = "test.jpg"
    unsupported_model = "unsupported_model"

    with pytest.raises(
        ValueError, match=f"Unsupported model type: {unsupported_model}"
    ):
        describe_image(test_image, model=unsupported_model)


def test_describe_image_with_nonexistent_file():
    """Test image description with a file that doesn't exist."""
    test_image = "nonexistent.jpg"

    # Create mock model that raises FileNotFoundError
    mock_model = MagicMock()
    mock_model.describe_image.side_effect = FileNotFoundError(
        f"File not found: {test_image}"
    )

    # Create mock model class
    mock_model_class = MagicMock()
    mock_model_class.return_value = mock_model

    # Register mock model
    ModelFactory.register_model("llama", mock_model_class)

    with pytest.raises(
        FileNotFoundError, match=f"File not found: {test_image}"
    ):
        describe_image(test_image, model="llama")
