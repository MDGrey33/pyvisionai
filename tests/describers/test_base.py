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


def test_describe_image_with_fallback():
    """Test image description falls back to alternative model when default fails."""
    test_image = "test.jpg"
    expected_description = (
        "A test image description from fallback model"
    )

    # Create mock models
    failed_model = MagicMock()
    failed_model.describe_image.side_effect = ConnectionError(
        "Failed to connect"
    )

    working_model = MagicMock()
    working_model.describe_image.return_value = expected_description

    # Create mock model classes
    failed_model_class = MagicMock()
    failed_model_class.return_value = failed_model

    working_model_class = MagicMock()
    working_model_class.return_value = working_model

    # Register mock models (gpt4 as default will fail, llama as fallback will work)
    ModelFactory.register_model("gpt4", failed_model_class)
    ModelFactory.register_model("llama", working_model_class)

    # Call function without specifying model (should use default then fallback)
    result = describe_image(test_image)
    assert result == expected_description

    # Verify both models were tried
    failed_model_class.assert_called_once()
    failed_model.describe_image.assert_called_once_with(test_image)
    working_model_class.assert_called_once()
    working_model.describe_image.assert_called_once_with(test_image)


def test_describe_image_no_fallback_when_model_specified():
    """Test image description doesn't fall back when specific model fails."""
    test_image = "test.jpg"

    # Create mock model that fails
    failed_model = MagicMock()
    failed_model.describe_image.side_effect = ConnectionError(
        "Failed to connect"
    )

    # Create mock model class
    failed_model_class = MagicMock()
    failed_model_class.return_value = failed_model

    # Register both models
    ModelFactory.register_model("gpt4", failed_model_class)
    ModelFactory.register_model(
        "llama", MagicMock()
    )  # This should not be called

    # Call function with specific model
    with pytest.raises(
        ConnectionError,
        match="Failed to connect to gpt4 and no working alternatives found",
    ):
        describe_image(test_image, model="gpt4")

    # Verify only the specified model was tried
    failed_model_class.assert_called_once()
    failed_model.describe_image.assert_called_once_with(test_image)


def test_describe_image_all_models_fail():
    """Test image description when all models fail to connect."""
    test_image = "test.jpg"

    # Create mock models that fail
    failed_model1 = MagicMock()
    failed_model1.describe_image.side_effect = ConnectionError(
        "Failed to connect"
    )

    failed_model2 = MagicMock()
    failed_model2.describe_image.side_effect = ConnectionError(
        "Failed to connect"
    )

    # Create mock model classes
    failed_model_class1 = MagicMock()
    failed_model_class1.return_value = failed_model1

    failed_model_class2 = MagicMock()
    failed_model_class2.return_value = failed_model2

    # Register both failing models
    ModelFactory.register_model("gpt4", failed_model_class1)
    ModelFactory.register_model("llama", failed_model_class2)

    # Call function without specifying model
    with pytest.raises(
        ConnectionError,
        match="Failed to connect to gpt4 and no working alternatives found",
    ):
        describe_image(test_image)

    # Verify both models were tried
    failed_model_class1.assert_called_once()
    failed_model1.describe_image.assert_called_once_with(test_image)
    failed_model_class2.assert_called_once()
    failed_model2.describe_image.assert_called_once_with(test_image)
