"""
Integration tests for file extraction functionality.
"""

import os
import shutil
import subprocess
from datetime import datetime


class TestFileExtraction:
    """Test suite for file extraction functionality."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.test_output = "./content/test/output"
        self.log_dir = "./content/log"

        # Record existing log files before test
        self.existing_logs = set()
        if os.path.exists(self.log_dir):
            self.existing_logs = {
                f for f in os.listdir(self.log_dir) if f.endswith(".log")
            }

        # Clean output directory
        if os.path.exists(self.test_output):
            shutil.rmtree(self.test_output)
        os.makedirs(self.test_output)

    def teardown_method(self):
        """Clean up test environment after each test."""
        # Clean output directory
        if os.path.exists(self.test_output):
            shutil.rmtree(self.test_output)

        # Clean only test-generated log files
        if os.path.exists(self.log_dir):
            current_logs = {f for f in os.listdir(self.log_dir) if f.endswith(".log")}
            test_logs = current_logs - self.existing_logs

            for log_file in test_logs:
                os.remove(os.path.join(self.log_dir, log_file))

            # Only remove log directory if it's empty and wasn't pre-existing
            if not os.listdir(self.log_dir) and not self.existing_logs:
                os.rmdir(self.log_dir)

    def run_extraction(self, file_type, extractor_type=None):
        """Run extraction for a specific file type and verify basic outputs."""
        test_file = f"test.{file_type}"
        base_name = os.path.splitext(test_file)[0]
        output_dir = self.test_output

        # Build command
        cmd = [
            "file-extract",
            "--type",
            file_type,
            "--source",
            "./content/test/source",
            "--output",
            output_dir,
        ]
        if extractor_type:
            cmd.extend(["--extractor", extractor_type])

        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Print output if there's an error
        if result.returncode != 0:
            print("\nSTDOUT:", result.stdout)
            print("\nSTDERR:", result.stderr)

        assert (
            result.returncode == 0
        ), f"{file_type.upper()} extraction should complete successfully"

        # Verify log file contents
        log_files = [f for f in os.listdir("content/log") if f.endswith(".log")]
        assert log_files, "Log file should be created"

        log_file_path = os.path.join("content/log", sorted(log_files)[-1])
        with open(log_file_path, "r") as f:
            log_content = f.read()
            # Check for the presence of the file path in the log, ignoring timestamp and log level
            assert (
                f"./content/test/source/{test_file}" in log_content
            ), f"Log should mention processing {test_file}"

        # Verify output files
        assert os.path.exists(
            output_dir
        ), f"Output directory should exist at {output_dir}"
        md_file = os.path.join(output_dir, f"{base_name}.md")
        assert os.path.exists(md_file), f"Markdown file should be created at {md_file}"

        # Verify markdown content
        with open(md_file, "r") as f:
            content = f.read()
            assert len(content) > 0, "Markdown file should not be empty"

        return output_dir, md_file

    def test_pdf_extraction(self):
        """Test PDF extraction process with page_as_image method."""
        output_dir, md_file = self.run_extraction("pdf", "page_as_image")
        # Add PDF-specific assertions here if needed

    def test_pdf_text_and_images_extraction(self):
        """Test PDF extraction with text_and_images method."""
        output_dir, md_file = self.run_extraction("pdf", "text_and_images")
        # Add PDF-specific assertions here if needed

    def test_docx_extraction(self):
        """Test DOCX extraction process with page_as_image method."""
        output_dir, md_file = self.run_extraction("docx", "page_as_image")
        # Add DOCX-specific assertions here if needed

    def test_docx_text_and_images_extraction(self):
        """Test DOCX extraction with text_and_images method."""
        output_dir, md_file = self.run_extraction("docx", "text_and_images")
        # Add DOCX-specific assertions here if needed

    def test_pptx_extraction(self):
        """Test PPTX extraction process with page_as_image method."""
        output_dir, md_file = self.run_extraction("pptx", "page_as_image")
        # Add PPTX-specific assertions here if needed

    def test_pptx_text_and_images_extraction(self):
        """Test PPTX extraction with text_and_images method."""
        output_dir, md_file = self.run_extraction("pptx", "text_and_images")
        # Add PPTX-specific assertions here if needed
