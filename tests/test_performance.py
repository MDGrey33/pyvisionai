"""
Performance benchmark tests.
"""

import os
import time
import pytest
from pyvisionai import create_extractor


@pytest.fixture
def test_dirs():
    """Create and return test directories."""
    source_dir = "./content/test/source"
    output_dir = "./content/test/output"
    os.makedirs(output_dir, exist_ok=True)
    return source_dir, output_dir


def measure_extraction_time(file_type, extractor_type=None):
    """Measure time taken for extraction process."""
    source_dir = "./content/test/source"
    output_dir = "./content/test/output"
    test_file = os.path.join(source_dir, f"test.{file_type}")

    # Create extractor
    start_time = time.time()
    extractor = create_extractor(
        file_type, extractor_type=extractor_type or "text_and_images"
    )
    setup_time = time.time() - start_time

    # Extract content
    start_time = time.time()
    output_path = extractor.extract(test_file, output_dir)
    extraction_time = time.time() - start_time

    return {
        "setup_time": setup_time,
        "extraction_time": extraction_time,
        "total_time": setup_time + extraction_time,
        "output_size": (
            os.path.getsize(output_path) if os.path.exists(output_path) else 0
        ),
    }


def test_pdf_performance():
    """Benchmark PDF extraction performance."""
    # Test page-as-image method
    results_page = measure_extraction_time("pdf", "page_as_image")
    print(f"\nPDF (page-as-image) Performance:")
    print(f"Setup time: {results_page['setup_time']:.2f}s")
    print(f"Extraction time: {results_page['extraction_time']:.2f}s")
    print(f"Total time: {results_page['total_time']:.2f}s")
    print(f"Output size: {results_page['output_size']/1024:.2f}KB")

    # Test text-and-images method
    results_text = measure_extraction_time("pdf", "text_and_images")
    print(f"\nPDF (text-and-images) Performance:")
    print(f"Setup time: {results_text['setup_time']:.2f}s")
    print(f"Extraction time: {results_text['extraction_time']:.2f}s")
    print(f"Total time: {results_text['total_time']:.2f}s")
    print(f"Output size: {results_text['output_size']/1024:.2f}KB")


def test_docx_performance():
    """Benchmark DOCX extraction performance."""
    # Test page-as-image method
    results_page = measure_extraction_time("docx", "page_as_image")
    print(f"\nDOCX (page-as-image) Performance:")
    print(f"Setup time: {results_page['setup_time']:.2f}s")
    print(f"Extraction time: {results_page['extraction_time']:.2f}s")
    print(f"Total time: {results_page['total_time']:.2f}s")
    print(f"Output size: {results_page['output_size']/1024:.2f}KB")

    # Test text-and-images method
    results_text = measure_extraction_time("docx", "text_and_images")
    print(f"\nDOCX (text-and-images) Performance:")
    print(f"Setup time: {results_text['setup_time']:.2f}s")
    print(f"Extraction time: {results_text['extraction_time']:.2f}s")
    print(f"Total time: {results_text['total_time']:.2f}s")
    print(f"Output size: {results_text['output_size']/1024:.2f}KB")


def test_pptx_performance():
    """Benchmark PPTX extraction performance."""
    results = measure_extraction_time("pptx", "text_and_images")
    print(f"\nPPTX Performance:")
    print(f"Setup time: {results['setup_time']:.2f}s")
    print(f"Extraction time: {results['extraction_time']:.2f}s")
    print(f"Total time: {results['total_time']:.2f}s")
    print(f"Output size: {results['output_size']/1024:.2f}KB")
