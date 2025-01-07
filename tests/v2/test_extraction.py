"""
Integration tests with performance benchmarking for file extraction functionality.
"""

import os
import json
import time
import pytest
import subprocess
from datetime import datetime
from git import Repo
from pyvisionai import create_extractor, describe_image_ollama, describe_image_openai


def get_commit_info():
    """Get current git commit information."""
    repo = Repo(os.getcwd())
    commit = repo.head.commit
    return {
        "hash": commit.hexsha[:8],
        "date": datetime.fromtimestamp(commit.committed_date).isoformat(),
        "message": commit.message.strip(),
    }


def log_benchmark(file_type, method, metrics):
    """Log benchmark results with git commit information."""
    log_dir = "content/log"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "benchmark.log")

    commit_info = get_commit_info()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "commit": commit_info,
        "test": {"file_type": file_type, "method": method},
        "metrics": metrics,
    }

    # Append to log file
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


@pytest.fixture(scope="module")
def setup_test_env():
    """Set up test environment."""
    output_dir = "./content/test/output"
    log_dir = "./content/log"

    # Record existing log files before test
    existing_logs = set()
    if os.path.exists(log_dir):
        existing_logs = {f for f in os.listdir(log_dir) if f.endswith(".log")}

    # Create directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    yield output_dir

    # Cleanup output directory
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))

    # Clean only test-generated log files
    if os.path.exists(log_dir):
        current_logs = {f for f in os.listdir(log_dir) if f.endswith(".log")}
        test_logs = current_logs - existing_logs

        for log_file in test_logs:
            os.remove(os.path.join(log_dir, log_file))

        # Only remove log directory if it's empty and wasn't pre-existing
        if not os.listdir(log_dir) and not existing_logs:
            os.rmdir(log_dir)


# File extraction tests
@pytest.mark.parametrize(
    "file_type,method",
    [
        ("pdf", "page_as_image"),
        ("pdf", "text_and_images"),
        ("docx", "page_as_image"),
        ("docx", "text_and_images"),
        ("pptx", "text_and_images"),
    ],
)
def test_file_extraction_lib(file_type, method, setup_test_env):
    """Test file extraction using library API."""

    # Setup
    source_file = f"./content/test/source/test.{file_type}"
    output_dir = setup_test_env

    # Test API performance and functionality
    start_time = time.time()
    extractor = create_extractor(file_type, method)
    setup_time = time.time() - start_time

    start_time = time.time()
    output_path = extractor.extract(source_file, output_dir)
    extraction_time = time.time() - start_time

    # Measure output size
    output_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0

    # Log API benchmark results
    api_metrics = {
        "setup_time": setup_time,
        "extraction_time": extraction_time,
        "total_time": setup_time + extraction_time,
        "output_size": output_size,
        "interface": "api",
    }
    log_benchmark(file_type, method, api_metrics)

    # Print API performance metrics
    print(f"\n{file_type.upper()} ({method}) API Performance:")
    print(f"Setup time: {setup_time:.2f}s")
    print(f"Extraction time: {extraction_time:.2f}s")
    print(f"Total time: {setup_time + extraction_time:.2f}s")
    print(f"Output size: {output_size/1024:.2f}KB")

    # Functional assertions for API
    assert os.path.exists(output_path)
    with open(output_path, "r") as f:
        content = f.read()
        assert len(content) > 0
        assert "Description:" in content
        assert "# test" in content

        # File type specific assertions
        if file_type == "pdf":
            assert "Page 1" in content
        elif file_type == "pptx":
            assert "Slide 1" in content


