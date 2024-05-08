from utils import AiDevsTask, OpenAIChat, Downloader
import json
import os
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

class ContextCompressor:
    def __init__(self):
        self.chatbot = OpenAIChat()
        self.downloader = Downloader()
        
    def Compress(self, file_name, new_file_name):
        print("Compressing file:", file_name)

        context_object = self.ReadFile(file_name)
        if context_object is None:
            print("File not found:", file_name)
            return None
        else:
            new_dict = {}
            for key, value in context_object.items():
                print(key, ":", len(context_object[key]))
                messages=[
                    HumanMessage(content=f"""Compress this list of facts, keep all information, do not lose any detail: {context_object[key]}. 
                                Return that and only that. 
                                Response format should be JSON list of strings.
                            """),
                ]
                new_dict[key] = json.loads(self.chatbot.handle_messages(messages))
                
            self.SaveFile(new_file_name, new_dict)
            return new_dict
        
    def ReadFile(self, file_name):
        print("Reading file:", file_name)
        json_dict = None
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                json_dict = json.load(file)
        return json_dict
    
    def SaveFile(self, file_name, json_dict):
        print("Saving file:", file_name)
        with open(file_name, "w") as file:
            json.dump(json_dict, file)