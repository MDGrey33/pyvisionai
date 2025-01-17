"""Base image description functionality."""

import os
from typing import Optional

from ..utils.config import DEFAULT_IMAGE_MODEL
from .ollama import describe_image_ollama
from .openai import describe_image_openai


def describe_image(image_path: str, model: Optional[str] = None) -> str:
    """
    Describe the contents of an image using the specified model.

    Args:
        image_path: Path to the image file
        model: Optional model name to use for description (default: uses configured default)

    Returns:
        str: Description of the image
    """
    # Use configured default if no model specified
    model = model or DEFAULT_IMAGE_MODEL

    if model == "llama":
        return describe_image_ollama(image_path)
    elif model == "gpt4":
        return describe_image_openai(image_path)
    else:
        raise ValueError(f"Unsupported model: {model}")
