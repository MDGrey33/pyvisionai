"""Common test fixtures and configuration."""

import json
import logging
import os
import shutil
from datetime import datetime
from unittest.mock import patch

import pytest

from pyvisionai.utils.logger import setup_logger


def copy_test_files(source_dir):
    """Copy test files to the test environment."""
    test_files = {
        "pdf": "test.pdf",
        "docx": "test.docx",
        "pptx": "test.pptx",
        "html": "test.html",
    }

    for _, filename in test_files.items():
        src = os.path.join("content", "test", "source", filename)
        dst = os.path.join(source_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
        else:
            # Create a simple HTML file for testing if it doesn't exist
            if filename.endswith(".html"):
                with open(dst, "w") as f:
                    f.write(
                        "<html><body><h1>Test HTML</h1></body></html>"
                    )
            else:
                raise FileNotFoundError(f"Test file not found: {src}")


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


@pytest.fixture(autouse=True)
def mock_sleep():
    """Mock time.sleep globally to speed up tests."""
    with patch('time.sleep'):
        yield


@pytest.fixture
def benchmark_logger():
    """Create a logger for benchmark results."""
    logger = logging.getLogger("benchmark")
    logger.setLevel(logging.INFO)
    return logger


@pytest.fixture
def setup_test_env(tmp_path):
    """Set up test environment with required directories."""
    content_dir = tmp_path / "content"
    source_dir = content_dir / "source"
    extracted_dir = content_dir / "extracted"
    log_dir = content_dir / "logs"

    # Create directories
    content_dir.mkdir()
    source_dir.mkdir()
    extracted_dir.mkdir()
    log_dir.mkdir()

    # Copy test files
    copy_test_files(str(source_dir))

    # Set up logging
    setup_logger("pyvisionai.test", log_dir=log_dir)

    return {
        "content_dir": str(content_dir),
        "source_dir": str(source_dir),
        "extracted_dir": str(extracted_dir),
        "log_dir": str(log_dir),
    }


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
