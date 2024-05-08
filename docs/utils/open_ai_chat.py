import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

class OpenAIChat:
    def __init__(self, llm_model = 'gpt-3.5-turbo'):
        self.chat = ChatOpenAI(model = llm_model)
        self.messages = []
    
    def handle_query(self, prompt: HumanMessage):
        print(f"Prompt: {prompt.content}")
        self.messages.append(prompt) 
        response = self.chat(self.messages)
        self.messages.append(response)
        
        return response.content
    
    def handle_messages(self, messages: list):
        self.messages = messages
        response = self.chat(self.messages)
        return response.content