"""Tests for batch processing example."""

import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import pytest

from examples.batch_processing import BatchProcessor

# Test data paths
TEST_DATA_DIR = os.path.join("tests", "data", "batch")


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def setup_test_files(temp_output_dir):
    """Set up test files for batch processing."""
    os.makedirs(TEST_DATA_DIR, exist_ok=True)

    # Create sample files of different types
    files = {
        "doc1.pdf": "PDF content",
        "doc2.docx": "DOCX content",
        "doc3.pptx": "PPTX content",
        "page.html": "HTML content",
        "ignored.txt": "Text content",
    }

    for filename, content in files.items():
        filepath = os.path.join(TEST_DATA_DIR, filename)
        with open(filepath, "w") as f:
            f.write(content)

    yield

    # Cleanup
    shutil.rmtree(TEST_DATA_DIR)


def test_batch_processor_init():
    """Test BatchProcessor initialization."""
    processor = BatchProcessor(max_workers=2)
    assert processor.max_workers == 2
    assert len(processor.extractors) == 4  # pdf, docx, pptx, html
    assert all(
        ext in processor.extractors
        for ext in [".pdf", ".docx", ".pptx", ".html"]
    )


@patch("examples.batch_processing.create_extractor")
def test_process_file_success(
    mock_create_extractor, temp_output_dir, setup_test_files
):
    """Test successful file processing."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor

    # Create processor
    processor = BatchProcessor()

    # Process PDF file
    input_file = os.path.join(TEST_DATA_DIR, "doc1.pdf")
    filename, success, message = processor.process_file(
        input_file, temp_output_dir
    )

    # Verify
    assert filename == "doc1.pdf"
    assert success is True
    assert "Processed successfully" in message
    mock_extractor.extract.assert_called_once()


def test_process_file_unsupported(temp_output_dir, setup_test_files):
    """Test processing unsupported file type."""
    processor = BatchProcessor()

    # Try to process text file
    input_file = os.path.join(TEST_DATA_DIR, "ignored.txt")
    filename, success, message = processor.process_file(
        input_file, temp_output_dir
    )

    # Verify
    assert filename == "ignored.txt"
    assert success is False
    assert message == "Unsupported file type"


@patch("examples.batch_processing.create_extractor")
def test_process_file_error(
    mock_create_extractor, temp_output_dir, setup_test_files
):
    """Test handling of processing errors."""
    # Setup mock to raise exception
    mock_extractor = Mock()
    mock_extractor.extract.side_effect = Exception("Processing failed")
    mock_create_extractor.return_value = mock_extractor

    # Create processor and process file
    processor = BatchProcessor()
    input_file = os.path.join(TEST_DATA_DIR, "doc1.pdf")
    filename, success, message = processor.process_file(
        input_file, temp_output_dir
    )

    # Verify
    assert filename == "doc1.pdf"
    assert success is False
    assert "Error: Processing failed" in message


@patch("examples.batch_processing.create_extractor")
def test_process_directory(
    mock_create_extractor, temp_output_dir, setup_test_files
):
    """Test processing entire directory."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor

    # Create processor and process directory
    processor = BatchProcessor(max_workers=2)
    successful, failed, errors = processor.process_directory(
        TEST_DATA_DIR, temp_output_dir
    )

    # Verify
    assert successful == 4  # pdf, docx, pptx, html
    assert failed == 0
    assert len(errors) == 0
    assert mock_extractor.extract.call_count == 4


def test_process_directory_empty(temp_output_dir):
    """Test processing empty directory."""
    # Create empty directory
    empty_dir = os.path.join(temp_output_dir, "empty")
    os.makedirs(empty_dir)

    # Process empty directory
    processor = BatchProcessor()
    successful, failed, errors = processor.process_directory(
        empty_dir, temp_output_dir
    )

    # Verify
    assert successful == 0
    assert failed == 0
    assert len(errors) == 1
    assert errors[0] == "No files found to process"


@patch("examples.batch_processing.create_extractor")
def test_process_directory_filtered(
    mock_create_extractor, temp_output_dir, setup_test_files
):
    """Test processing directory with file type filter."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor

    processor = BatchProcessor()

    # Process only PDF files
    successful, failed, errors = processor.process_directory(
        TEST_DATA_DIR, temp_output_dir, file_types=[".pdf"]
    )

    # Verify
    assert successful == 1  # Only PDF
    assert failed == 0
    assert len(errors) == 0
    # Verify that only PDF file was processed
    mock_extractor.extract.assert_called_once()
    args = mock_extractor.extract.call_args[0]
    assert args[0].endswith(".pdf")


@patch("examples.batch_processing.create_extractor")
def test_parallel_processing(
    mock_create_extractor, temp_output_dir, setup_test_files
):
    """Test parallel processing of files."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor

    # Process with multiple workers
    processor = BatchProcessor(max_workers=4)
    successful, failed, errors = processor.process_directory(
        TEST_DATA_DIR, temp_output_dir
    )

    # Verify
    assert successful == 4
    assert failed == 0
    assert len(errors) == 0
    assert mock_extractor.extract.call_count == 4
