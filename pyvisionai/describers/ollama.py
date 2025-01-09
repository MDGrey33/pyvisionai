"""Image description using Ollama's Llama3.2 Vision model."""

import base64
from typing import Optional

import requests

from ..utils.config import DEFAULT_PROMPT, OLLAMA_MODEL_NAME
from ..utils.logger import logger


def describe_image_ollama(
    image_path: str,
    model: Optional[str] = None,
    prompt: Optional[str] = None,
) -> str:
    """
    Describe an image using Ollama's Llama3.2 Vision model.

    Args:
        image_path: Path to the image file
        model: Name of the Ollama model to use (default: llama3.2-vision)
        prompt: Custom prompt for image description (optional)

    Returns:
        str: Description of the image
    """
    try:
        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode()

        # Use default prompt if none provided
        prompt = prompt or DEFAULT_PROMPT
        # Use default model if none provided
        model = model or OLLAMA_MODEL_NAME

        # Prepare request
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "images": [image_data],
        }

        # Make request
        response = requests.post(url, json=payload)
        response.raise_for_status()

        # Extract description
        result = response.json()
        description = result.get("response", "").strip()

        if not description:
            raise ValueError("No description generated")

        return description

    except Exception as e:
        logger.error(f"Error describing image with Ollama: {str(e)}")
        raise
