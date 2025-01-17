# Contributing to PyVisionAI

Thank you for your interest in contributing to PyVisionAI! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MDGrey33/pyvisionai.git
   cd pyvisionai
   ```

2. **Set up Python environment**
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

3. **Install system dependencies**
   ```bash
   # macOS
   brew install --cask libreoffice
   brew install poppler

   # Ubuntu/Debian
   sudo apt-get install -y libreoffice poppler-utils

   # Windows
   # Install LibreOffice and Poppler manually
   ```

4. **Install development tools**
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

1. **Running tests**
   ```bash
   # Run all tests
   poetry run pytest

   # Run with coverage
   poetry run pytest --cov=pyvisionai

   # Run specific test file
   poetry run pytest tests/test_specific.py
   ```

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
