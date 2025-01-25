"""Image description using OpenAI's GPT-4 Vision model."""

import base64
from typing import Optional

from openai import OpenAI

from ..utils.config import DEFAULT_PROMPT, OPENAI_MODEL_NAME
from ..utils.logger import logger
from ..utils.retry import RetryManager, RetryStrategy
from .base import VisionModel


class GPT4VisionModel(VisionModel):
    """GPT-4 Vision model implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        prompt: Optional[str] = None,
    ):
        super().__init__(api_key=api_key, prompt=prompt)
        self.max_tokens = 300
        self.model_name = OPENAI_MODEL_NAME
        # Initialize retry manager with exponential backoff
        self.retry_manager = RetryManager(
            max_attempts=3,
            strategy=RetryStrategy.EXPONENTIAL,
            base_delay=1.0,
            max_delay=10.0,
            logger=logger,
        )

    def describe_image(self, image_path: str) -> str:
        """Describe an image using OpenAI's GPT-4 Vision model."""

        def _make_request():
            # Initialize client
            client = OpenAI(api_key=self.api_key)

            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(
                    image_file.read()
                ).decode()

            # Use default prompt if none provided
            prompt = self.prompt or DEFAULT_PROMPT

            # Prepare request
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=self.max_tokens,
            )

            # Extract description
            description = response.choices[0].message.content.strip()

            if not description:
                raise ValueError("No description generated")

            return description

        try:
            # Execute with retry
            return self.retry_manager.execute(_make_request)
        except Exception as e:
            logger.error(
                f"Error describing image with OpenAI: {str(e)}"
            )
            raise

    def _validate_config(self) -> None:
        """Validate OpenAI configuration."""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")


def describe_image_openai(
    image_path: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    max_tokens: int = 300,
    prompt: Optional[str] = None,
) -> str:
    """
    Describe an image using OpenAI's GPT-4 Vision model.

    Args:
        image_path: Path to the image file
        model: Name of the OpenAI model to use (default: gpt-4o-mini)
        api_key: OpenAI API key (optional if set in environment)
        max_tokens: Maximum tokens in the response
        prompt: Custom prompt for image description (optional)

    Returns:
        str: Description of the image
    """
    try:
        # Initialize client
        client = OpenAI(api_key=api_key)

        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode()

        # Use default prompt if none provided
        prompt = prompt or DEFAULT_PROMPT
        # Use default model if none provided
        model = model or OPENAI_MODEL_NAME

        # Prepare request
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=max_tokens,
        )

        # Extract description
        description = response.choices[0].message.content.strip()

        if not description:
            raise ValueError("No description generated")

        return description

    except Exception as e:
        logger.error(f"Error describing image with OpenAI: {str(e)}")
        raise
