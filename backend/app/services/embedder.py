from google import genai
from google.genai import types
from backend.app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def embed_text(text: str, task_type: str = "retrieval_document") -> list[float]:
    """
    Returns embedding vector for a piece of text.
    task_type: retrieval_document or retrieval_query
    """
    resp = genai.Client().models.embed_content(
        model=settings.EMBEDDING_MODEL,
        contents=[text],
        config=types.EmbedContentConfig(output_dimensionality=settings.EMBEDDING_DIM,
                                         task_type=types.TaskType.RETRIEVAL_DOCUMENT if task_type == "retrieval_document" else types.TaskType.RETRIEVAL_QUERY)
    )
    embedding = resp.embeddings[0]  # assuming embeddings field
    return embedding.values  # or as list

def embed_many(texts: list[str], task_type: str = "retrieval_document") -> list[list[float]]:
    # batch embedding: break into batches, etc.
    embeddings = []
    for chunk in texts:
        emb = embed_text(chunk, task_type)
        embeddings.append(emb)
    return embeddings
