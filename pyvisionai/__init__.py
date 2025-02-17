"""PyVisionAI package."""

from typing import Optional

from pyvisionai.core.factory import create_extractor
from pyvisionai.describers.base import describe_image
from pyvisionai.describers.ollama import describe_image_ollama
from pyvisionai.describers.openai import describe_image_openai


def describe_image_claude(
    image_path: str,
    api_key: Optional[str] = None,
    prompt: Optional[str] = None,
    **kwargs,
) -> str:
    """Stub function for Claude image description."""
    raise NotImplementedError(
        "Claude image description not implemented yet"
    )


__version__ = "0.1.0"
__all__ = [
    "create_extractor",
    "describe_image",
    "describe_image_ollama",
    "describe_image_openai",
    "describe_image_claude",
]
