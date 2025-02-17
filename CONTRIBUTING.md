# Contributing to PyVisionAI

Thank you for your interest in contributing to PyVisionAI! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MDGrey33/pyvisionai.git
   cd pyvisionai
   ```

2. **Set up environment variables and services**
   ```bash
   # For GPT-4 Vision development
   export OPENAI_API_KEY='your-openai-key'

   # For Claude Vision development
   export ANTHROPIC_API_KEY='your-anthropic-key'

   # For local Llama development
   export OLLAMA_HOST='http://localhost:11434'  # Optional, this is the default

   # Install and start Ollama (macOS)
   brew install ollama
   ollama serve &  # Run in background

   # Or install Ollama (Linux)
   curl -fsSL https://ollama.com/install.sh | sh
   ollama serve &  # Run in background

   # Pull required model for development
   ollama pull llama3.2-vision

   # Verify Ollama setup
   ollama list  # Should show llama3.2-vision
   curl http://localhost:11434/api/tags  # Should return JSON response
   ```

   Note: For Windows development, download Ollama from https://ollama.com/download/windows
   and run it as a service.

3. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows

   # Install dependencies for development
   pip install -e .
   pip install -r requirements-dev.txt
   ```

4. **Install system dependencies**
   ```bash
   # macOS
   brew install --cask libreoffice
   brew install poppler

   # Ubuntu/Debian
   sudo apt-get install -y libreoffice poppler-utils

   # Windows
   # Install LibreOffice and Poppler manually
   ```

5. **Install development tools**
   ```bash
   # Install pre-commit hooks
   pre-commit install
   ```

## Code Style

We use several tools to maintain code quality:

1. **Black** for code formatting
   - Line length: 72 characters
   - Target version: Python 3.12
   ```bash
   poetry run black .
   ```

2. **isort** for import sorting
   - Compatible with Black
   - Line length: 72 characters
   ```bash
   poetry run isort .
   ```

3. **Flake8** for style guide enforcement
   ```bash
   poetry run flake8
   ```

4. **pydocstyle** for docstring checking
   - Following Google style
   ```bash
   poetry run pydocstyle
   ```

## Testing

1. **Environment Setup**
   ```bash
   # Required for full test coverage
   export OPENAI_API_KEY='your-openai-key'
   export ANTHROPIC_API_KEY='your-anthropic-key'
   ```

2. **Running Tests**
   ```bash
   # Run all tests
   pytest

   # Run specific test categories
   pytest tests/test_extractors/  # Test extractors
   pytest tests/test_describers/  # Test vision models
   pytest tests/test_cli.py       # Test CLI interface

   # Run tests for specific models
   pytest -k "test_gpt4"         # Test GPT-4 Vision
   pytest -k "test_claude"       # Test Claude Vision
   pytest -k "test_llama"        # Test Llama Vision
   ```

   Note: Tests requiring API keys will be skipped if the corresponding environment variable is not set.

2. **Writing tests**
   - Place tests in the `tests/` directory
   - Match test file names with source files
   - Use descriptive test names
   - Include both success and failure cases
   - Mock external services appropriately

Example test:
```python
def test_pdf_extraction():
    """Test PDF content extraction."""
    extractor = create_extractor("pdf")
    result = extractor.extract("tests/data/sample.pdf", "tests/output")
    assert os.path.exists(result)
    assert result.endswith(".md")
```

## Pull Request Process

1. **Fork the repository**
   - Create a fork on GitHub
   - Clone your fork locally

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-fix-name
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add/update tests as needed
   - Update documentation if required

4. **Commit your changes**
   - Use meaningful commit messages
   - Follow conventional commits format:
     ```
     type(scope): description

     [optional body]

     [optional footer]
     ```
   - Types: feat, fix, docs, style, refactor, test, chore

5. **Push and create PR**
   ```bash
   git push origin your-branch-name
   ```
   Then:
   - Go to the repository on GitHub
   - Click "Pull Request"
   - Fill out the PR template completely
   - Link related issues
   - Request review from maintainers

6. **Review process**
   - Integration checks must pass
   - At least one maintainer review required
   - Address review comments
   - Keep PR focused and reasonable in size

## Documentation

When adding new features or making changes:

1. **Update API documentation**
   - Add/update docstrings
   - Update `docs/api.md` if needed

2. **Update examples**
   - Add example code in `examples/`
   - Update example documentation

3. **Update guides**
   - Update relevant sections in guides
   - Add new guides if needed

## Release Process

1. **Version bumping**
   ```bash
   poetry version patch  # or minor, or major
   ```

2. **Update CHANGELOG.md**
   - Add version section
   - List all changes
   - Credit contributors

3. **Create release PR**
   - Update version in pyproject.toml
   - Update documentation
   - Run all tests

## Getting Help

- Create an issue for bugs or features
- Join discussions in GitHub Discussions
- Tag maintainers in complex issues
- Check existing issues and PRs first

## Code of Conduct

Please note that PyVisionAI has a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## Development Guidelines

### Vision Model Integration

When implementing or modifying vision model support:

1. **Model Interface**
   - Implement the `BaseVisionModel` interface
   - Handle API key validation and configuration
   - Implement proper retry logic for API calls
   - Follow the established error handling patterns

2. **Testing**
   - Add comprehensive unit tests
   - Include API error simulation tests
   - Add integration tests with real API calls
   - Ensure tests can run without API keys (using skip markers)

3. **Documentation**
   - Update API documentation
   - Add usage examples
   - Document environment variables
   - Update CLI help messages

4. **Error Handling**
   - Use appropriate exception classes
   - Add descriptive error messages
   - Implement proper retry logic
   - Handle rate limits gracefully

### Model-Specific Guidelines

1. **GPT-4 Vision**
   - Follow OpenAI's best practices
   - Handle token limits appropriately
   - Implement proper error handling for API responses
   - Use appropriate model versions

2. **Claude Vision**
   - Follow Anthropic's guidelines
   - Handle API rate limits
   - Implement proper retry logic
   - Use appropriate model versions

3. **Llama Vision**
   - Handle local model availability
   - Implement proper error handling
   - Support custom model configurations
   - Handle resource constraints
