"""CLI tests for file extraction functionality."""

import os
import subprocess
import time

import pytest

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
def test_file_extraction_cli(file_type, method, setup_test_env):
    """Test file extraction using CLI."""
    # Skip if no API key is provided for text_and_images method
    if method == "text_and_images":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("Skipping GPT-4 test - No API key provided")

    # Setup
    output_dir = setup_test_env
    source_path = os.path.join("content", "test", "source")
    source_file = f"test.{file_type}"

    # Test CLI performance
    start_time = time.time()
    cmd = [
        "file-extract",
        "--type",
        file_type,
        "--source",
        os.path.join(source_path, source_file),
        "--output",
        output_dir,
        "--extractor",
        method,
    ]
    
    # Add API key for text_and_images method
    if method == "text_and_images":
        cmd.extend(["--api-key", api_key])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    cli_time = time.time() - start_time

    # Get output path
    base_name = os.path.splitext(source_file)[0]
    output_path = os.path.join(
        output_dir, f"{base_name}_{file_type}.md"
    )
    output_size = (
        os.path.getsize(output_path)
        if os.path.exists(output_path)
        else 0
    )

    # Log CLI benchmark results
    cli_metrics = {
        "total_time": cli_time,
        "output_size": output_size,
        "interface": "cli",
    }
    log_benchmark(file_type, method, cli_metrics)

    # Print performance metrics
    print_performance_metrics(
        file_type, method, 0, cli_time, output_size, interface="CLI"
    )

    # Verify output
    assert (
        result.returncode == 0
    ), f"CLI command failed with: {result.stderr}"
    assert os.path.exists(
        output_path
    ), f"Output file not found: {output_path}"
    with open(output_path, "r") as f:
        content = f.read()

        # Verify basic content requirements
        verify_basic_content(content)

        # Verify file-type specific content
        content_verifiers[file_type](content)
