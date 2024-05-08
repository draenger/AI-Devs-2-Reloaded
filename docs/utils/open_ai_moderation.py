import requests
from dotenv import load_dotenv
import os
       
class OpenAIModeration:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        
    def moderate_text(self, text):
        moderation_url = "https://api.openai.com/v1/moderations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "input": text,  # Tekst do moderacji
            "model": "text-moderation-latest"  # Określenie najnowszego modelu do moderacji
        }
        response = requests.post(moderation_url, headers=headers, json=payload)
        if response.status_code == 200:
            moderation_result = response.json()
            return moderation_result  # Zwróć cały wynik moderacji
        else:
            return None
        
    def get_flagged_value_zero_or_one(self, moderation_result):
        if moderation_result is not None:
            formated_response = moderation_result['results'][0]['flagged']
            print(formated_response)
            if formated_response == True:
                return 1
            elif formated_response == False:
                return 0
        else:
            return None
        
    def moderate_inputs(self, inputs):
        result_array = []
        for input_text in inputs:
            result = self.moderate_text(input_text)
            zero_or_one = self.get_flagged_value_zero_or_one(result)
            result_array.append(zero_or_one)
        return result_array
