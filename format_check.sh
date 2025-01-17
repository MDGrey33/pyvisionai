#!/bin/bash

# Function to print colored output
green() { echo -e "\033[32m$1\033[0m"; }
red() { echo -e "\033[31m$1\033[0m"; }

# Run black
echo "Running black..."
if black ./examples ./pyvisionai ./tests; then
    green "✓ Black formatting successful"
else
    red "✗ Black formatting had errors"
    exit 1
fi

# Run isort
echo -e "\nRunning isort..."
if isort ./examples ./pyvisionai ./tests; then
    green "✓ Import sorting successful"
else
    red "✗ Import sorting had errors"
    exit 1
fi

# Run flake8 with explicit ignore flags
echo -e "\nRunning flake8 (critical issues only)..."
if flake8 ./examples ./pyvisionai ./tests --ignore=E501,F401,F841,W503,E226,E128,F403,F405,E402,E731,F541 --select=E9,F63,F7,F82,E722; then
    green "✓ No critical issues found"
else
    red "✗ Critical issues were found"
    exit 1
fi

green "\n✓ All checks passed!"
