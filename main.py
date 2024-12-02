"""
Extract text and images from a variety of file types and replace the images with their descriptions based on MM-LLM Vision.
"""

import os
import sys
from extract_pdf import process_pdf_files
from extract_docx import process_docx_files
from extract_pptx import process_pptx_files

# Define constants for supported file types and default folders
SUPPORTED_FILE_TYPES = ["pdf", "docx", "pptx"]
DEFAULT_SOURCE_FOLDER = "./content/source"
DEFAULT_OUTPUT_FOLDER = "./content/extracted"


def process_files(file_type, source_folder, output_folder):
    """Process files of the specified type from the source folder and save the results in the output folder."""
    if file_type not in SUPPORTED_FILE_TYPES:
        raise ValueError(f"Unsupported file type: {file_type}")

    # Use a dictionary to map file types to their respective processing functions
    processing_functions = {
        "pdf": process_pdf_files,
        "docx": process_docx_files,
        "pptx": process_pptx_files,
    }

    # Call the appropriate processing function based on the file type
    processing_functions[file_type](source_folder, output_folder)


def get_user_input():
    """Get user input for source folder, output folder, and file type."""
    
    while True:
        file_type = input(
            f"Enter file type to process ({'/'.join(SUPPORTED_FILE_TYPES)}): "
        ).lower()
        if file_type in SUPPORTED_FILE_TYPES:
            break
        print(
            f"Invalid file type. Please enter one of: {', '.join(SUPPORTED_FILE_TYPES)}"
        )

    source_folder = input(
        f"Enter the source folder path (default: {DEFAULT_SOURCE_FOLDER}): "
    )
    if not source_folder:
        source_folder = DEFAULT_SOURCE_FOLDER

    output_folder = input(
        f"Enter the output folder path (default: {DEFAULT_OUTPUT_FOLDER}): "
    )
    if not output_folder:
        output_folder = DEFAULT_OUTPUT_FOLDER


    return source_folder, output_folder, file_type


def main():
    source_folder, output_folder, file_type = get_user_input()
    try:
        process_files(file_type, source_folder, output_folder)
    except ValueError as e:
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
