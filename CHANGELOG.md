# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
