"""
Base class for DOCX extraction methods.
"""

from abc import ABC, abstractmethod


class DocxExtractor(ABC):
    """Abstract base class for DOCX extraction methods."""

    @abstractmethod
    def extract(self, docx_path: str, output_dir: str) -> str:
        """
        Extract content from DOCX file and return path to markdown file.

        Args:
            docx_path: Path to the DOCX file to process
            output_dir: Directory to save output files

        Returns:
            str: Path to the generated markdown file
        """
        pass
