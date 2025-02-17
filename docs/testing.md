# Testing Guide

This document provides a comprehensive guide to running tests in the PyVisionAI project.

## Table of Contents
- [Testing Guide](#testing-guide)
  - [Table of Contents](#table-of-contents)
  - [Test Organization](#test-organization)
    - [Directory Structure](#directory-structure)
    - [Test Categories](#test-categories)
    - [Test Naming Conventions](#test-naming-conventions)
  - [Running Tests](#running-tests)
    - [Basic Test Execution](#basic-test-execution)
    - [Advanced Test Selection](#advanced-test-selection)
    - [Parallel Test Execution](#parallel-test-execution)
  - [Test Requirements](#test-requirements)
    - [Environment Setup](#environment-setup)
    - [API Keys](#api-keys)
    - [Dependencies](#dependencies)
  - [Configuration](#configuration)
    - [pytest.ini Settings](#pytestini-settings)
    - [Custom Markers](#custom-markers)
    - [Fixture Management](#fixture-management)
  - [Writing Tests](#writing-tests)
    - [Test Structure](#test-structure)
    - [Best Practices](#best-practices)
    - [Fixtures and Mocking](#fixtures-and-mocking)
    - [Test Fixtures](#test-fixtures)
    - [Mocking External Services](#mocking-external-services)
  - [Performance Testing](#performance-testing)
    - [Benchmark Tests](#benchmark-tests)

## Test Organization

### Directory Structure

The test suite follows a structured organization:

```
tests/
├── core/              # Core functionality tests
│   ├── test_extractor.py
│   └── test_factory.py
├── describers/        # Vision model tests
│   ├── test_base.py
│   ├── test_claude.py
│   ├── test_openai.py
│   └── test_ollama.py
├── extractors/        # File extraction tests
│   ├── test_pdf.py
│   ├── test_docx.py
│   └── test_pptx.py
├── utils/            # Utility function tests
│   ├── test_retry.py
│   └── test_benchmark.py
├── conftest.py      # Shared test configuration and fixtures
└── test_*.py        # Top-level integration and feature tests
```

### Test Categories

1. **Unit Tests**
   - Test individual components in isolation
   - Mock external dependencies
   - Fast execution

2. **Integration Tests**
   - Test component interactions
   - May require external services
   - Slower execution

3. **End-to-End Tests**
   - Test complete workflows
   - Require all dependencies
   - Slowest execution

4. **Model-Specific Tests**
   - Tests for each vision model (GPT-4, Claude, Llama)
   - API integration tests
   - Error handling and retry logic
   - Rate limit handling

Tests are organized into several categories using pytest markers:

```python
# Integration Tests
@pytest.mark.integration
def test_end_to_end():
    pass

# CLI Tests
@pytest.mark.cli
class TestCLI:
    pass

# Model-specific Tests
@pytest.mark.openai
@pytest.mark.ollama
@pytest.mark.claude  # New marker for Claude tests
def test_model():
    pass
```

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Integration tests: `test_*_integration.py`
- Benchmark tests: `test_*_benchmark.py`

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with different verbosity levels
pytest -q  # quiet
pytest -v  # verbose
pytest -vv # very verbose

# Run with test selection
pytest -k "pattern"  # run tests matching pattern
pytest -m marker    # run tests with specific marker
```

### Advanced Test Selection

```bash
# Run tests by module
pytest tests/describers/

# Run tests by class
pytest tests/test_cli.py::TestDescribeImageCLI

# Run specific test
pytest tests/test_image_description.py::test_image_description_lib_gpt4

# Run tests by marker combination
pytest -m "integration and not openai"
pytest -m "cli or integration"
```

### Parallel Test Execution

```bash
# Run tests in parallel
pytest -n auto  # use all CPU cores
pytest -n 4     # use 4 cores

# Run tests in parallel with specific groups
pytest -n auto --dist=loadgroup
```

## Test Requirements

### Environment Setup

Before running tests, ensure you have the necessary environment variables set:

```bash
# For GPT-4 Vision tests
export OPENAI_API_KEY='your-openai-key'

# For Claude Vision tests
export ANTHROPIC_API_KEY='your-anthropic-key'

# For local Llama tests (optional)
export OLLAMA_HOST='http://localhost:11434'
```

Note: Tests requiring API keys will be skipped if the corresponding environment variable is not set.

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\\Scripts\\activate   # Windows
```

2. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

### API Keys

Required environment variables:
```bash
# OpenAI API
export OPENAI_API_KEY="your-key-here"

# Anthropic API (Claude)
export ANTHROPIC_API_KEY="your-key-here"

# Alternative: Use .env file
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
```

### Dependencies

Core test dependencies:
- pytest>=7.0.0
- pytest-cov>=4.0.0
- pytest-xdist>=3.0.0
- pytest-timeout>=2.0.0

## Configuration

### pytest.ini Settings

```ini
[pytest]
# Test Discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output Configuration
addopts =
    --tb=short        # Short traceback
    --quiet          # Minimal output
    --no-header      # No pytest header
    --disable-warnings
    -ra              # Report all except passed

# Logging Configuration
log_cli = true
log_cli_level = ERROR
log_cli_format = %(levelname)-8s %(name)s: %(message)s
log_file = tests/test.log
log_file_level = DEBUG
log_file_format = %(asctime)s [%(levelname)8s] %(name)s: %(message)s (%(filename)s:%(lineno)s)
```

### Custom Markers

```python
# Register custom markers
def pytest_configure(config):
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "cli: CLI interface tests")
    config.addinivalue_line("markers", "openai: OpenAI API tests")
    config.addinivalue_line("markers", "claude: Claude API tests")
    config.addinivalue_line("markers", "ollama: Ollama model tests")
```

### Fixture Management

```python
# Session-wide fixtures
@pytest.fixture(scope="session")
def test_env():
    pass

# Function-level fixtures
@pytest.fixture
def mock_api():
    pass

# Parametrized fixtures
@pytest.fixture(params=["gpt4", "llama", "claude"])
def model_type(request):
    pass
```

## Writing Tests

### Test Structure

Follow this structure for test files:

```python
import pytest
from unittest.mock import Mock, patch
from pyvisionai import ClaudeVisionModel  # Add this import

class TestVisionModel:
    """Base class for vision model tests."""

    def setup_method(self):
        """Set up test fixtures."""
        pass

    def teardown_method(self):
        """Clean up after tests."""
        pass

class TestGPT4Vision(TestVisionModel):
    """Tests for GPT-4 Vision model."""

    @pytest.mark.skipif(
        "OPENAI_API_KEY" not in os.environ,
        reason="OpenAI API key not found"
    )
    def test_real_api_call(self):
        """Test with real API call."""
        pass

class TestClaudeVision(TestVisionModel):
    """Tests for Claude Vision model."""

    @pytest.mark.skipif(
        "ANTHROPIC_API_KEY" not in os.environ,
        reason="Anthropic API key not found"
    )
    def test_real_api_call(self):
        """Test with real API call."""
        pass

    def test_retry_logic(self):
        """Test retry logic for rate limits."""
        pass

    def test_error_handling(self):
        """Test error handling for various API responses."""
        pass

class TestLlamaVision(TestVisionModel):
    """Tests for local Llama model."""

    def test_local_model(self):
        """Test with local model."""
        pass
```

### Best Practices

1. Test Independence:
   ```python
   def test_independent():
       """Each test should be independent."""
       # Setup specific to this test
       # Test execution
       # Cleanup specific to this test
   ```

2. Clear Test Names:
   ```python
   def test_should_handle_empty_input():
       pass

   def test_should_raise_error_on_invalid_key():
       pass
   ```

3. Use Appropriate Assertions:
   ```python
   def test_assertions():
       assert isinstance(result, dict)
       assert len(result) > 0
       assert "key" in result
       assert result["value"] == expected
   ```

### Fixtures and Mocking

```python
# Test data fixtures
@pytest.fixture
def sample_image(tmp_path):
    image_path = tmp_path / "test.jpg"
    # Create test image
    return image_path

# API mocking
@pytest.fixture
def mock_openai():
    with patch("openai.ChatCompletion.create") as mock:
        mock.return_value = {"choices": [{"message": {"content": "test"}}]}
        yield mock
```

### Test Fixtures

Use fixtures for common setup:

```python
@pytest.fixture
def mock_claude_api():
    """Mock Claude Vision API responses."""
    with patch("anthropic.Anthropic") as mock:
        yield mock

@pytest.fixture
def mock_openai_api():
    """Mock OpenAI API responses."""
    with patch("openai.Client") as mock:
        yield mock

@pytest.fixture
def mock_ollama_api():
    """Mock Ollama API responses."""
    with patch("ollama.Client") as mock:
        yield mock
```

### Mocking External Services

Example of mocking API calls:

```python
def test_claude_vision_description(mock_claude_api):
    """Test Claude Vision image description."""
    mock_response = {
        "content": [{"text": "A detailed description of the image"}]
    }
    mock_claude_api.return_value.messages.create.return_value = mock_response

    model = ClaudeVisionModel(api_key="test_key")
    result = model.describe_image("test.jpg")
    assert "detailed description" in result

def test_claude_rate_limit_retry(mock_claude_api):
    """Test retry logic for rate limits."""
    mock_claude_api.return_value.messages.create.side_effect = [
        anthropic.RateLimitError("Rate limit exceeded"),
        {"content": [{"text": "Success after retry"}]}
    ]

    model = ClaudeVisionModel(api_key="test_key")
    result = model.describe_image("test.jpg")
    assert "Success" in result
```

## Performance Testing

### Benchmark Tests

```
