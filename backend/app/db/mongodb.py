from pymongo import MongoClient
from backend.app.config import settings

client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB]

docs_coll = db["documents"]
chunks_coll = db["chunks"]
chat_coll = db["chat_history"]

def insert_document(doc_id:str , metadata: dict):
    docs_coll.insert_one(
        {
            "_id":doc_id,
            **metadata
        }
    )
    
def insert_chunk(doc_id: str, chunk_id: int, text: str, pages: list[list[int]], embedding: list[float]):
    chunks_coll.insert_one(
        {
        "doc_id": doc_id,
        "chunk_id": chunk_id,
        "text": text,
        "pages": pages,
        "embedding": embedding
        }
    )
    
#def insert_chat_history():

def get_all_chunks_embeddings():
    results = list(chunks_coll.find({},{"embedding":1,"text":1,"pages":1,"doc_id":1}))
    return results
    