"""Common test fixtures and configuration."""

import os
import json
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

