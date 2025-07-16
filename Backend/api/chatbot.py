# 📁 api/chatbot.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from pypdf import PdfReader
import os
from dotenv import load_dotenv
import re

load_dotenv()
router = APIRouter()

# 🔑 Groq Chat LLM Setup
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-70b-8192"
)

# 📚 Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 📂 Vector DB path (optional for persistent DB)
VECTOR_DB_PATH = "vectorstore/"
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

# 🔍 Extract text from uploaded PDF
def extract_text_from_pdf(file: UploadFile) -> str:
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# 📦 Split into chunks, embed, and store in FAISS
def create_vector_db_from_resume(text: str) -> FAISS:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    vectorstore = FAISS.from_documents(docs, embedding_model)
    return vectorstore

# 🧹 Optional: Clean markdown-style output
def clean_response(text: str) -> str:
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove bold
    text = re.sub(r'\* ', '- ', text)              # Convert bullets to dashes
    text = text.replace('\n', '\n')                # Normalize newlines
    return text.strip()

# 🚀 Main route for chat-based QnA with resume
@router.post("/chat_resume")
async def chat_with_resume(file: UploadFile = File(...), query: str = Form(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        resume_text = extract_text_from_pdf(file)
        vectorstore = create_vector_db_from_resume(resume_text)
        rel_docs = vectorstore.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in rel_docs])

        full_prompt = f"Answer the question based on this resume:\n\n{context}\n\nQuestion: {query}"
        raw_response = llm.invoke([HumanMessage(content=full_prompt)])
        cleaned_response = clean_response(raw_response.content)

        return {"response": cleaned_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
