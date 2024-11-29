import os
import subprocess

def describe_image(image_path):
    # Define the prompt as input to be passed to the command
    prompt = f"Describe this image: {image_path}"

    try:
        # Use subprocess to pass input to the command via stdin
        result = subprocess.run(
            ["ollama", "run", "llava"],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )

        # Check if the output exists
        if result.stdout:
            return result.stdout
        else:
            raise Exception("No output from the command.")

    except subprocess.CalledProcessError as e:
        raise Exception(f"Command failed with return code {e.returncode}. Error output: {e.stderr}")

    except FileNotFoundError:
        raise Exception("Ollama is not installed or not found in PATH. Ensure it's installed and accessible.")

# Example usage
if __name__ == "__main__":
    image_path = "/Users/roland/code/file_extractor/the_image.png"  # Replace with your image path
    try:
        description = describe_image(image_path)
        print("Image Description:")
        print(description)
    except Exception as e:
        print(f"Error: {str(e)}")

