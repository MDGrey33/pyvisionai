"""
CLI tool for testing image description with different parameters.
"""

import argparse
import os
from describe_image import describe_image


# Available models for each service
OLLAMA_MODEL = "llama3.2-vision"
GPT4_MODEL = "gpt-4-vision-preview"
GPT3_MODEL = "gpt-3-vision"

# Three main use cases
USE_CASES = {
    "llama": {"describer": "ollama", "model": OLLAMA_MODEL},
    "gpt4": {"describer": "openai", "model": GPT4_MODEL},
    "gpt3": {"describer": "openai", "model": GPT3_MODEL}
}


def setup_parser():
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate descriptions for images using various models and settings."
    )
    
    parser.add_argument(
        "--image",
        "-i",
        type=str,
        required=True,
        help="Path to the image file to describe"
    )
    
    parser.add_argument(
        "--use",
        "-u",
        type=str,
        default="llama",
        choices=list(USE_CASES.keys()),
        help="Use case to run (default: llama). Options:\n"
             "llama: Ollama with llama3.2-vision (local)\n"
             "gpt4: OpenAI with GPT-4 Vision (requires API key)\n"
             "gpt3: OpenAI with GPT-3 Vision (requires API key)"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (required for gpt4 and gpt3)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Optional file to save the description to"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print additional information about the process"
    )
    
    return parser


def main():
    """Main entry point for the CLI tool."""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Validate image path
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        return 1
    
    # Get use case configuration
    use_case = USE_CASES[args.use]
    
    # Validate OpenAI API key if needed
    if use_case["describer"] == "openai" and not args.api_key:
        print(f"Error: OpenAI API key is required for {args.use}")
        return 1
    
    try:
        if args.verbose:
            print(f"Processing image: {args.image}")
            print(f"Using: {args.use}")
            print(f"Describer: {use_case['describer']}")
            print(f"Model: {use_case['model']}")
        
        # Generate description
        description = describe_image(
            image_path=args.image,
            model=use_case["model"],
            api_key=args.api_key,
            describer_choice=use_case["describer"]
        )
        
        # Output description
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(description)
            if args.verbose:
                print(f"Description saved to: {args.output}")
        else:
            print("\nDescription:")
            print("-" * 80)
            print(description)
            print("-" * 80)
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main()) 