#!/bin/bash
# PyVisionAI Server Manager
# Simple wrapper for running PyVisionAI servers

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the Python script with all arguments
python "$SCRIPT_DIR/scripts/run_pyvisionai.py" "$@"
