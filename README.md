# Content Extractor with Vision LLM

This repository contains a Python project that extracts text and images from various file types (PDF, DOCX, PPTX), describes the images using the `llama3.2-vision` model, and saves the results in a specified output directory.

## TODO
- Delete extracted images after processing.
- Implement a module to extract tabular data from documents and transform it into a narrative format for more meaningful LLM consumption.

## Features

- Extract text and images from PDF, DOCX, and PPTX files
- Describe images using the `llama3.2-vision` model
- Save extracted text and image descriptions in a specified output directory
- User-friendly command-line interface for specifying input and output folders
- Modular and extensible code structure following SOLID principles
- Compare image descriptions generated by different models

## Prerequisites

- Python 3.x
- Poetry
- Ollama

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Poetry**

   If you haven't installed Poetry yet, you can do so by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

3. **Install Project Dependencies**

   Use Poetry to install the dependencies:

   ```bash
   poetry install
   ```

## Setup Ollama

1. **Run Ollama Server**

   Start the Ollama server by running:

   ```bash
   ollama serve
   ```

2. **Pull the `llama3.2-vision` Model**

   Pull the required model by executing:

   ```bash
   ollama pull llama3.2-vision
   ```

## Configuration

The image description script can be configured using the `config.py` file. The available configuration options are:

- `DEFAULT_IMAGE_PATH`: The default path to the image file to be described.
- `DEFAULT_DESCRIBER`: The default describer to use for generating image descriptions. Available options are "openai" (OpenAI API) and "ollama" (local Ollama model).
- `DEFAULT_MODEL`: The default model to use for image description. The available options depend on the selected describer:
  - OpenAI describer: "gpt-4o" (default), "gpt-3.5-turbo"
  - Ollama describer: "llava", "llava:34b", "llama3.2-vision"

You can modify these configuration options in the `config.py` file to customize the script's behavior according to your requirements.

## Usage

1. **Run the Main Script**

   Execute the main script using Poetry:

   ```bash
   poetry run python main.py
   ```

2. **Provide Input**

   When prompted, enter the following information:
   - Source folder path (default: `./content/source`)
   - Output folder path (default: `./content/extracted`)
   - File type to process (pdf, docx, or pptx)

   The script will process the specified file type from the source folder and save the extracted text and image descriptions in the output folder.

### Examples

- Run the script with the default configuration:

  ```bash
  poetry run python main.py
  ```

- Run the script using the OpenAI describer with the "gpt-3.5-turbo" model:

  ```bash
  poetry run python main.py --describer openai --model gpt-3.5-turbo
  ```

- Run the script using the Ollama describer with the "llava:34b" model:

  ```bash
  poetry run python main.py --describer ollama --model llava:34b
  ```

## Compare Image Descriptions

The `describe_image_compare.py` script allows you to compare image descriptions generated by different models. It takes an image path as input and sends the image to multiple specified models to obtain their respective descriptions. The script then saves the results in a CSV file for easy comparison.

### Usage

1. Update the `image_path` variable in the `describe_image_compare.py` script with the path to the image you want to compare descriptions for.

2. Modify the `models` list in the script to include the models you want to compare. The available models are: "llava", "llava:34b", and "llama3.2-vision".

3. Run the script:

   ```bash
   poetry run python describe_image_compare.py
   ```

4. The script will process the image with each specified model and save the results in a CSV file. The default output path is `/Users/roland/image_descriptions.csv`. You can change this by updating the `output_csv` variable in the script.

The generated CSV file will have two columns: "model" and "description". Each row represents the description generated by a specific model for the given image.

## Project Structure

- `main.py`: The main script that orchestrates the file processing and user input.
- `extract_pdf.py`: Module for extracting text and images from PDF files.
- `extract_docx.py`: Module for extracting text and images from DOCX files.
- `extract_pptx.py`: Module for extracting text and images from PPTX files.
- `describe_image.py`: Module for describing images using the `llama3.2-vision` model.
- `describe_image_compare.py`: Script for comparing image descriptions generated by different models.
- `pyproject.toml`: Poetry configuration file specifying project dependencies.
- `.gitignore`: File specifying patterns for files and directories to be ignored by Git.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
