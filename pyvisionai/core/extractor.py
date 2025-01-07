"""Base class for all content extractors."""

from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """Base class for document content extractors."""

    @abstractmethod
    def extract(self, file_path: str, output_dir: str) -> str:
        """
        Extract content from a document file.

        Args:
            file_path: Path to the document file to extract from
            output_dir: Directory to save extracted content

        Returns:
            str: Path to the generated markdown file
        """
        pass
