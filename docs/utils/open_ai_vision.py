import base64
import requests
import os

class OpenAIVision:
    def __init__(self, model = "gpt-4-turbo"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

    def execute_local(self, query, image_path):
        base64_image = self.encode_image(image_path)
        image = f"data:image/jpeg;base64,{base64_image}"
        return self._execute(query, image)

    def execute_url(self, query, image_url):
        return self._execute(query, image_url)

    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _execute(self, query, image):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": f"{self.model}",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{query}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        print(payload)

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        return response.json()
