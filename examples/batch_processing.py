#!/usr/bin/env python3
"""
Batch processing example using PyVisionAI.

This script demonstrates how to efficiently process multiple files
in parallel with progress tracking and error handling.
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple

from pyvisionai import create_extractor


class BatchProcessor:
    """Handles batch processing of documents with progress tracking."""

    def __init__(self, max_workers: int = 4):
        """
        Initialize the batch processor.

        Args:
            max_workers: Maximum number of parallel workers
        """
        self.max_workers = max_workers
        self.extractors: Dict[str, object] = {
            ".pdf": create_extractor("pdf"),
            ".docx": create_extractor("docx"),
            ".pptx": create_extractor("pptx"),
            ".html": create_extractor("html"),
        }

    def process_file(
        self, input_path: str, output_dir: str
    ) -> Tuple[str, bool, str]:
        """
        Process a single file.

        Args:
            input_path: Path to input file
            output_dir: Output directory

        Returns:
            Tuple of (filename, success status, message)
        """
        filename = os.path.basename(input_path)
        ext = os.path.splitext(filename)[1].lower()

        if ext not in self.extractors:
            return filename, False, "Unsupported file type"

        try:
            # Create file-specific output directory
            file_output_dir = os.path.join(
                output_dir, filename.replace(".", "_")
            )
            os.makedirs(file_output_dir, exist_ok=True)

            # Extract content
            output_path = self.extractors[ext].extract(
                input_path, file_output_dir
            )
            return (
                filename,
                True,
                f"Processed successfully: {output_path}",
            )

        except Exception as e:
            return filename, False, f"Error: {str(e)}"

    def process_directory(
        self,
        input_dir: str,
        output_dir: str,
        file_types: List[str] = None,
    ) -> Tuple[int, int, List[str]]:
        """
        Process all supported files in a directory.

        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            file_types: List of file extensions to process (default: all supported)

        Returns:
            Tuple of (successful count, failed count, error messages)
        """
        if file_types is None:
            file_types = list(self.extractors.keys())

        # Get list of files to process
        files_to_process = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if any(
                    file.lower().endswith(ext) for ext in file_types
                ):
                    files_to_process.append(os.path.join(root, file))

        if not files_to_process:
            return 0, 0, ["No files found to process"]

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Process files in parallel
        successful = 0
        failed = 0
        errors = []

        print(f"\nProcessing {len(files_to_process)} files...")
        start_time = time.time()

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(self.process_file, f, output_dir): f
                for f in files_to_process
            }

            # Process completed tasks
            for i, future in enumerate(as_completed(future_to_file), 1):
                filename, success, message = future.result()
                if success:
                    successful += 1
                else:
                    failed += 1
                    errors.append(f"{filename}: {message}")

                # Print progress
                print(
                    f"Progress: {i}/{len(files_to_process)} files "
                    f"({successful} successful, {failed} failed)"
                )

        # Print summary
        elapsed_time = time.time() - start_time
        print(f"\nProcessing completed in {elapsed_time:.2f} seconds")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")

        return successful, failed, errors


def main():
    """Run the batch processing example."""
    # Initialize batch processor
    processor = BatchProcessor(max_workers=4)

    # Process all supported files in example_data directory
    successful, failed, errors = processor.process_directory(
        input_dir="example_data", output_dir="output/batch_results"
    )

    # Print errors if any
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
