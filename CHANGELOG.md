# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2024-03-25

### Added
- Added new `-m/--model` parameter to `describe-image` command for model selection
- Added comprehensive test coverage for CLI parameters:
  - Tests for both `-m/--model` and `-u/--use-case` parameters
  - Tests for parameter precedence
  - Tests for default model behavior
  - Tests for deprecation warnings

### Changed
- Updated CLI parameter handling to support both new and legacy model selection
- Enhanced help messages with clearer model descriptions
- Improved error messages and help text for CLI commands
- Updated documentation to reflect new CLI parameters
- Added friendly guidance message for `-u/--use-case` users to consider using `-m/--model`
- Enhanced parameter handling with proper precedence rules

### Note
- The `-u/--use-case` parameter continues to be fully supported for backward compatibility
- We recommend using `-m/--model` for better consistency across commands
- Both parameters will be maintained to ensure a stable user experience
- Users can choose either option based on their preference and existing scripts

## [0.3.0] - 2024-03-25

### Added
#### Claude Vision Integration
- Added `ClaudeVisionModel` class for Anthropic's Claude Vision API integration
- Implemented robust retry logic and error handling for Claude API calls
  - Added handling for rate limits and server errors
  - Added specific handling for API overload conditions (Error 529)
  - Implemented exponential backoff for retries
- Added support for custom prompts with Claude Vision
- Added `describe_image_claude` function to main API

#### Testing Framework
- Added Claude-specific test markers (`@pytest.mark.claude`)
- Added comprehensive test suite for Claude Vision model:
  - Unit tests for initialization, configuration, and error handling
  - Integration tests with real API calls
  - Rate limit and retry logic tests
  - Custom prompt handling tests
  - CLI interface tests

#### Documentation
- Added Claude Vision model documentation in `docs/getting_started.md`
- Updated API documentation with Claude Vision integration details
- Added environment setup instructions for Anthropic API key
- Enhanced testing documentation with Claude-specific examples
- Updated CLI help messages with Claude Vision options

#### Configuration
- Added `ANTHROPIC_API_KEY` environment variable support
- Added Claude Vision model configuration in factory system
- Added retry strategy configuration for API calls

### Enhanced
- Improved error handling with specific error types for API issues
- Enhanced retry logic for rate limits and server errors
- Updated model factory to support Claude Vision
- Improved test fixtures for better test isolation
- Enhanced documentation with more comprehensive examples

### Fixed
- Proper handling of empty responses from Claude API
- Correct error propagation for authentication issues
- Improved rate limit handling with exponential backoff

## [0.2.8] - 2024-01-31

### Added
- Added Homebrew support for easy installation:
  - Created Homebrew formula with all dependencies
  - Added support for both cloud (OpenAI) and local (Ollama) models
  - Automated installation of system dependencies (poppler, libreoffice)
  - Added post-installation verification and helpful setup instructions
  - Comprehensive documentation for Homebrew users

### Changed
- Improved installation process with better dependency management
- Enhanced system compatibility checks
- Updated documentation with Homebrew installation instructions

## [0.2.7] - 2024-03-22

### Added
- Added retry mechanism for handling transient failures:
  - Implemented RetryManager with configurable strategies
  - Added support for exponential, linear, and constant backoff
  - Added comprehensive logging for retry attempts
  - Added proper error handling and delay management


### Changed
- Improved error handling in model selection:
  - Enhanced connection error handling for API calls
  - Added graceful fallback when default model is unavailable
  - Improved error messages with detailed failure context
- Enhanced test coverage:
  - Added tests for retry mechanism with various strategies
  - Added tests for model fallback scenarios
  - Added mocked API tests for connection failures

### Fixed
- Fixed model selection to properly handle connection failures
- Fixed retry delays to prevent excessive wait times
- Fixed logging to capture all retry and fallback attempts

## [0.2.6] - 2024-01-25

