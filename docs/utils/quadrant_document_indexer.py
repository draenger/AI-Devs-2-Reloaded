import os
import uuid
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import json

class QuadrantDocumentIndexer:
    def __init__(self, memory_path, collection_name):
        self.memory_path = memory_path
        self.collection_name = collection_name
        self.qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))
        print(f"Qdrant URL: {os.getenv('QDRANT_URL')}")
        self.embeddings = OpenAIEmbeddings(model = "text-embedding-ada-002")
    
    def create_collection(self): 
        try:
            collection_info = self.qdrant.get_collection(collection_name=self.collection_name)
            print("Collection already exists.")
            return
        except Exception:
            self.qdrant.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE, on_disk=True),
                )
            print(f"Collection {self.collection_name} created.") 
        
    def index_documents(self):
        collection_info = self.qdrant.get_collection(collection_name=self.collection_name)
        if collection_info.vectors_count == 0:
            print("Indexing documents...")
            
            if os.path.exists('points.json'):
                with open('points.json', 'r') as file:
                    points_data = json.load(file)
                    points = []
                    for point_data in points_data:
                        point = PointStruct(
                            id=point_data['id'],
                            payload=point_data['payload'],
                            vector=point_data['vector']
                        )
                        points.append(point)
            else:
                points = []
                with open(self.memory_path, 'r') as file:
                    documents = json.load(file)
                    for document in documents:
                        metadata = {
                            "source": self.collection_name,
                            "title": document["title"],
                            "info": document["info"],
                            "url": document["url"],
                            "date": document["date"],
                            "uuid": str(uuid.uuid4())
                        }
                        embedding = self.embeddings.embed_documents([document["info"]])[0]
                        point = PointStruct(
                            id = metadata['uuid'],
                            payload = metadata,
                            vector = embedding,
                        )
                        points.append(point)
                try:
                    # Save points to JSON file
                    points_json = []
                    for point in points:
                        point_data = {
                            "id": point.id,
                            "payload": point.payload,
                            "vector": point.vector
                        }
                        points_json.append(point_data)

                    with open('points.json', 'w') as file:
                        json.dump(points_json, file)
                except Exception as e:
                    print(f"Error saving points to JSON file: {str(e)}")
    
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=True
            )

            print("Documents indexed.")
        else:
            print("Documents already indexed.")
    
    def search_document(self, query):
        query_embedding = self.embeddings.embed_query(query)
        search_result = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=1
        )
        return search_result
