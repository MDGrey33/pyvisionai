# PyVisionAI Examples

This directory contains practical examples demonstrating various use cases of PyVisionAI. Each example is self-contained and includes detailed comments explaining the code.

## Examples List

1. `basic_extraction.py` - Simple examples of extracting content from different file types
2. `batch_processing.py` - Process multiple files in parallel with progress tracking
3. `custom_prompts.py` - Examples of using custom prompts for different document types
4. `web_scraping.py` - Extract content from web pages and dynamic websites
5. `privacy_focused.py` - Using local Llama model for private document processing
6. `output_customization.py` - Customize the output format and organization
7. `error_handling.py` - Proper error handling and logging examples
8. `memory_optimization.py` - Techniques for processing large documents efficiently

## Running the Examples

1. Install dependencies:
   ```bash
   pip install pyvisionai
   ```

2. Set up your environment variables:
   ```bash
   export OPENAI_API_KEY='your-api-key'  # For OpenAI examples
   ```

3. Run any example:
   ```bash
   python examples/basic_extraction.py
   ```

## Example Data

The `example_data/` directory contains sample files for testing:
- PDF documents
- Word documents
- PowerPoint presentations
- HTML files
- Images

## Contributing

Feel free to add your own examples! Please follow these guidelines:
1. Include detailed comments
2. Handle errors appropriately
3. Follow the existing naming convention
4. Update this README with your example 