### Added
- Implemented Model Factory pattern for vision models:
  - Added VisionModel base class with abstract methods
  - Added ModelFactory for centralized model management
  - Added concrete implementations for GPT4 and Llama models
  - Added comprehensive logging for model lifecycle
  - Added configuration validation for each model type

### Changed
- Refactored model initialization to use factory pattern
- Improved error handling in model creation and validation
- Standardized model interface across all implementations
- Enhanced logging with model-specific context

### Documentation
- Added docstrings for new model classes
- Updated logging documentation
- Added model factory usage examples

## [0.2.5] - 2024-01-21

### Added
- Implemented comprehensive logging across all extractors:
  - Added structured logging for PDF processing stages
  - Added progress tracking for DOCX file conversions and page processing
  - Added detailed logging for PPTX slide extraction and conversion
  - Added HTML processing status and element detection logging

### Changed
- Standardized logging patterns across all extractors:
  - Consistent start/completion messages
  - Clear error reporting with context
  - Progress indicators for multi-step operations
  - Performance metrics logging
- Replaced print statements with proper logger calls
- Added logging initialization in all core modules
- Standardized log message format and levels:
  - INFO for progress and success
  - WARNING for non-critical issues
  - ERROR for operation failures

### Improved
- Enhanced benchmark testing reliability:
  - Added self-contained benchmark test fixtures
  - Improved test independence from environment
  - Added comprehensive validation of benchmark metrics
  - Removed dependency on pre-existing log files
- Added performance metrics logging for both CLI and API interfaces

### Documentation
- Added logging configuration examples
- Updated docstrings with logging details
- Added benchmark metrics documentation

## [0.2.4] - 2024-03-21

### Changed
- Implemented parallel processing for DOCX text and images extraction
  - Added concurrent processing of paragraphs and images
  - Improved performance through ThreadPoolExecutor implementation
  - Maintained document structure and content order
  - Fixed image placement to ensure correct positioning within text
  - Added proper error handling and cleanup
  - Performance results: ~72% reduction in processing time (189s → 53s)

- Implemented parallel processing for DOCX page-as-image extraction
  - Added PageTask dataclass for encapsulating page processing data
  - Introduced process_page method for individual page handling
  - Modified extract method to use ThreadPoolExecutor with 4 workers
  - Maintained page order using indexed results collection

### Fixed
- Added docstring to PDF extractor explaining sequential processing decision
- Fixed test infrastructure to properly use poetry run in CLI tests

## [0.2.3] - 2024-03-20

### Changed
- Implemented parallel processing for PDF page-as-image extraction
  - Improved performance by ~68% (from 4 minutes to 1.3 minutes on a 27-page PDF)
  - Added ThreadPoolExecutor with 4 workers for concurrent page processing
  - Maintained page order while processing in parallel

## [0.2.2] - 2024-03-20

### Added
- Support for custom prompts in image description
- Added support for custom prompts in file extraction

## [0.2.1] - 2024-03-19

### Added
- Support for HTML file extraction using Playwright
- Capability to handle interactive HTML pages with JavaScript rendering
- HTML to image conversion for consistent extraction results
- Simplified the test suite with V2

## [0.2.0] - 2024-01-07

### Fixed
- Fixed PDF image extraction where images were being extracted as black ([#11](https://github.com/MDGrey33/pyvisionai/issues/11))
  - Added proper color space handling for ICC and other PDF color spaces
  - Implemented data decompression and size verification for image data
  - Added validation to detect and skip corrupted or completely black images
  - Improved error handling and logging for image extraction process

### Changed
- Improved image extraction reliability across all supported formats
- Enhanced error reporting during image processing
- Implemented parallel processing for image extraction and description to improve performance
- Updated documentation with more detailed command parameters
- Restructured README with comprehensive sections on CLI parameters and usage examples


## [0.1.1] - 2024-01-07

### Added
- Initial release with support for PDF, DOCX, and PPTX file processing
- Text and image extraction capabilities
- Image description using Vision LLMs
- Command-line interface for file extraction and image description
