"""Command-line interface for file extraction."""

import os
import argparse
from typing import Optional

from file_extractor.core.factory import create_extractor
from file_extractor.utils.logger import logger
from file_extractor.utils.config import (
    DEFAULT_PDF_EXTRACTOR,
    DEFAULT_IMAGE_MODEL,
    CONTENT_DIR,
    SOURCE_DIR,
    EXTRACTED_DIR,
)


def process_file(
    file_type: str,
    input_file: str,
    output_dir: str,
    extractor_type: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Process a single file using the appropriate extractor.

    Args:
        file_type: Type of file to process ('pdf', 'docx', 'pptx')
        input_file: Path to the input file
        output_dir: Directory to save extracted content
        extractor_type: Optional specific extractor type
        model: Optional model to use for image descriptions
        api_key: Optional OpenAI API key (required for GPT-4)

    Returns:
        str: Path to the output file
    """
    try:
        # Get base name of the input file
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        file_output_dir = os.path.join(output_dir, base_name)

        # Create output directory if it doesn't exist
        os.makedirs(file_output_dir, exist_ok=True)

        # Create and use appropriate extractor
        extractor = create_extractor(file_type, extractor_type, model, api_key)
        logger.info(f"Processing {file_type} file: {input_file}")
        logger.info(f"Output directory: {file_output_dir}")
        return extractor.extract(input_file, file_output_dir)

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise


def process_directory(
    file_type: str,
    input_dir: str,
    output_dir: str,
    extractor_type: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> None:
    """
    Process all files of a given type in a directory.

    Args:
        file_type: Type of files to process ('pdf', 'docx', 'pptx')
        input_dir: Directory containing input files
        output_dir: Directory to save extracted content
        extractor_type: Optional specific extractor type
        model: Optional model to use for image descriptions
        api_key: Optional OpenAI API key (required for GPT-4)
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Process each file
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(f".{file_type}"):
                input_file = os.path.join(input_dir, filename)
                process_file(file_type, input_file, output_dir, extractor_type, model, api_key)

    except Exception as e:
        logger.error(f"Error processing directory: {str(e)}")
        raise


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Extract content from various file types."
    )
    parser.add_argument(
        "-t", "--type",
        choices=["pdf", "docx", "pptx"],
        required=True,
        help="Type of file to process"
    )
    parser.add_argument(
        "-s", "--source",
        default=SOURCE_DIR,
        help="Source file or directory"
    )
    parser.add_argument(
        "-o", "--output",
        default=EXTRACTED_DIR,
        help="Output directory"
    )
    parser.add_argument(
        "-e", "--extractor",
        choices=["text_and_images", "page_as_image"],
        default=DEFAULT_PDF_EXTRACTOR,
        help="Type of extractor to use"
    )
    parser.add_argument(
        "-m", "--model",
        choices=["llama", "gpt4"],
        default=DEFAULT_IMAGE_MODEL,
        help="Model to use for image descriptions"
    )
    parser.add_argument(
        "-k", "--api-key",
        help="OpenAI API key (required for GPT-4)"
    )

    args = parser.parse_args()

    try:
        # Determine if source is a file or directory
        if os.path.isfile(args.source):
            process_file(args.type, args.source, args.output, args.extractor, args.model, args.api_key)
        elif os.path.isdir(args.source):
            process_directory(args.type, args.source, args.output, args.extractor, args.model, args.api_key)
        else:
            raise FileNotFoundError(f"Source not found: {args.source}")

    except Exception as e:
        logger.error(str(e))
        exit(1)


if __name__ == "__main__":
    main() 