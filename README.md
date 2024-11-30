# Content Extractor with Vision LLM

This repository contains a Python project that extracts text and images from various file types (PDF, DOCX, PPTX), describes the images using the `llama3.2-vision` model, and saves the results in a specified output directory.

## Features

- Extract text and images from PDF, DOCX, and PPTX files
- Describe images using the `llama3.2-vision` model
- Save extracted text and image descriptions in a specified output directory
- User-friendly command-line interface for specifying input and output folders
- Modular and extensible code structure following SOLID principles

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

## Project Structure

- `main.py`: The main script that orchestrates the file processing and user input.
- `extract_pdf.py`: Module for extracting text and images from PDF files.
- `extract_docx.py`: Module for extracting text and images from DOCX files.
- `extract_pptx.py`: Module for extracting text and images from PPTX files.
- `describe_image.py`: Module for describing images using the `llama3.2-vision` model.
- `pyproject.toml`: Poetry configuration file specifying project dependencies.
- `.gitignore`: File specifying patterns for files and directories to be ignored by Git.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
