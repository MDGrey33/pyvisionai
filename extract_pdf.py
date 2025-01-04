"""
Extract text and images from a PDF file.
"""

import os
import config
from pdf_extractors.pdf_text_image_extractor import PDFTextImageExtractor
from pdf_extractors.pdf_page_image_extractor import PDFPageImageExtractor


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_pdf_extractor(extractor_type: str = config.DEFAULT_PDF_EXTRACTOR):
    """Factory function to create the appropriate PDF extractor."""
    if extractor_type == "text_and_images":
        return PDFTextImageExtractor()
    elif extractor_type == "page_as_image":
        return PDFPageImageExtractor()
    else:
        raise ValueError(f"Invalid PDF extractor type: {extractor_type}")


def process_pdf(pdf_path: str, output_dir: str) -> str:
    """Process a PDF file using the configured extraction method."""
    extractor_type = config.DEFAULT_PDF_EXTRACTOR
    extractor = create_pdf_extractor(extractor_type)
    return extractor.extract(pdf_path, output_dir)


def process_pdf_files(pdf_folder: str, output_folder: str):
    """Process all PDF files in the specified folder."""
    create_directory_if_not_exists(pdf_folder)
    create_directory_if_not_exists(output_folder)

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            # Create a subdirectory for the PDF file
            pdf_filename = os.path.splitext(filename)[0]
            pdf_output_dir = os.path.join(output_folder, pdf_filename)
            create_directory_if_not_exists(pdf_output_dir)
            
            print(f"\nProcessing: {filename}")
            process_pdf(pdf_path, pdf_output_dir)


if __name__ == "__main__":
    pdf_folder = "./content/source"
    output_folder = "./content/extracted"
    process_pdf_files(pdf_folder, output_folder)
