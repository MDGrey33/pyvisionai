"""Test configuration and shared fixtures."""

import json
import logging
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from pyvisionai.utils.benchmark import BenchmarkLogger
from pyvisionai.utils.logger import setup_logger


# Configure logging for tests
def configure_test_logging():
    """Configure logging to reasonable levels for testing."""
    # Set reasonable levels for external libraries
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    logging.getLogger("playwright").setLevel(logging.WARNING)

    # Set our library to INFO for better debugging
    logging.getLogger("pyvisionai").setLevel(logging.INFO)


logger = logging.getLogger(__name__)
configure_test_logging()


def pytest_configure(config):
    """Register custom markers."""
    # Markers are now defined in pytest.ini
    pass


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


# ==================== Mock Fixtures ====================


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client with successful response."""
    with patch('openai.OpenAI') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance

        # Mock the chat completion response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content="This is a mocked description of the image."
                )
            )
        ]
        mock_instance.chat.completions.create.return_value = (
            mock_response
        )

        yield mock_instance


@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client with successful response."""
    with patch('anthropic.Anthropic') as mock_class:
        mock_instance = MagicMock()
        mock_class.return_value = mock_instance

        # Mock the messages create response
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text="This is a mocked Claude description.")
        ]
        mock_instance.messages.create.return_value = mock_response

        yield mock_instance


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client with successful response."""
    with patch('requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "content": "This is a mocked Ollama description."
            }
        }
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture(autouse=True)
def mock_playwright_for_unit_tests(request):
    """Mock playwright for unit tests to avoid browser dependencies."""
    if request.node.get_closest_marker('unit') or (
        not request.node.get_closest_marker('e2e')
        and not request.node.get_closest_marker('integration')
    ):
        with patch(
            'pyvisionai.extractors.html.browser.async_playwright'
        ) as mock_playwright:
            # Mock the entire playwright flow
            mock_page = MagicMock()
            mock_page.screenshot.return_value = b'fake_screenshot_data'
            mock_browser = MagicMock()
            mock_browser.new_page.return_value = mock_page
            mock_chromium = MagicMock()
            mock_chromium.launch.return_value = mock_browser
            mock_pw = MagicMock()
            mock_pw.chromium = mock_chromium
            mock_pw.start.return_value = mock_pw
            mock_playwright.return_value.__aenter__.return_value = (
                mock_pw
            )
            yield
    else:
        yield


@pytest.fixture(autouse=True)
def mock_libreoffice_for_unit_tests(request):
    """Mock LibreOffice (soffice) for unit tests."""
    if request.node.get_closest_marker('unit') or (
        not request.node.get_closest_marker('e2e')
        and not request.node.get_closest_marker('integration')
    ):
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            yield
    else:
        yield


# ==================== Test Environment Fixtures ====================


@pytest.fixture
def temp_test_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def test_files_dir():
    """Get the test files directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_pdf_path(test_files_dir):
    """Path to sample PDF file."""
    pdf_path = test_files_dir / "sample.pdf"
    if not pdf_path.exists():
        # Create a minimal PDF for testing
        pdf_path.parent.mkdir(exist_ok=True)
        pdf_path.write_bytes(
            b'%PDF-1.4\n1 0 obj\n<< >>\nendobj\ntrailer\n<< >>\n%%EOF'
        )
    return pdf_path


@pytest.fixture
def sample_image_path(test_files_dir):
    """Path to sample image file."""
    img_path = test_files_dir / "sample.jpg"
    if not img_path.exists():
        # Create a minimal JPEG for testing
        img_path.parent.mkdir(exist_ok=True)
        # Minimal JPEG header
        img_path.write_bytes(
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xd9'
        )
    return img_path


@pytest.fixture
def setup_test_env(temp_test_dir):
    """Set up test environment with required directories."""
    content_dir = temp_test_dir / "content"
    source_dir = content_dir / "source"
    extracted_dir = content_dir / "extracted"
    log_dir = content_dir / "log"

    # Create directories
    for dir_path in [content_dir, source_dir, extracted_dir, log_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Copy real test files from content/test/source/
    import shutil

    test_files_source = Path("content/test/source")
    if test_files_source.exists():
        for test_file in test_files_source.glob("test.*"):
            shutil.copy2(test_file, source_dir / test_file.name)
    else:
        # Fallback to minimal test files if real ones don't exist
        (source_dir / "test.pdf").write_bytes(b'%PDF-1.4\n%%EOF')
        (source_dir / "test.html").write_text(
            '<html><body>Test</body></html>'
        )
        (source_dir / "test.docx").write_bytes(
            b'PK'
        )  # Minimal zip header
        (source_dir / "test.pptx").write_bytes(
            b'PK'
        )  # Minimal zip header

    return {
        "content_dir": str(content_dir),
        "source_dir": str(source_dir),
        "extracted_dir": str(extracted_dir),
        "log_dir": str(log_dir),
    }


# ==================== Auto-use Fixtures ====================


@pytest.fixture(autouse=True)
def clean_test_environment():
    """Ensure clean test environment before and after each test."""
    # Clean before
    yield
    # Clean after - nothing needed with temp directories


@pytest.fixture(autouse=True)
def mock_sleep_for_unit_tests(request):
    """Mock time.sleep for unit tests to speed them up."""
    if request.node.get_closest_marker(
        'unit'
    ) or not request.node.get_closest_marker('slow'):
        with patch('time.sleep'):
            yield
    else:
        yield


@pytest.fixture(autouse=True)
def configure_api_mocks(
    request,
    mock_openai_client,
    mock_anthropic_client,
    mock_ollama_client,
):
    """Automatically mock API calls for non-e2e tests."""
    if not request.node.get_closest_marker('e2e'):
        # APIs are already mocked via fixtures
        pass


@pytest.fixture(autouse=True)
def skip_by_marker(request):
    """Skip tests based on markers and available resources."""
    if request.node.get_closest_marker('e2e'):
        if request.node.get_closest_marker('openai') and not os.getenv(
            'OPENAI_API_KEY'
        ):
            pytest.skip('OpenAI API key not available for e2e test')
        if request.node.get_closest_marker('claude') and not os.getenv(
            'ANTHROPIC_API_KEY'
        ):
            pytest.skip('Anthropic API key not available for e2e test')
        if request.node.get_closest_marker('ollama'):
            # Check if Ollama is running
            import requests

            try:
                requests.get(
                    'http://localhost:11434/api/tags', timeout=1
                )
            except Exception:
                pytest.skip('Ollama not running for e2e test')


# ==================== Benchmark Fixtures ====================


@pytest.fixture
def benchmark_log_file(temp_test_dir):
    """Create a temporary benchmark log file."""
    log_dir = temp_test_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    return log_dir / "benchmark.log"


@pytest.fixture
def benchmark_logger(temp_test_dir):
    """Create a benchmark logger with a temporary file."""
    log_dir = temp_test_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    logger = BenchmarkLogger(log_dir=str(log_dir))
    return logger


# ==================== Test Data ====================

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
