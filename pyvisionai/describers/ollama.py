"""Image description using Ollama's Llama3.2 Vision model."""

import base64
from typing import Optional

import requests

from ..utils.config import DEFAULT_PROMPT, OLLAMA_MODEL_NAME
from ..utils.logger import logger
from ..utils.retry import RetryManager, RetryStrategy
from .base import VisionModel


class LlamaVisionModel(VisionModel):
    """Llama Vision model implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        prompt: Optional[str] = None,
    ):
        super().__init__(api_key=api_key, prompt=prompt)
        self.model_name = OLLAMA_MODEL_NAME
        # Initialize retry manager with exponential backoff
        self.retry_manager = RetryManager(
            max_attempts=3,
            strategy=RetryStrategy.EXPONENTIAL,
            base_delay=1.0,
            max_delay=10.0,
            logger=logger,
        )

    def describe_image(self, image_path: str) -> str:
        """Describe an image using Ollama's Llama3.2 Vision model."""

        def _make_request():
            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(
                    image_file.read()
                ).decode()

            # Use default prompt if none provided
            prompt = self.prompt or DEFAULT_PROMPT

            # Prepare request
            url = "http://localhost:11434/api/generate"
            payload = {
                "model": self.model_name,
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

        try:
            # Execute with retry
            return self.retry_manager.execute(_make_request)
        except requests.exceptions.ConnectionError as e:
            error_msg = str(e)
            logger.error(
                f"Error describing image with Ollama: {error_msg}"
            )
            raise ConnectionError(error_msg)
        except Exception as e:
            logger.error(
                f"Error describing image with Ollama: {str(e)}"
            )
            raise

    def _validate_config(self) -> None:
        """Validate Ollama configuration."""
        # No API key required for Ollama
        pass


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
