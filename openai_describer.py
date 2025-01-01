import os
import openai
import base64
from typing import Optional


class OpenAIDescriber:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is required. Provide it as an argument or set it in the OPENAI_API_KEY environment variable."
            )
        openai.api_key = api_key
        self.client = openai.OpenAI()

    def describe(self, image_path: str, model: str = "gpt-4o") -> str:
        try:
            # Read and encode the image in base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe the image in extreme detail",
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}"
                                },
                            }
                        ],
                    },
                ],
                response_format={"type": "text"},
                temperature=1,
                max_completion_tokens=10000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Failed to generate description: {e}")
