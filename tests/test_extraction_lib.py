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

    # Verify output
    with open(output_path, "r") as f:
        content = f.read()
    verify_basic_content(content)
    if file_type in content_verifiers:
        content_verifiers[file_type](content)
