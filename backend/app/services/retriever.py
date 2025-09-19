import numpy as np
from backend.app.db.mongodb import get_all_chunks_embeddings
from backend.app.services.embedder import embed_text
from backend.app.config import settings

def cosine_similarity(a: np.ndarray, b:np.ndarray):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10) 

def retrieve(question: str, top_k: int = None):
    if top_k is None:
        top_k = settings.TOP_K
    q_emb = embed_text(question, task_type="retrieval_query")

    entries = get_all_chunks_embeddings()
    scores = []

    for e in entries:
        stored_emb = np.array(e["embedding"])
        score = cosine_similarity(np.array(q_emb), stored_emb)
        scores.append((score,e))

    top = sorted(scores, key=lambda x:x[0],  reverse=True)[:top_k]  

    return [(e, float(score)) for score, e in top] 


