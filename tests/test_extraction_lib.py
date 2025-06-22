"""Library API tests for file extraction functionality."""

import os
import time
from unittest.mock import MagicMock, mock_open, patch

import pytest

from pyvisionai import create_extractor
from tests.conftest import (
    ids_file_extraction,
    log_benchmark,
    testdata_file_extraction,
)
from tests.utils.metrics import print_performance_metrics
from tests.utils.verifiers import (
    content_verifiers,
    verify_basic_content,
)


@pytest.mark.unit
class TestFileExtractionUnit:
    """Unit tests for file extraction with mocked dependencies."""

    def test_pdf_extractor_creation(self):
        """Test PDF extractor creation."""
        # Test page_as_image method
        extractor = create_extractor("pdf", "page_as_image")
        assert extractor is not None
        assert hasattr(extractor, 'extract')

        # Test text_and_images method
        extractor = create_extractor("pdf", "text_and_images")
        assert extractor is not None
        assert hasattr(extractor, 'extract')

    def test_docx_extractor_creation(self):
        """Test DOCX extractor creation."""
        # Test page_as_image method
        extractor = create_extractor("docx", "page_as_image")
        assert extractor is not None
        assert hasattr(extractor, 'extract')

        # Test text_and_images method
        extractor = create_extractor("docx", "text_and_images")
        assert extractor is not None
        assert hasattr(extractor, 'extract')

    def test_pptx_extractor_creation(self):
        """Test PPTX extractor creation."""
        # Test page_as_image method
        extractor = create_extractor("pptx", "page_as_image")
        assert extractor is not None
        assert hasattr(extractor, 'extract')

        # Test text_and_images method
        extractor = create_extractor("pptx", "text_and_images")
        assert extractor is not None
        assert hasattr(extractor, 'extract')

    def test_create_extractor_invalid_file_type(self):
        """Test creating extractor with invalid file type."""
        with pytest.raises(ValueError, match="Unsupported file type"):
            create_extractor("invalid", "page_as_image")

    def test_create_extractor_invalid_method(self):
        """Test creating extractor with invalid method."""
        with pytest.raises(
            ValueError, match="Unsupported extractor type"
        ):
            create_extractor("pdf", "invalid_method")


@pytest.mark.integration
@pytest.mark.parametrize(
    "file_type,method",
    testdata_file_extraction,
    ids=ids_file_extraction,
)
def test_file_extraction_lib(file_type, method, setup_test_env):
    """Test file extraction using library API (integration test)."""
    # Skip if required API keys are not available
    if method == "text_and_images" and not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
    if method == "page_as_image" and not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")

    # Skip DOCX/PPTX page_as_image tests if LibreOffice is not installed
    if file_type in ["docx", "pptx"] and method == "page_as_image":
        import shutil

        if not shutil.which("soffice"):
            pytest.skip(
                "LibreOffice (soffice) not installed - required for DOCX/PPTX page_as_image extraction"
            )

    # Setup
    filename = "test"
    source_file = os.path.join(
        setup_test_env["source_dir"], f"{filename}.{file_type}"
    )
    # Create unique output directory for this test
    test_output_dir = os.path.join(
        setup_test_env["extracted_dir"], f"{file_type}_{method}"
    )
    os.makedirs(test_output_dir, exist_ok=True)

    # Test API performance and functionality
    start_time = time.time()
    extractor = create_extractor(file_type, method)
    setup_time = time.time() - start_time

    start_time = time.time()
    output_path = extractor.extract(source_file, test_output_dir)
    extraction_time = time.time() - start_time

    # Measure output size
    output_size = (
        os.path.getsize(output_path)
        if os.path.exists(output_path)
        else 0
    )

    # Log API benchmark results
    log_benchmark(
        file_type,
        method,
        {
            "setup_time": setup_time,
            "extraction_time": extraction_time,
            "output_size": output_size,
        },
    )

    # Print performance metrics
    print_performance_metrics(
        file_type=file_type,
        method=method,
        setup_time=setup_time,
        extraction_time=extraction_time,
        output_size=output_size,
        interface="API",
    )

    # Verify output exists
    assert os.path.exists(
        output_path
    ), f"Output file not created: {output_path}"

    # Verify output content
    with open(output_path, "r") as f:
        content = f.read()

    # Basic verification - just check it's not empty
    assert content.strip(), "Output file is empty"

    # Skip detailed verification for integration tests to avoid API-specific content checks
    # Just verify basic structure
    verify_basic_content(content)
