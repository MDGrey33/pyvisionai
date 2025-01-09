"""File Extractor package."""

from pyvisionai.core.factory import create_extractor
from pyvisionai.describers.ollama import describe_image_ollama
from pyvisionai.describers.openai import describe_image_openai

__version__ = "0.1.0"
__all__ = [
    "create_extractor",
    "describe_image_ollama",
    "describe_image_openai",
]
