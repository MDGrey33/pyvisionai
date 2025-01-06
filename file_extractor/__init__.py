"""File Extractor package."""

from file_extractor.core.factory import create_extractor
from file_extractor.describers.ollama import describe_image_ollama
from file_extractor.describers.openai import describe_image_openai

__version__ = "0.1.0"
__all__ = ["create_extractor", "describe_image_ollama", "describe_image_openai"]
