"""PyVisionAI package."""

from typing import Optional

from pyvisionai.core.factory import create_extractor
from pyvisionai.describers.base import describe_image
from pyvisionai.describers.claude import ClaudeVisionModel
from pyvisionai.describers.ollama import describe_image_ollama
from pyvisionai.describers.openai import describe_image_openai


def describe_image_claude(
    image_path: str,
    api_key: Optional[str] = None,
    prompt: Optional[str] = None,
    **kwargs,
) -> str:
    """Describe an image using Claude Vision.

    Args:
        image_path: Path to the image file
        api_key: Anthropic API key (optional)
        prompt: Custom prompt for image description (optional)
        **kwargs: Additional arguments passed to the model

    Returns:
        str: Image description
    """
    model = ClaudeVisionModel(api_key=api_key, prompt=prompt)
    return model.describe_image(image_path)


__version__ = "0.1.0"
__all__ = [
    "create_extractor",
    "describe_image",
    "describe_image_ollama",
    "describe_image_openai",
    "describe_image_claude",
]
