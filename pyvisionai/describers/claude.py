"""Claude Vision model for image description."""

from typing import Optional

from pyvisionai.describers.base import VisionModel


class ClaudeVisionModel(VisionModel):
    """Claude Vision model for image description.

    This is a placeholder class that will be implemented in the future.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Claude Vision model.

        Args:
            api_key: Anthropic API key (optional)
        """
        super().__init__(api_key=api_key)

    def _validate_config(self) -> None:
        """Validate the model configuration."""
        if not self.api_key:
            raise ValueError("Anthropic API key is required")

    def describe_image(
        self, image_path: str, prompt: Optional[str] = None
    ) -> str:
        """Describe an image using Claude Vision.

        Args:
            image_path: Path to the image file
            prompt: Custom prompt to use for description (optional)

        Returns:
            str: Image description

        Raises:
            NotImplementedError: Claude Vision is not implemented yet
        """
        raise NotImplementedError(
            "Claude Vision model is not implemented yet"
        )
