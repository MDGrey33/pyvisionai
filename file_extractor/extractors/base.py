"""Base class for all extractors."""

from abc import ABC, abstractmethod
from typing import Optional

from file_extractor.describers import describe_image_ollama, describe_image_openai
from file_extractor.utils.config import DEFAULT_IMAGE_MODEL


class BaseExtractor(ABC):
    """Base class for all extractors."""

    def __init__(self):
        """Initialize the extractor."""
        self.model = DEFAULT_IMAGE_MODEL
        self.api_key = None

    def describe_image(self, image_path: str) -> str:
        """
        Describe an image using the configured model.

        Args:
            image_path: Path to the image file

        Returns:
            str: Description of the image
        """
        if self.model == "llama":
            return describe_image_ollama(image_path)
        elif self.model == "gpt4":
            return describe_image_openai(image_path, model="gpt-4o-mini", api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    @abstractmethod
    def extract(self, input_file: str, output_dir: str) -> str:
        """
        Extract content from a file.

        Args:
            input_file: Path to the input file
            output_dir: Directory to save extracted content

        Returns:
            str: Path to the generated markdown file
        """
        pass 