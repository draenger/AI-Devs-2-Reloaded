import os
from langchain_openai import OpenAIEmbeddings

class OpenAIEmbedding:
    def __init__(self, embedding_model = 'text-embedding-ada-002'):
        self.embed_model = OpenAIEmbeddings(model = embedding_model) 
    
    def embed_query(self, query: str):
        return self.embed_model.embed_query(query)
        
        
