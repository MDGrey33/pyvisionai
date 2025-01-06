"""Extractors package."""

from file_extractor.extractors.pdf import PDFTextImageExtractor
from file_extractor.extractors.pdf_page import PDFPageImageExtractor
from file_extractor.extractors.docx import DocxTextImageExtractor
from file_extractor.extractors.pptx import PptxTextImageExtractor

__all__ = [
    "PDFTextImageExtractor",
    "PDFPageImageExtractor",
    "DocxTextImageExtractor",
    "PptxTextImageExtractor",
]
