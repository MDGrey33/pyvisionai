"""Command-line interface for file extraction."""

import argparse
import os
from typing import Optional

from pyvisionai.core.factory import create_extractor
from pyvisionai.utils.config import (
    CONTENT_DIR,
    DEFAULT_IMAGE_MODEL,
    DEFAULT_PDF_EXTRACTOR,
    DEFAULT_PROMPT,
    EXTRACTED_DIR,
    SOURCE_DIR,
)
from pyvisionai.utils.logger import logger


def process_file(
    file_type: str,
    input_file: str,
    output_dir: str,
    extractor_type: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    prompt: Optional[str] = None,
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
        prompt: Optional custom prompt for image description

    Returns:
        str: Path to the output file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Create and use appropriate extractor
        extractor = create_extractor(
            file_type, extractor_type, model, api_key
        )
        # Set custom prompt if provided
        if prompt:
            extractor.prompt = prompt
        return extractor.extract(input_file, output_dir)

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise


def process_directory(
    file_type: str,
    input_dir: str,
    output_dir: str,
    extractor_type: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    prompt: Optional[str] = None,
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
        prompt: Optional custom prompt for image description
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Process each file
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(f".{file_type}"):
                input_file = os.path.join(input_dir, filename)
                logger.info(f"Processing {input_file}...")
                process_file(
                    file_type,
                    input_file,
                    output_dir,
                    extractor_type,
                    model,
                    api_key,
                    prompt,
                )

    except Exception as e:
        logger.error(f"Error processing directory: {str(e)}")
        raise


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Extract content from various file types."
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["pdf", "docx", "pptx", "html"],
        required=True,
        help="Type of file to process",
    )
    parser.add_argument(
        "-s",
        "--source",
        default=SOURCE_DIR,
        help="Source file or directory",
    )
    parser.add_argument(
        "-o", "--output", default=EXTRACTED_DIR, help="Output directory"
    )
    parser.add_argument(
        "-e",
        "--extractor",
        choices=["text_and_images", "page_as_image"],
        default=DEFAULT_PDF_EXTRACTOR,
        help="Type of extractor to use",
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["llama", "gpt4"],
        default=DEFAULT_IMAGE_MODEL,
        help="Model to use for image descriptions",
    )
    parser.add_argument(
        "-k", "--api-key", help="OpenAI API key (required for GPT-4)"
    )
    parser.add_argument(
        "-p",
        "--prompt",
        help=f"Custom prompt for image description (default: {DEFAULT_PROMPT})",
    )

    args = parser.parse_args()

    try:
        # Determine if source is a file or directory
        if os.path.isfile(args.source):
            process_file(
                args.type,
                args.source,
                args.output,
                args.extractor,
                args.model,
                args.api_key,
                args.prompt,
            )
        elif os.path.isdir(args.source):
            process_directory(
                args.type,
                args.source,
                args.output,
                args.extractor,
                args.model,
                args.api_key,
                args.prompt,
            )
        else:
            raise FileNotFoundError(f"Source not found: {args.source}")

    except Exception as e:
        logger.error(str(e))
        exit(1)


if __name__ == "__main__":
    main()
