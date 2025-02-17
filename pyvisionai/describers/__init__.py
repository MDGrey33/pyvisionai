"""Image description functions."""

from typing import Optional

from .base import ModelFactory, VisionModel, describe_image
from .claude import ClaudeVisionModel
from .ollama import LlamaVisionModel, describe_image_ollama
from .openai import GPT4VisionModel, describe_image_openai

# Register models with the factory
ModelFactory.register_model("llama", LlamaVisionModel)
ModelFactory.register_model("gpt4", GPT4VisionModel)
ModelFactory.register_model("claude", ClaudeVisionModel)


def describe_image_claude(
    image_path: str,
    api_key: Optional[str] = None,
    prompt: Optional[str] = None,
) -> str:
    """Describe an image using Claude Vision.

    Args:
        image_path: Path to the image file
        api_key: Anthropic API key (optional)
        prompt: Custom prompt for image description (optional)

    Returns:
        str: Image description
    """
    model = ClaudeVisionModel(api_key=api_key, prompt=prompt)
    return model.describe_image(image_path)


__all__ = [
    "describe_image",
    "describe_image_ollama",
    "describe_image_openai",
    "describe_image_claude",
    "VisionModel",
    "ModelFactory",
    "LlamaVisionModel",
    "GPT4VisionModel",
]
