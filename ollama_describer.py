import ollama

class OllamaDescriber:
    def describe(self, image_path: str) -> str:
        """Send an image to the ollama model and return the description."""
        try:
            # Send the image to the model
            response = ollama.chat(
                model="llama3.2-vision",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Describe this image factually in extreme detail, less information is better "
                            "than uncertain information, do not say anything unless sure, I do not see and I count on you."
                        ),
                        "images": [image_path],
                    }
                ],
            )
            # Return the description
            return response["message"]["content"]

        except Exception as e:
            raise RuntimeError(f"Error generating description with ollama: {str(e)}") 