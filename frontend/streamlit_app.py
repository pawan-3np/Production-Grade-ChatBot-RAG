import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

def upload_pdf():
    st.sidebar.header("Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")
    if uploaded_file is not None:
        with st.spinner("Uploading and processing PDF..."):
            files = {"file": (uploaded_file.name, uploaded_file.read(), "application/pdf")}
            resp = requests.post(f"{API_URL}/upload_pdf/", files=files)
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Uploaded document. Doc ID: {data['doc_id']}, chunks: {data['num_chunks']}")
        else:
            st.error(f"Upload failed: {resp.text}")

def ask_question():
    st.header("Ask a question")
    question = st.text_input("Your question:")
    if st.button("Ask") and question:
        with st.spinner("Thinking..."):
            resp = requests.post(f"{API_URL}/ask/", json={"question": question})
        if resp.status_code == 200:
            result = resp.json()
            st.write("**Answer:**")
            st.write(result["answer"])
            st.write("**Sources:**")
            for src in result["sources"]:
                st.write(f"Document: {src['doc_id']}, Pages: {src['pages']}, Score: {src['score']:.3f}")
        else:
            st.error("Error in getting answer")

def main():
    st.title("RAG Agent Chatbot")
    upload_pdf()
    st.write("---")
    ask_question()

if __name__ == "__main__":
    main()
