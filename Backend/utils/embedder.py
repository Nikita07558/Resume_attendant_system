# backend/utils/embedder.py
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    return embedder.encode([text])[0]  # returns 1D numpy array
