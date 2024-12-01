import ollama
import csv

def describe_image(image_path, model_name):
    """
    Sends an image to the specified model and returns the description.
    """
    try:
        # Send the image to the model
        response = ollama.chat(
            model=model_name,
            messages=[{
                "role": "user",
                "content": (
                    "Describe this image factually in extreme detail, less information is better "
                    "than uncertain information, do not say anything unless sure, I do not see and I count on you."
                ),
                "images": [image_path]
            }]
        )
        # Return the description
        return response["message"]["content"]

    except Exception as e:
        raise Exception(f"Error with model '{model_name}': {str(e)}")


if __name__ == "__main__":
    # Path to the image
    image_path = "/Users/roland/code/file_extractor/content/source/the_image.png"  # Replace with your image path
    
    # Models to test
    models = ["llava", "llava:34b", "llama3.2-vision"]
    
    # Output CSV file
    output_csv = "/Users/roland/image_descriptions.csv"  # Replace with desired output path
    
    # Initialize results list
    results = []

    # Iterate through models
    for model in models:
        try:
            print(f"Processing image with model: {model}")
            description = describe_image(image_path, model)
            results.append({"model": model, "description": description})
            print(f"Description from {model}: {description}")
        except Exception as e:
            print(f"Error processing with {model}: {e}")
            results.append({"model": model, "description": f"Error: {e}"})

    # Write results to CSV
    try:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["model", "description"])
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {output_csv}")
    except Exception as e:
        print(f"Error writing to CSV: {e}") 