from fastapi import FastAPI, File, UploadFile,HTTPException
from backend.app.services.pdf_processor import extract_text_from_pdf, chunk_text
from backend.app.services.embedder import embed_many
from backend.app.db.mongodb import insert_chunk,insert_document
from backend.app.services.qa_chaining import answer_question
from uuid import uuid4

app = FastAPI(title="Production Ready Ai ChatBot", description="A AI Chatbot which can be used to interact with with ur documents")

@app.post("/upload_pdf/")
async def upload_def(file: UploadFile = File(...)):
    content = await file.read()

    doc_id = str(uuid4())
    pages = extract_text_from_pdf(content)
    if not pages:
        raise HTTPException(status_code=400, detail="No text found in pdf")
    chunks=chunk_text(pages)

    texts = [c["text"] for c in chunks]
    embeddings = embed_many(texts, task_type="retrieval_document")

    insert_document(doc_id,{"filename":file.filename})
    for c,emb in zip(chunks, embeddings):
        insert_chunk(doc_id, c["chunk_id"], c["text"],c["pages"],emb)
    return {
        "doc_id": doc_id,
        "num_chunks":len(chunks)
    }

@app.post("/ask/")
async def ask(question: str):
    return answer_question(question)

@app.get("/health")
async def health():
    return {"status":"ok"}