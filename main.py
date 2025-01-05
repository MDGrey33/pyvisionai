"""
Extract text and images from a variety of file types and replace the images with their descriptions based on MM-LLM Vision.
"""

import os
import argparse
from logger import logger
from extract_pdf import process_pdf
from extract_docx import process_docx
from extract_pptx import process_pptx


def process_file(file_type, input_file, output_dir, extractor_type=None):
    logger.info(f"Processing {file_type} file: {input_file}")
    logger.info(f"Output directory: {output_dir}")
    if extractor_type:
        logger.info(f"Using extractor type: {extractor_type}")
    
    if file_type == "pdf":
        process_pdf(input_file, output_dir, extractor_type)
    elif file_type == "docx":
        process_docx(input_file, output_dir)
    elif file_type == "pptx":
        process_pptx(input_file, output_dir)
    else:
        logger.error(f"Unsupported file type: {file_type}")


def main():
    parser = argparse.ArgumentParser(description="Extract text and images from files.")
    parser.add_argument(
        "--source", "-s", default="./content/source", help="Path to the source folder"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="./content/extracted",
        help="Path to the output directory",
    )
    parser.add_argument(
        "--type",
        "-t",
        choices=["pdf", "docx", "pptx"],
        help="Type of the files to process",
    )
    parser.add_argument(
        "--extractor",
        "-e",
        choices=["text_and_images", "page_as_image"],
        help="Extraction method to use (for PDF files)",
    )

    args = parser.parse_args()

    source_folder = args.source
    output_folder = args.output
    file_type = args.type or input("Enter the file type (pdf, docx, or pptx): ")
    extractor_type = args.extractor

    if not os.path.isdir(source_folder):
        logger.error(f"Source folder not found: {source_folder}")
        return

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Created output directory: {output_folder}")

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(f".{file_type}"):
            input_file = os.path.join(source_folder, filename)
            output_dir = os.path.join(output_folder, os.path.splitext(filename)[0])
            os.makedirs(output_dir, exist_ok=True)
            process_file(file_type, input_file, output_dir, extractor_type)


if __name__ == "__main__":
    main()
