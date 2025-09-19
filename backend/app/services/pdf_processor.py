import io
from typing import List,Dict
from pdfplumber import open as open_pdf

from backend.app.config import settings
import tiktoken

#returns list of dicts
def extract_text_from_pdf(pdf_bytes: bytes) -> List[Dict]:
    pages = []
    with open_pdf(io.BytesIO(pdf_bytes)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                pages.append({'page':i,"text":text})
    return pages

def chunk_text(pages: List[Dict])-> List[Dict]:
    chunks = []
    chunk_id = 0
    buffer = ""
    buffer_pages = []
    for p in pages:
        buffer += "\n" + p["text"]
        buffer_pages.append = (p["page"])
        #check buffer is too big

        if len(buffer) > settings.CHUNK_SIZE:
            chunk_id += 1
            chunks.append({
                "chunk_id": chunk_id,
                "text": buffer,
                "pages": buffer_pages.copy()
            })

            buffer = buffer[-settings.CHUNK_OVERLAP:]
            buffer_pages = buffer_pages[-1:]

    if buffer.strip():
        chunk_id +=1
        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": buffer,
                "pages": buffer_pages.copy()
            }
        )  

        return chunks      


