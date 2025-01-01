"""
Extract text and images from a variety of file types and replace the images with their descriptions based on MM-LLM Vision.
"""

import os
import argparse
from extract_pdf import process_pdf
from extract_docx import process_docx
from extract_pptx import process_pptx


def process_file(file_type, input_file, output_dir):
    if file_type == "pdf":
        process_pdf(input_file, output_dir)
    elif file_type == "docx":
        process_docx(input_file, output_dir)
    elif file_type == "pptx":
        process_pptx(input_file, output_dir)
    else:
        print(f"Unsupported file type: {file_type}")


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

    args = parser.parse_args()

    source_folder = args.source
    output_folder = args.output
    file_type = args.type or input("Enter the file type (pdf, docx, or pptx): ")

    if not os.path.isdir(source_folder):
        print(f"Source folder not found: {source_folder}")
        return

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(f".{file_type}"):
            input_file = os.path.join(source_folder, filename)
            output_dir = os.path.join(output_folder, os.path.splitext(filename)[0])
            os.makedirs(output_dir, exist_ok=True)
            process_file(file_type, input_file, output_dir)


if __name__ == "__main__":
    main()
