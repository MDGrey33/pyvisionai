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
        "poetry", "run", "python", "describe_image_cli.py",
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
    assert "Description:" in result.stdout, "No description found in output"
    assert len(result.stdout) > 100, "Description seems too short"


def test_cli_image_description_gpt3():
    """Test image description using OpenAI GPT-3.5 model."""
    # Skip if no API key is provided
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\nSkipping GPT-3 test - No API key provided")
        return
        
    test_image = os.path.join("content", "test", "source", "test.jpeg")
    
    # Run the CLI command with GPT-3 model
    cmd = [
        "poetry", "run", "python", "describe_image_cli.py",
        "-i", test_image,
        "-u", "gpt3",  # Use gpt3 use case which uses gpt-3.5-turbo
        "--api-key", api_key,
        "-v"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output for debugging
    print("\nGPT-3 Model Output:")
    print(result.stdout)
    if result.stderr:
        print("Stderr:", result.stderr)
    
    # Check if the command was successful
    assert result.returncode == 0, f"CLI command failed with error: {result.stderr}"
    assert "Description:" in result.stdout, "No description found in output"
    assert len(result.stdout) > 100, "Description seems too short" 