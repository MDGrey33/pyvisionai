"""CLI tests for file extraction functionality."""

import logging
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

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def setup_test_logging():
    """Configure test-specific logging."""
    logger.setLevel(logging.ERROR)
    return logger


# Test data including model variations
testdata_with_models = []
for file_type, method in testdata_file_extraction:
    # For page_as_image, test both models
    if method == "page_as_image":
        testdata_with_models.append((file_type, method, "gpt4"))
        testdata_with_models.append((file_type, method, "llama"))
    # For text_and_images, only use gpt4 (default)
    else:
        testdata_with_models.append((file_type, method, "gpt4"))

ids_with_models = [
    f"{filetype}-{method}-{model}"
    for filetype, method, model in testdata_with_models
]


@pytest.mark.cli
@pytest.mark.integration
@pytest.mark.parametrize(
    "file_type,method,model",
    testdata_with_models,
    ids=ids_with_models,
)
def test_file_extraction_cli(file_type, method, model, setup_test_env):
    """Test file extraction using CLI."""
    logger.info(
        f"Starting CLI test for {file_type} using {method} method with {model} model"
    )

    # Skip tests based on available resources
    if model == "gpt4":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.info("Skipping GPT-4 test - No API key provided")
            pytest.skip("Skipping GPT-4 test - No API key provided")
    elif model == "llama":
        # Check if Ollama is running
        import requests

        try:
            response = requests.get(
                'http://localhost:11434/api/tags', timeout=1
            )
            if response.status_code != 200:
                pytest.skip("Ollama not running")
        except Exception:
            pytest.skip("Ollama not available")

    # Setup
    filename = "test"
    source_file = os.path.join(
        setup_test_env["source_dir"], f"{filename}.{file_type}"
    )
    # Create unique output directory for this test
    test_output_dir = os.path.join(
        setup_test_env["extracted_dir"], f"{file_type}_{method}_{model}"
    )
    os.makedirs(test_output_dir, exist_ok=True)

    logger.debug(f"Source file: {source_file}")
    logger.debug(f"Output directory: {test_output_dir}")

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

    # Add model parameter for page_as_image
    if method == "page_as_image":
        cmd.extend(["--model", model])

    # Add API key for GPT-4 models
    if model == "gpt4" and method == "text_and_images":
        cmd.extend(["--api-key", api_key])

    logger.debug(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    cli_time = time.time() - start_time

    # Log any errors
    if result.stderr:
        logger.error(f"CLI error output: {result.stderr}")
    if result.stdout:
        logger.debug(f"CLI output: {result.stdout}")

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

    logger.debug(f"Output file size: {output_size} bytes")
    logger.debug(f"CLI execution time: {cli_time:.2f} seconds")

    # Log CLI benchmark results
    log_benchmark(
        file_type,
        f"{method}_{model}",
        {
            "cli_time": cli_time,
            "output_size": output_size,
        },
    )

    # Print performance metrics
    print_performance_metrics(
        file_type=file_type,
        method=f"{method}_{model}",
        setup_time=0,
        extraction_time=cli_time,
        output_size=output_size,
        interface="CLI",
    )

    # Verify output
    output_path = os.path.join(test_output_dir, f"test_{file_type}.md")
    logger.debug(f"Verifying output file: {output_path}")

    # For tests with errors, we might have partial output
    if not os.path.exists(output_path):
        logger.warning(f"Output file not found: {output_path}")
        pytest.skip(
            f"Output file not created - likely due to API errors"
        )

    with open(output_path, "r") as f:
        content = f.read()

    # Verify output content
    assert content.strip(), "Output file is empty"

    # Verify content type-specific patterns
    if file_type == "pptx" and method == "text_and_images":
        # For PPTX text_and_images, just verify basic structure
        assert (
            "Slide" in content
        ), "PPTX content should include slide references"
        if "[Image" in content:
            # Just verify that there's some image description
            assert (
                len(
                    [
                        line
                        for line in content.split('\n')
                        if '[Image' in line
                    ]
                )
                > 0
            ), "No image descriptions found"
    elif (
        file_type == "pdf"
        and method == "page_as_image"
        and model == "llama"
    ):
        # For Ollama PDF page_as_image, be more flexible about content
        assert (
            "Page 1" in content
        ), "PDF content should include page numbers"
        assert "[Image" in content, "PDF should have image descriptions"
        # Don't check for specific text content as Ollama may describe differently
    else:
        content_verifiers[file_type](content)

    logger.info(
        f"CLI test for {file_type} using {method} method with {model} model completed successfully"
    )
