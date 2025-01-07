# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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