# PyVisionAI
# Content Extractor and Image Description with Vision LLM

Extract and describe content from documents using Vision Language Models.

## Repository

https://github.com/MDGrey33/pyvisionai

## Requirements

- Python 3.8 or higher
- Operating system: Windows, macOS, or Linux
- Disk space: At least 1GB free space (more if using local Llama model)

## Features

- Extract text and images from PDF, DOCX, PPTX, and HTML files
- Capture interactive HTML pages as images with full rendering
- Describe images using:
  - Cloud-based models (OpenAI GPT-4 Vision, Anthropic Claude Vision)
  - Local models (Ollama's Llama Vision)
- Save extracted text and image descriptions in markdown format
- Support for both CLI and library usage
- Multiple extraction methods for different use cases
- Detailed logging with timestamps for all operations
- Customizable image description prompts

## Installation

For macOS users, you can install using Homebrew:
```bash
brew tap mdgrey33/pyvisionai
brew install pyvisionai
```
For more details and configuration options, see the [Homebrew tap repository](https://github.com/roland/homebrew-pyvisionai).

1. **Install System Dependencies**
   ```bash
   # macOS (using Homebrew)
   brew install --cask libreoffice  # Required for DOCX/PPTX processing
   brew install poppler             # Required for PDF processing
   pip install playwright          # Required for HTML processing
   playwright install              # Install browser dependencies

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y libreoffice  # Required for DOCX/PPTX processing
   sudo apt-get install -y poppler-utils # Required for PDF processing
   pip install playwright               # Required for HTML processing
   playwright install                   # Install browser dependencies

   # Windows
   # Download and install:
   # - LibreOffice: https://www.libreoffice.org/download/download/
   # - Poppler: http://blog.alivate.com.au/poppler-windows/
   # Add poppler's bin directory to your system PATH
   pip install playwright
   playwright install
   ```

2. **Install PyVisionAI**
   ```bash
   # Using pip
   pip install pyvisionai

   # Using poetry (will automatically install playwright as a dependency)
   poetry add pyvisionai
   poetry run playwright install  # Install browser dependencies
   ```

## Directory Structure

By default, PyVisionAI uses the following directory structure:
```
content/
├── source/      # Default input directory for files to process
├── extracted/   # Default output directory for processed files
└── log/         # Directory for log files and benchmarks
```

These directories are created automatically when needed, but you can:
1. Create them manually:
   ```bash
   mkdir -p content/source content/extracted content/log
   ```
2. Override them with custom paths:
   ```bash
   # Specify custom input and output directories
   file-extract -t pdf -s /path/to/inputs -o /path/to/outputs

   # Process a single file with custom output
   file-extract -t pdf -s ~/documents/file.pdf -o ~/results
   ```

Note: While the default directories provide a organized structure, you're free to use any directory layout that suits your needs by specifying custom paths with the `-s` (source) and `-o` (output) options.

## Setup for Image Description

For cloud image description (default, recommended):
```bash
# Set OpenAI API key (for GPT-4 Vision)
export OPENAI_API_KEY='your-openai-key'

# Or set Anthropic API key (for Claude Vision)
export ANTHROPIC_API_KEY='your-anthropic-key'
```

For local image description (optional):
```bash
# Install Ollama
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download/windows

# Start Ollama server
ollama serve

# Pull the required model
ollama pull llama3.2-vision

# Verify installation
ollama list  # Should show llama3.2-vision
curl http://localhost:11434/api/tags  # Should return JSON response
```

Note: The local Llama model:
- Runs entirely on your machine
- No API key required
- Requires about 8GB of disk space
- Needs 16GB+ RAM for optimal performance
- May be slower than cloud models but offers privacy

## Features

- Extract text and images from PDF, DOCX, PPTX, and HTML files
- Capture interactive HTML pages as images with full rendering
- Describe images using:
  - Cloud-based models (OpenAI GPT-4 Vision, Anthropic Claude Vision)
  - Local models (Ollama's Llama Vision)
- Save extracted text and image descriptions in markdown format
- Support for both CLI and library usage
- Multiple extraction methods for different use cases
- Detailed logging with timestamps for all operations

## Usage

### Command Line Interface

1. **Extract Content from Files**
   ```bash
   # Process a single file (using default page-as-image method)
   file-extract -t pdf -s path/to/file.pdf -o output_dir
   file-extract -t docx -s path/to/file.docx -o output_dir
   file-extract -t pptx -s path/to/file.pptx -o output_dir
   file-extract -t html -s path/to/file.html -o output_dir

   # Process with specific model
   file-extract -t pdf -s input.pdf -o output_dir -m claude
   file-extract -t pdf -s input.pdf -o output_dir -m gpt4
   file-extract -t pdf -s input.pdf -o output_dir -m llama

   # Process with specific extractor
   file-extract -t pdf -s input.pdf -o output_dir -e text_and_images

   # Process all files in a directory
   file-extract -t pdf -s input_dir -o output_dir

   # Example with custom prompt
   file-extract -t pdf -s document.pdf -o output_dir -p "Extract the exact text as present in the image and write one sentence about each visual in the image"
   ```

   **Note:** The custom prompt for file extraction will affect the content of the output document. In case of page_as_image It should contain instructions to extract text and describe visuals. Variations are acceptable as long as they encompass these tasks. Avoid prompts like "What's the color of this picture?" as they may not yield the desired results.

2. **Describe Images**
   ```bash
   # Using GPT-4 Vision (default)
   describe-image -i path/to/image.jpg

   # Using Claude Vision (with --model parameter)
   describe-image -i path/to/image.jpg -m claude -k your-anthropic-key

   # Using local Llama model (with --model parameter)
   describe-image -i path/to/image.jpg -m llama

   # Using custom prompt
   describe-image -i image.jpg -p "List the main colors in this image"

   # Using legacy --use-case parameter (deprecated, use --model instead)
   describe-image -i path/to/image.jpg -u claude -k your-anthropic-key

   # Additional options
   describe-image -i image.jpg -v  # Verbose output
   ```

   **Note:** The `-u/--use-case` parameter is deprecated but maintained for backward compatibility. Please use `-m/--model` instead.

### Library Usage

```python
from pyvisionai import (
    create_extractor,
    describe_image_openai,
    describe_image_claude,
    describe_image_ollama
)

# 1. Extract content from files
# Using GPT-4 Vision (default)
extractor = create_extractor("pdf")
output_path = extractor.extract("input.pdf", "output_dir")

# Using Claude Vision
extractor = create_extractor("pdf", model="claude")
output_path = extractor.extract("input.pdf", "output_dir")

# Using specific extraction method
extractor = create_extractor("pdf", extractor_type="text_and_images")
output_path = extractor.extract("input.pdf", "output_dir")

# 2. Describe images
# Using GPT-4 Vision
description = describe_image_openai(
    "image.jpg",
    model="gpt-4o-mini",  # default
    api_key="your-openai-key",  # optional if set in environment
    max_tokens=300,  # default
    prompt="Describe this image focusing on colors and textures"  # optional
)

# Using Claude Vision
description = describe_image_claude(
    "image.jpg",
    api_key="your-anthropic-key",  # optional if set in environment
    prompt="Describe this image focusing on colors and textures"  # optional
)

# Using local Llama model
description = describe_image_ollama(
    "image.jpg",
    model="llama3.2-vision",  # default
    prompt="List the main objects in this image"  # optional
)
```

## Logging

The application maintains detailed logs of all operations:
- By default, logs are stored in `content/log/` with timestamp-based filenames
- Each run creates a new log file: `pyvisionai_YYYYMMDD_HHMMSS.log`
- Logs include:
  - Timestamp for each operation
  - Processing steps and their status
  - Error messages and warnings
  - Extraction method used
  - Input and output file paths

## Environment Variables

```bash
# Required for OpenAI Vision (if using GPT-4)
export OPENAI_API_KEY='your-openai-key'

# Required for Claude Vision (if using Claude)
export ANTHROPIC_API_KEY='your-anthropic-key'

# Optional: Ollama host (if using local description)
export OLLAMA_HOST='http://localhost:11434'
```

## Performance Optimization

1. **Memory Management**
   - Use `text_and_images` method for large documents
   - Process files in smaller batches
   - Monitor memory usage during batch processing
   - Clean up temporary files regularly

2. **Processing Speed**
   - Cloud models (GPT-4, Claude) are generally faster than local models
   - Use parallel processing for batch operations
   - Consider SSD storage for better I/O performance
   - Optimize image sizes before processing

3. **API Usage**
   - Implement proper rate limiting
   - Use appropriate retry mechanisms
   - Cache results when possible
   - Monitor API quotas and usage

## License

This project is licensed under the [Apache License 2.0](LICENSE).

## Command Parameters

### `file-extract` Command
```bash
file-extract [-h] -t TYPE -s SOURCE -o OUTPUT [-e EXTRACTOR] [-m MODEL] [-k API_KEY] [-v]

Required Arguments:
  -t, --type TYPE         File type to process (pdf, docx, pptx, html)
  -s, --source SOURCE     Source file or directory path
  -o, --output OUTPUT     Output directory path

Optional Arguments:
  -h, --help             Show help message and exit
  -e, --extractor TYPE   Extraction method:
                         - page_as_image: Convert pages to images (default)
                         - text_and_images: Extract text and images separately
                         Note: HTML only supports page_as_image
  -m, --model MODEL      Vision model for image description:
                         - gpt4: GPT-4 Vision (default)
                         - claude: Claude Vision
                         - llama: Local Llama model
  -k, --api-key KEY      API key (required for GPT-4 and Claude)
  -v, --verbose          Enable verbose logging
  -p, --prompt TEXT      Custom prompt for image description
```

### `describe-image` Command
```bash
describe-image [-h] -s SOURCE [-m MODEL] [-k API_KEY] [-v] [-p PROMPT]

Required Arguments:
  -s, --source SOURCE   Path to the image file to describe

Optional Arguments:
  -h, --help            Show help message and exit
  -m, --model MODEL     Model to use for description:
                        - gpt4: GPT-4 Vision (default)
                        - claude: Claude Vision
                        - llama: Local Llama model
  -k, --api-key KEY     API key (required for GPT-4 and Claude)
  -v, --verbose         Enable verbose logging
  -p, --prompt TEXT     Custom prompt for image description

Note: For backward compatibility, you can also use -i/--image instead of -s/--source.
      The -u/--use-case parameter is deprecated. Please use -m/--model instead.
```

### File Extraction Examples
```bash
# Basic usage with defaults (page_as_image method, GPT-4 Vision)
file-extract -t pdf -s document.pdf -o output_dir
file-extract -t html -s webpage.html -o output_dir  # HTML always uses page_as_image

# Specify extraction method (not applicable for HTML)
file-extract -t docx -s document.docx -o output_dir -e text_and_images

# Use local Llama model for image description
file-extract -t pptx -s slides.pptx -o output_dir -m llama

# Process all PDFs in a directory with verbose logging
file-extract -t pdf -s input_dir -o output_dir -v

# Use custom OpenAI API key
file-extract -t pdf -s document.pdf -o output_dir -k "your-api-key"

# Use custom prompt for image descriptions
file-extract -t pdf -s document.pdf -o output_dir -p "Focus on text content and layout"
```

### Image Description Examples
```bash
# Basic usage with defaults (GPT-4 Vision)
describe-image -s photo.jpg
describe-image -i photo.jpg  # Legacy parameter, still supported

# Using specific models
describe-image -s photo.jpg -m claude -k your-anthropic-key
describe-image -s photo.jpg -m llama
describe-image -i photo.jpg -m gpt4  # Legacy parameter style

# Using custom prompt
describe-image -s photo.jpg -p "List the main colors and their proportions"

# Customize token limit
describe-image -s photo.jpg -t 500

# Enable verbose logging
describe-image -s photo.jpg -v

# Use custom OpenAI API key
describe-image -s photo.jpg -k "your-api-key"

# Combine options
describe-image -s photo.jpg -m llama -p "Describe the lighting and shadows" -v
```

## Custom Prompts

PyVisionAI supports custom prompts for both file extraction and image description. Custom prompts allow you to control how content is extracted and described.

### Using Custom Prompts

1. **CLI Usage**
   ```bash
   # File extraction with custom prompt
   file-extract -t pdf -s document.pdf -o output_dir -p "Extract all text verbatim and describe any diagrams or images in detail"

   # Image description with custom prompt
   describe-image -i image.jpg -p "List the main colors and describe the layout of elements"
   ```

2. **Library Usage**
   ```python
   # File extraction with custom prompt
   extractor = create_extractor(
       "pdf",
       extractor_type="page_as_image",
       prompt="Extract all text exactly as it appears and provide detailed descriptions of any charts or diagrams"
   )
   output_path = extractor.extract("input.pdf", "output_dir")

   # Image description with custom prompt
   description = describe_image_openai(
       "image.jpg",
       prompt="Focus on spatial relationships between objects and any text content"
   )
   ```

3. **Environment Variable**
   ```bash
   # Set default prompt via environment variable
   export FILE_EXTRACTOR_PROMPT="Extract text and describe visual elements with emphasis on layout"
   ```

### Writing Effective Prompts

1. **For Page-as-Image Method**
   - Include instructions for both text extraction and visual description since the entire page is processed as an image
   - Example: "Extract the exact text as it appears on the page and describe any images, diagrams, or visual elements in detail"

2. **For Text-and-Images Method**
   - Focus only on image description since text is extracted separately
   - The model only sees the images, not the text content
   - Example: "Describe the visual content, focusing on what the image represents and any visual elements it contains"

3. **For Image Description**
   - Be specific about what aspects to focus on
   - Example: "Describe the main elements, their arrangement, and any text visible in the image"

Note: For page-as-image method, prompts must include both text extraction and visual description instructions as the entire page is processed as an image. For text-and-images method, prompts should focus solely on image description as text is handled separately.

## Contributing

We welcome contributions to PyVisionAI! Whether you're fixing bugs, improving documentation, or proposing new features, your help is appreciated.

Please read our [Contributing Guidelines](CONTRIBUTING.md) for detailed information on:
- Setting up your development environment
- Code style and standards
- Testing requirements
- Pull request process
- Documentation guidelines

### Quick Start for Contributors

1. Fork and clone the repository
2. Install development dependencies:
   ```bash
   pip install poetry
   poetry install
   ```
3. Install pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```
4. Make your changes
5. Run tests:
   ```bash
   poetry run pytest
   ```
6. Submit a pull request

For more detailed instructions, see [CONTRIBUTING.md](CONTRIBUTING.md).
