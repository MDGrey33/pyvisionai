"""
Basic integration test for image description CLI.
"""

import os
import subprocess


def test_cli_image_description_llama():
    """Test image description using local Llama model."""
    test_image = os.path.join("content", "test", "source", "test.jpeg")
    
    # Run the CLI command with Llama model
    cmd = [
        "poetry", "run", "describe-image",
        "-i", test_image,
        "-u", "llama",  # Use llama use case which uses llama3.2-vision
        "-v"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output for debugging
    print("\nLlama Model Output:")
    print(result.stdout)
    if result.stderr:
        print("Stderr:", result.stderr)
    
    # Check if the command was successful
    assert result.returncode == 0, f"CLI command failed with error: {result.stderr}"
    assert len(result.stdout) > 100, "Description seems too short"


def test_cli_image_description_gpt4():
    """Test image description using OpenAI GPT-4 Vision model."""
    # Skip if no API key is provided
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\nSkipping GPT-4 test - No API key provided")
        return
        
    test_image = os.path.join("content", "test", "source", "test.jpeg")
    
    # Run the CLI command with GPT-4 model
    cmd = [
        "poetry", "run", "describe-image",
        "-i", test_image,
        "-u", "gpt4",  # Use gpt4 use case which uses gpt-4-vision
        "-k", api_key,
        "-v"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output for debugging
    print("\nGPT-4 Model Output:")
    print(result.stdout)
    if result.stderr:
        print("Stderr:", result.stderr)
    
    # Check if the command was successful
    assert result.returncode == 0, f"CLI command failed with error: {result.stderr}"
    assert len(result.stdout) > 100, "Description seems too short" 