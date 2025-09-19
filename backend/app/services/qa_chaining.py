from backend.app.services.retriever import retrieve
from backend.app.config import settings
from google import genai


def answer_question(question: str):
    retrieved = retrieve(question, settings.TOP_K)

    context_texts = []
    source_info = []

    for (entry,score) in retrieved:
        context_texts.append(entry["text"])
        source_info.append(
            {
                "doc_id": entry["doc_id"],
                "pages": entry["pages"],
                "score": score
            }
        )

    prompt = build_prompt(question, context_texts)
    resp = genai.Client().models.generate_content(
        model = settings.LLM_MODEL,
        prompt = prompt
    ) 

    answer = resp.candidates[0].output
    return {
        "answer":answer,
        "sources": source_info
    }
def build_prompt(question: str, context: list[str])-> str:
    system = "You are an AI assistant. Use the following context to answer the question. If you do not know the answer, say so."
    ctx = "\n\n".join(context)
    prompt = f"{system}\n\nContext: \n{ctx} \n\nQuestion: {question}\nAnswer"
    return prompt


