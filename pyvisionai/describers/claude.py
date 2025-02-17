"""Claude Vision model for image description."""

import base64
from typing import Optional
from unittest.mock import MagicMock

from anthropic import Anthropic, APIError, AuthenticationError

from pyvisionai.describers.base import VisionModel
from pyvisionai.utils.config import DEFAULT_PROMPT
from pyvisionai.utils.retry import (
    ConnectionError,
    RetryManager,
    RetryStrategy,
)


def create_api_error(message: str) -> APIError:
    """Create an APIError with the required arguments."""
    return APIError(
        message=message,
        request=MagicMock(),
        body={"error": {"message": message}},
    )


class ClaudeVisionModel(VisionModel):
    """Claude Vision model for image description."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        prompt: Optional[str] = None,
    ):
        """Initialize the Claude Vision model.

        Args:
            api_key: Anthropic API key (optional)
            prompt: Custom prompt for image description (optional)
        """
        super().__init__(api_key=api_key, prompt=prompt)
        self.client = None
        self.retry_manager = RetryManager(
            max_attempts=3,  # Initial attempt + 2 retries to match tests
            strategy=RetryStrategy.EXPONENTIAL,
            base_delay=1.0,
            max_delay=10.0,
        )

    def _validate_config(self) -> None:
        """Validate the model configuration."""
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        if not self.client:
            self.client = Anthropic(api_key=self.api_key)

    def describe_image(self, image_path: str) -> str:
        """Describe an image using Claude Vision.

        Args:
            image_path: Path to the image file

        Returns:
            str: Image description

        Raises:
            ValueError: If the configuration is invalid or no description generated
            ConnectionError: If API connection fails
            RuntimeError: For other errors
        """
        self.validate_config()

        def _call_api():
            with open(image_path, "rb") as f:
                image_data = f.read()

            effective_prompt = self.prompt or DEFAULT_PROMPT
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": effective_prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64.b64encode(
                                        image_data
                                    ).decode(),
                                },
                            },
                        ],
                    }
                ],
            )

            # More defensive response validation
            if (
                not response
                or not hasattr(response, 'content')
                or not response.content
                or not isinstance(response.content, list)
                or not response.content[0]
                or not hasattr(response.content[0], 'text')
            ):
                raise ValueError("No description generated")

            text = response.content[0].text
            if not text or not text.strip():
                raise ValueError("No description generated")

            return text.strip()

        try:
            return self.retry_manager.execute(_call_api)
        except APIError as e:
            error_msg = str(e).lower()
            if "authentication" in error_msg or "401" in error_msg:
                raise ConnectionError(
                    f"Authentication failed: {str(e)}"
                )
            # Let retry manager handle rate limits and server errors
            raise
        except (ValueError, ConnectionError) as e:
            # Re-raise these errors directly
            raise
        except Exception as e:
            raise RuntimeError(
                f"Error describing image with Claude: {str(e)}"
            )
