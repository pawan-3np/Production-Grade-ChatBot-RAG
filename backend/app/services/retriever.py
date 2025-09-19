import numpy as np
from backend.app.db.mongodb import get_all_chunks_embeddings
from backend.app.services.embedder import embed_text
from backend.app.config import settings

def cosine_similarity(a: np.ndarray, b:np.ndarray):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10) 