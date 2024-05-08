import requests
from dotenv import load_dotenv
import os

class AiDevsTask:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('AI_DEVS_API_KEY')
        self.token = None
    
    def get_token(self, task_name):
        auth_url = f"https://tasks.aidevs.pl/token/{task_name.lower()}"
        auth_payload = {"apikey": self.api_key}
        auth_response = requests.post(auth_url, json=auth_payload)
        self.token = auth_response.json().get("token")
        print(f"Token: {self.token}")
    
    def get_task_content(self):
        if self.token:
            task_url = f"https://tasks.aidevs.pl/task/{self.token}"
            task_response = requests.get(task_url)
            if task_response.status_code == 200:
                task_content = task_response.json()
                print("Treść zadania: ", task_content)
                return task_content
            else:
                print("Błąd podczas pobierania treści zadania:", task_response.status_code)
        else:
            print("Token nie został pobrany.")
        return None
    
    def send_answer(self, answer):
        answer_payload = {"answer": answer} 
        print("Odpowiedź:", answer_payload)
        answer_url = f"https://tasks.aidevs.pl/answer/{self.token}"
        answer_response = requests.post(answer_url, json=answer_payload)
        print("Odpowiedź serwera: ", answer_response.json())
        return answer_response.json()
        
    def send_question(self, question):
        if self.token:
            question_payload = {"question": question}
            print("Pytanie:", question_payload)
            task_url = f"https://tasks.aidevs.pl/task/{self.token}"
            question_response = requests.post(task_url, data=question_payload)
            if question_response.status_code == 200:
                question_content = question_response.json()
                print("Odpowiedź na pytanie: ", question_content)
                return question_content
            else:
                print("Błąd podczas pobierania odpowiedzi:", task_response.status_code)
        else:
            print("Token nie został pobrany.")
        return None
