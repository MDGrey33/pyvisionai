"""Image description functions."""

from file_extractor.describers.ollama import describe_image_ollama
from file_extractor.describers.openai import describe_image_openai

__all__ = ["describe_image_ollama", "describe_image_openai"]
