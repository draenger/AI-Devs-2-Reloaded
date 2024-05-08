import requests
import os

class RenderForm:
    def __init__(self):
        self.api_key = os.getenv("RENDER_FORM_API_KEY")
        self.url = 'https://get.renderform.io/api/v2/render'
        self.headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

    def render(self, template_id, caption_text, image_src):
        payload = {
            'template': template_id,
            'data': {
                'caption.text': caption_text,
                'image.src': image_src
            }
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.json()