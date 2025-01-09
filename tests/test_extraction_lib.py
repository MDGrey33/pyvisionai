"""Library API tests for file extraction functionality."""

import os
import time

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


@pytest.mark.parametrize(
    "file_type,method",
    testdata_file_extraction,
    ids=ids_file_extraction,
)
def test_file_extraction_lib(file_type, method, setup_test_env):
    """Test file extraction using library API."""
    # Setup
    source_file = os.path.join(
        "content", "test", "source", f"test.{file_type}"
    )
    output_dir = setup_test_env

    # Test API performance and functionality
    start_time = time.time()
    extractor = create_extractor(file_type, method)
    setup_time = time.time() - start_time

    start_time = time.time()
    output_path = extractor.extract(source_file, output_dir)
    extraction_time = time.time() - start_time

    # Measure output size
    output_size = (
        os.path.getsize(output_path)
        if os.path.exists(output_path)
        else 0
    )

    # Log API benchmark results
    api_metrics = {
        "setup_time": setup_time,
        "extraction_time": extraction_time,
        "total_time": setup_time + extraction_time,
        "output_size": output_size,
        "interface": "api",
    }
    log_benchmark(file_type, method, api_metrics)

    # Print performance metrics
    print_performance_metrics(
        file_type, method, setup_time, extraction_time, output_size
    )

    # Verify output
    assert os.path.exists(
        output_path
    ), f"Output file not found: {output_path}"
    with open(output_path, "r") as f:
        content = f.read()

        # Verify basic content requirements
        verify_basic_content(content)

        # Verify file-type specific content
        content_verifiers[file_type](content)
