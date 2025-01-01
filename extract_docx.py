"""
Extract text and images from a DOCX file using different extraction methods.
"""

import os
import config
from docx_extractors.docx_extractor_base import DocxExtractor
from docx_extractors.docx_text_image_extractor import DocxTextImageExtractor
from docx_extractors.docx_page_image_extractor import DocxPageImageExtractor


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_docx_extractor(
    extractor_type: str = config.DEFAULT_DOCX_EXTRACTOR,
) -> DocxExtractor:
    """Factory function to create the appropriate DOCX extractor."""
    if extractor_type == "text_and_images":
        return DocxTextImageExtractor()
    elif extractor_type == "page_as_image":
        return DocxPageImageExtractor()
    else:
        raise ValueError(f"Invalid DOCX extractor type: {extractor_type}")


def process_docx(docx_path: str, output_dir: str) -> str:
    """Process a DOCX file using the configured extraction method."""
    extractor_type = config.DEFAULT_DOCX_EXTRACTOR
    extractor = create_docx_extractor(extractor_type)

    # Create a subdirectory for the DOCX file
    docx_filename = os.path.splitext(os.path.basename(docx_path))[0]
    docx_output_dir = os.path.join(output_dir, docx_filename)
    create_directory_if_not_exists(docx_output_dir)

    return extractor.extract(docx_path, docx_output_dir)


def process_docx_files(docx_folder: str, output_folder: str):
    """Process all DOCX files in the specified folder."""
    create_directory_if_not_exists(docx_folder)
    create_directory_if_not_exists(output_folder)

    for filename in os.listdir(docx_folder):
        if filename.lower().endswith(".docx"):
            docx_path = os.path.join(docx_folder, filename)
            print(f"\nProcessing: {filename}")
            process_docx(docx_path, output_folder)


if __name__ == "__main__":
    docx_folder = "./content/source"
    output_folder = "./content/extracted"
    process_docx_files(docx_folder, output_folder)
