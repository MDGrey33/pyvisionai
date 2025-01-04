"""
Base class for PDF extractors.
"""

from abc import ABC, abstractmethod


class PDFExtractor(ABC):
    """Base class for PDF extractors."""

    @abstractmethod
    def extract(self, pdf_path: str, output_dir: str) -> str:
        """
        Extract content from a PDF file.

        Args:
            pdf_path: Path to the PDF file.
            output_dir: Directory to save the output files.

        Returns:
            str: Path to the generated markdown file.
        """
        pass 