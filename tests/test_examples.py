"""Tests for the example scripts."""

import os
import shutil
import tempfile
from unittest.mock import Mock, patch

import pytest

from examples.basic_extraction import (
    ensure_dir,
    example_docx_extraction,
    example_html_extraction,
    example_image_description,
    example_pdf_extraction,
    example_pptx_extraction,
)

# Test data paths
TEST_DATA_DIR = os.path.join("tests", "data")
TEST_PDF = os.path.join(TEST_DATA_DIR, "sample.pdf")
TEST_DOCX = os.path.join(TEST_DATA_DIR, "sample.docx")
TEST_PPTX = os.path.join(TEST_DATA_DIR, "sample.pptx")
TEST_IMAGE = os.path.join(TEST_DATA_DIR, "sample_image.jpg")

@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir)

@pytest.fixture
def setup_test_files(temp_output_dir):
    """Set up test files and directories."""
    # Create test data directory if it doesn't exist
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    
    # Create sample test files if they don't exist
    if not os.path.exists(TEST_PDF):
        with open(TEST_PDF, "w") as f:
            f.write("Sample PDF content")
    
    if not os.path.exists(TEST_DOCX):
        with open(TEST_DOCX, "w") as f:
            f.write("Sample DOCX content")
    
    if not os.path.exists(TEST_PPTX):
        with open(TEST_PPTX, "w") as f:
            f.write("Sample PPTX content")
    
    if not os.path.exists(TEST_IMAGE):
        with open(TEST_IMAGE, "w") as f:
            f.write("Sample image content")
    
    yield

def test_ensure_dir(temp_output_dir):
    """Test directory creation function."""
    test_dir = os.path.join(temp_output_dir, "test_dir")
    ensure_dir(test_dir)
    assert os.path.exists(test_dir)
    assert os.path.isdir(test_dir)

@patch("examples.basic_extraction.create_extractor")
def test_pdf_extraction(mock_create_extractor, temp_output_dir, setup_test_files):
    """Test PDF extraction example."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor
    
    # Run example
    with patch("builtins.print"):  # Suppress print output
        example_pdf_extraction()
    
    # Verify
    mock_create_extractor.assert_called_once_with("pdf")
    mock_extractor.extract.assert_called_once()
    args = mock_extractor.extract.call_args[0]
    assert args[0].endswith("sample.pdf")
    assert args[1].endswith("pdf")

@patch("examples.basic_extraction.create_extractor")
def test_docx_extraction(mock_create_extractor, temp_output_dir, setup_test_files):
    """Test DOCX extraction example."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor
    
    # Run example
    with patch("builtins.print"):
        example_docx_extraction()
    
    # Verify
    mock_create_extractor.assert_called_once_with(
        "docx",
        extractor_type="text_and_images"
    )
    mock_extractor.extract.assert_called_once()
    args = mock_extractor.extract.call_args[0]
    assert args[0].endswith("sample.docx")
    assert args[1].endswith("docx")

@patch("examples.basic_extraction.create_extractor")
def test_pptx_extraction(mock_create_extractor, temp_output_dir, setup_test_files):
    """Test PPTX extraction example."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor
    
    # Run example
    with patch("builtins.print"):
        example_pptx_extraction()
    
    # Verify
    mock_create_extractor.assert_called_once_with(
        "pptx",
        prompt="List all text content and describe any diagrams or charts"
    )
    mock_extractor.extract.assert_called_once()
    args = mock_extractor.extract.call_args[0]
    assert args[0].endswith("sample.pptx")
    assert args[1].endswith("pptx")

@patch("examples.basic_extraction.create_extractor")
def test_html_extraction(mock_create_extractor, temp_output_dir):
    """Test HTML extraction example."""
    # Setup mock
    mock_extractor = Mock()
    mock_extractor.extract.return_value = "output.md"
    mock_create_extractor.return_value = mock_extractor
    
    # Run example
    with patch("builtins.print"):
        example_html_extraction()
    
    # Verify
    mock_create_extractor.assert_called_once_with("html")
    mock_extractor.extract.assert_called_once_with(
        "https://example.com",
        "output/html"
    )

@patch("examples.basic_extraction.describe_image_openai")
def test_image_description(mock_describe_image, temp_output_dir, setup_test_files):
    """Test image description example."""
    # Setup mock
    mock_describe_image.return_value = "Image description"
    
    # Run example
    with patch("builtins.print"):
        example_image_description()
    
    # Verify
    mock_describe_image.assert_called_once_with(
        os.path.join("example_data", "sample_image.jpg"),
        prompt="Describe the main elements and any text in this image"
    )

def test_file_not_found_handling():
    """Test error handling when files don't exist."""
    with patch("builtins.print") as mock_print:
        # Test with non-existent PDF
        with patch("examples.basic_extraction.create_extractor") as mock_create:
            mock_extractor = Mock()
            mock_extractor.extract.side_effect = FileNotFoundError(
                "example_data/sample.pdf"
            )
            mock_create.return_value = mock_extractor
            example_pdf_extraction()
            mock_print.assert_any_call("\n=== PDF Extraction Example ===")
            mock_print.assert_any_call(
                "Error processing technical doc: File not found - example_data/sample.pdf"
            )
        
        # Test with non-existent DOCX
        with patch("examples.basic_extraction.create_extractor") as mock_create:
            mock_extractor = Mock()
            mock_extractor.extract.side_effect = FileNotFoundError(
                "example_data/sample.docx"
            )
            mock_create.return_value = mock_extractor
            example_docx_extraction()
            mock_print.assert_any_call("\n=== Word Document Extraction Example ===")
            mock_print.assert_any_call(
                "Error processing technical doc: File not found - example_data/sample.docx"
            )
        
        # Test with non-existent PPTX
        with patch("examples.basic_extraction.create_extractor") as mock_create:
            mock_extractor = Mock()
            mock_extractor.extract.side_effect = FileNotFoundError(
                "example_data/sample.pptx"
            )
            mock_create.return_value = mock_extractor
            example_pptx_extraction()
            mock_print.assert_any_call("\n=== PowerPoint Extraction Example ===")
            mock_print.assert_any_call(
                "Error processing technical doc: File not found - example_data/sample.pptx"
            )
        
        # Test with non-existent image
        with patch("examples.basic_extraction.describe_image_openai") as mock_describe:
            mock_describe.side_effect = FileNotFoundError(
                "example_data/sample_image.jpg"
            )
            example_image_description()
            mock_print.assert_any_call("\n=== Image Description Example ===")
            mock_print.assert_any_call(
                "Error analyzing chart: File not found - example_data/sample_image.jpg"
            ) 