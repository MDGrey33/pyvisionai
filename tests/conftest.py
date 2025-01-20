"""Common test fixtures and configuration."""

import json
import os
from datetime import datetime

import pytest


def log_benchmark(file_type, method, metrics):
    """Log benchmark results."""
    log_dir = os.path.join("content", "log")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "benchmark.log")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "test": {"file_type": file_type, "method": method},
        "metrics": metrics,
    }

    # Append to log file
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


@pytest.fixture(scope="module")
def setup_test_env():
    """Set up test environment."""
    output_dir = os.path.join("content", "test", "output")
    log_dir = os.path.join("content", "log")

    # Record existing log files before test
    existing_logs = set()
    if os.path.exists(log_dir):
        existing_logs = {
            f for f in os.listdir(log_dir) if f.endswith(".log")
        }

    # Create directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    yield output_dir

    # Cleanup output directory
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except (OSError, PermissionError):
                pass  # Skip files we can't remove

    # Clean only test-generated log files
    if os.path.exists(log_dir):
        current_logs = {
            f for f in os.listdir(log_dir) if f.endswith(".log")
        }
        test_logs = current_logs - existing_logs

        for log_file in test_logs:
            try:
                os.remove(os.path.join(log_dir, log_file))
            except (OSError, PermissionError):
                pass  # Skip files we can't remove


# Test data for file extraction
testdata_file_extraction = (
    ("pdf", "page_as_image"),
    ("pdf", "text_and_images"),
    ("docx", "page_as_image"),
    ("docx", "text_and_images"),
    ("pptx", "page_as_image"),
    ("html", "page_as_image"),
)

ids_file_extraction = (
    "PDF using page-as-image method",
    "PDF using text-and-images method",
    "DOCX using page-as-image method",
    "DOCX using text-and-images method",
    "PPTX using page-as-image method",
    "HTML using page-as-image method",
)
