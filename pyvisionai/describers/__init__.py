"""Image description functions."""

from .base import ModelFactory, VisionModel, describe_image
from .ollama import LlamaVisionModel, describe_image_ollama
from .openai import GPT4VisionModel, describe_image_openai

# Register models with the factory
ModelFactory.register_model("llama", LlamaVisionModel)
ModelFactory.register_model("gpt4", GPT4VisionModel)

__all__ = [
    "describe_image",
    "describe_image_ollama",
    "describe_image_openai",
    "VisionModel",
    "ModelFactory",
    "LlamaVisionModel",
    "GPT4VisionModel",
]