@pytest.mark.parametrize(
    "file_type,method",
    [
        ("pdf", "page_as_image"),
        ("pdf", "text_and_images"),
        ("docx", "page_as_image"),
        ("docx", "text_and_images"),
        ("pptx", "text_and_images"),
    ],
)
def test_file_extraction_cli(file_type, method, setup_test_env):
    """Test file extraction using CLI."""

    # Setup
    output_dir = setup_test_env

    # Test CLI performance
    start_time = time.time()
    cmd = [
        "file-extract",
        "--type",
        file_type,
        "--source",
        "./content/test/source",
        "--output",
        output_dir,
        "--extractor",
        method,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    cli_time = time.time() - start_time

    # Get output path
    output_path = os.path.join(output_dir, f"test_{file_type}.md")
    output_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0

    # Log CLI benchmark results
    cli_metrics = {
        "total_time": cli_time,
        "output_size": output_size,
        "interface": "cli",
    }
    log_benchmark(file_type, method, cli_metrics)

    # Print CLI performance metrics
    print(f"\n{file_type.upper()} ({method}) CLI Performance:")
    print(f"Total time: {cli_time:.2f}s")
    print(f"Output size: {output_size/1024:.2f}KB")

    # Functional assertions for CLI
    assert result.returncode == 0, f"CLI command failed with: {result.stderr}"
    assert os.path.exists(output_path)
    with open(output_path, "r") as f:
        content = f.read()
        assert len(content) > 0
        assert "Description:" in content
        assert "# test" in content

        # File type specific assertions
        if file_type == "pdf":
            assert "Page 1" in content
        elif file_type == "pptx":
            assert "Slide 1" in content


# OpenAI Vision tests
def test_image_description_lib_gpt4(setup_test_env):
    """Test image description using GPT-4 through library API."""
    image_path = os.path.join("content", "test", "source", "test.jpeg")

    # Skip if no API key is provided
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("Skipping GPT-4 test - No API key provided")

    # Use GPT-4 Vision
    description = describe_image_openai(image_path, model="gpt-4o-mini")
    assert description and len(description) > 100, "Description seems too short"


def test_image_description_cli_gpt4(setup_test_env):
    """Test image description using GPT-4 through CLI."""
    image_path = os.path.join("content", "test", "source", "test.jpeg")

    # Skip if no API key is provided
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("Skipping GPT-4 test - No API key provided")

    # Run CLI command
    cmd = [
        "describe-image",
        "-i",
        image_path,
        "-u",
        "gpt4",  # Use gpt4 use case
        "-k",
        api_key,
        "-v",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Verify output
    assert result.returncode == 0, f"CLI command failed with: {result.stderr}"
    assert len(result.stdout) > 100, "Description seems too short"


# Local Vision tests
def test_image_description_lib_llama(setup_test_env):
    """Test image description using Llama through library API."""
    image_path = os.path.join("content", "test", "source", "test.jpeg")

    # Use Llama model
    description = describe_image_ollama(image_path, model="llama3.2-vision")
    assert description and len(description) > 100, "Description seems too short"


def test_image_description_cli_llama(setup_test_env):
    """Test image description using Llama through CLI."""
    image_path = os.path.join("content", "test", "source", "test.jpeg")

    # Run CLI command
    cmd = [
        "describe-image",
        "-i",
        image_path,
        "-u",
        "llama",  # Use llama use case
        "-v",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Verify output
    assert result.returncode == 0, f"CLI command failed with: {result.stderr}"
    assert len(result.stdout) > 100, "Description seems too short"


# Benchmark test
def test_benchmark_log_structure():
    """Verify that benchmark logs are being created with correct structure."""
    log_dir = "content/log"
    log_file = os.path.join(log_dir, "benchmark.log")

    assert os.path.exists(log_file), "Benchmark log file should be created"

    with open(log_file, "r") as f:
        last_line = f.readlines()[-1]
        entry = json.loads(last_line)

        # Verify log structure
        assert "timestamp" in entry
        assert "commit" in entry
        assert "hash" in entry["commit"]
        assert "date" in entry["commit"]
        assert "message" in entry["commit"]
        assert "test" in entry
        assert "metrics" in entry

        # Verify metrics structure
        metrics = entry["metrics"]
        if metrics["interface"] == "api":
            assert "setup_time" in metrics
            assert "extraction_time" in metrics
        assert "total_time" in metrics
        assert "output_size" in metrics
