./#!/bin/bash

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "Creating new virtual environment..."
    python3 -m venv env
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate

# Install dependencies
echo "Installing required packages..."
pip install PyPDF2 PyMuPDF Pillow

echo "Setup complete! Virtual environment is activated and dependencies are installed."
echo "You can now run the extract_content.py script." 