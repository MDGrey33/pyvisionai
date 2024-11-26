import openai
import base64
import os

# Set your OpenAI API key
openai.api_key = ""

def describe_image(image_path):
    # Read the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Encode the image to base64
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Prepare the message with the image
    messages = [
        {"role": "system", "content": "You are an assistant that describes images in detail."},
        {"role": "user", "content": f"![image](data:image/png;base64,{base64_image})"}
    ]

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )

    # Extract and return the description
    return response.choices[0].message["content"]

# Example usage
if __name__ == "__main__":
    image_path = "the_image.png"  # Replace with your image path
    try:
        description = describe_image(image_path)
        print("Image Description:")
        print(description)
    except Exception as e:
        print(f"Error: {str(e)}")

