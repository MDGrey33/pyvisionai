# content extractor with vision llm
Repo to prepare different type of files for LLM usage.
Example: extract text and images from PDFs, describe the images using the `llama3.2-vision` model, and save the results in a specified output directory.



# PDF Image and Text Extractor

This project extracts text and images from PDF files, describes the images using the `llama3.2-vision` model, and saves the results in a specified output directory.

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

1. **Prepare PDF Files**

   Place your PDF files in the `./content/source` directory.

2. **Run the PDF Processing Script**

   Execute the following command to process the PDFs:

   ```bash
   poetry run python pdf.py
   ```

3. **Check the Output**

   The extracted text and images will be saved in the `./content/extracted` directory.

## Notes

- Ensure the Ollama server is running before executing the script.
- The `llama3.2-vision` model is used to describe images extracted from the PDFs.