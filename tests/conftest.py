"""Test configuration and shared fixtures."""

import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from pyvisionai.utils.benchmark import BenchmarkLogger
from pyvisionai.utils.logger import setup_logger


# Configure logging
def configure_test_logging():
    """Configure logging to suppress verbose output."""
    logging.getLogger("httpcore").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger("anthropic").setLevel(logging.ERROR)

    # Disable propagation for these loggers
    for logger_name in ["httpcore", "httpx", "openai", "anthropic"]:
        logger = logging.getLogger(logger_name)
        logger.propagate = False


logger = logging.getLogger(__name__)
configure_test_logging()

# Test data for file extraction
testdata_file_extraction = [
    ("pdf", "page_as_image"),
    ("pdf", "text_and_images"),
    ("docx", "page_as_image"),
    ("docx", "text_and_images"),
    ("pptx", "page_as_image"),
    ("pptx", "text_and_images"),
]

ids_file_extraction = [
    f"{filetype}-{method}"
    for filetype, method in testdata_file_extraction
]


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


@pytest.fixture
def benchmark_log_file(tmp_path):
    """Create a temporary benchmark log file."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    return log_dir / "benchmark.log"


@pytest.fixture
def benchmark_logger(benchmark_log_file):
    """Create a benchmark logger with a temporary file."""
    logger = BenchmarkLogger(log_dir=benchmark_log_file.parent)
    logger.logger = logging.getLogger("benchmark")
    logger.logger.setLevel(logging.INFO)
    return logger


def log_benchmark(file_type, method, metrics, log_dir=None):
    """Log benchmark results using the benchmark logger.

    Args:
        file_type: Type of file being processed
        method: Extraction method used
        metrics: Dictionary containing benchmark metrics
        log_dir: Optional directory for log file (default: content/log)
    """
    logger = BenchmarkLogger(log_dir or "content/log")
    logger.log(file_type, method, metrics)


@pytest.fixture(autouse=True)
def clean_benchmark_logs():
    """Clean up benchmark logs after each test."""
    yield
    log_file = Path("content/log/benchmark.log")
    lock_file = Path("content/log/benchmark.log.lock")
    if log_file.exists():
        log_file.unlink()
    if lock_file.exists():
        lock_file.unlink()


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line(
        "markers", "cli: command line interface tests"
    )
    config.addinivalue_line(
        "markers", "openai: tests requiring OpenAI API"
    )
    config.addinivalue_line(
        "markers", "claude: tests requiring Claude API"
    )
    config.addinivalue_line("markers", "ollama: tests requiring Ollama")


@pytest.fixture(autouse=True)
def mock_sleep():
    """Mock time.sleep globally to speed up tests."""
    with patch('time.sleep'):
        yield


@pytest.fixture(autouse=True)
def skip_by_api_key(request):
    """Skip tests if required API key is missing."""
    if request.node.get_closest_marker('openai'):
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip('OpenAI API key missing')
    elif request.node.get_closest_marker('claude'):
        if not os.getenv('ANTHROPIC_API_KEY'):
            pytest.skip('Anthropic API key missing')


@pytest.fixture
def test_image_path():
    """Provide path to test image."""
    return str(Path("content") / "test" / "source" / "test.jpeg")


@pytest.fixture
def mock_api_response():
    """Provide mock API response."""
    return {"text": "A forest scene with tall trees and green foliage."}


@pytest.fixture
def setup_test_env(tmp_path):
    """Set up test environment with required directories."""
    content_dir = tmp_path / "content"
    source_dir = content_dir / "source"
    extracted_dir = content_dir / "extracted"
    log_dir = content_dir / "logs"

    # Create directories
    for dir_path in [content_dir, source_dir, extracted_dir, log_dir]:
        dir_path.mkdir(exist_ok=True)

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
