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
    filename = "test"
    source_file = os.path.join(
        setup_test_env["source_dir"], f"{filename}.{file_type}"
    )
    # Create unique output directory for this test
    test_output_dir = os.path.join(
        setup_test_env["extracted_dir"], f"{file_type}_{method}"
    )
    os.makedirs(test_output_dir, exist_ok=True)

    # Test CLI performance
    start_time = time.time()
    cmd = [
        "file-extract",
        "--type",
        file_type,
        "--source",
        source_file,
        "--output",
        test_output_dir,
        "--extractor",
        method,
    ]

    # Add API key for text_and_images method
    if method == "text_and_images":
        cmd.extend(["--api-key", api_key])

    result = subprocess.run(cmd, capture_output=True, text=True)
    cli_time = time.time() - start_time

    # Get output path
    base_name = os.path.splitext(os.path.basename(source_file))[0]
    output_path = os.path.join(
        test_output_dir, f"{base_name}_{file_type}.md"
    )
    output_size = (
        os.path.getsize(output_path)
        if os.path.exists(output_path)
        else 0
    )

    # Log CLI benchmark results
    log_benchmark(
        file_type,
        method,
        {
            "cli_time": cli_time,
            "output_size": output_size,
        },
    )

    # Print performance metrics
    print_performance_metrics(
        file_type=file_type,
        method=method,
        setup_time=0,
        extraction_time=cli_time,
        output_size=output_size,
        interface="CLI",
    )

    # Verify output
    output_path = os.path.join(test_output_dir, f"test_{file_type}.md")
    with open(output_path, "r") as f:
        content = f.read()
    verify_basic_content(content)
    if file_type in content_verifiers:
        content_verifiers[file_type](content)
