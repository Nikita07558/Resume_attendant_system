# utils/skills_extractor.py

import os
import json
import numpy as np
import spacy
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")
nlp = spacy.load("en_core_web_sm")

SKILLS_PATH = os.path.join("utils", "onet_skills.json")
EMBEDDINGS_PATH = os.path.join("utils", "skills_matrix.npy")

with open(SKILLS_PATH, "r") as f:
    skill_phrases = json.load(f)

skill_matrix = np.load(EMBEDDINGS_PATH)
assert len(skill_phrases) == skill_matrix.shape[0], "Mismatch in skills vs embeddings"

SIMILARITY_THRESHOLD = 0.72

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def extract_contextual_phrases(text: str):
    doc = nlp(text.lower())
    phrases = set()

    for sent in doc.sents:
        cleaned = sent.text.strip()
        if 5 <= len(cleaned) <= 100:
            phrases.add(cleaned)

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        if 2 <= len(phrase) <= 50:
            phrases.add(phrase)

    for token in doc:
        if not token.is_stop and not token.is_punct and token.pos_ in {"NOUN", "PROPN", "VERB"}:
            if 2 <= len(token.text) <= 30:
                phrases.add(token.lemma_.strip())

    return list(phrases)

def match_skills_from_text(text: str):
    phrases = extract_contextual_phrases(text)
    if not phrases:
        return []

    phrase_embeddings = model.encode(phrases)
    sims = cosine_similarity(phrase_embeddings, skill_matrix)

    matched_skills = set()
    for i, row in enumerate(sims):
        max_idx = np.argmax(row)
        if row[max_idx] >= SIMILARITY_THRESHOLD:
            matched_skills.add(skill_phrases[max_idx])

    return sorted(matched_skills)

def get_missing_skills_from_pdf(resume_pdf_path: str, jd_text: str):
    resume_text = extract_text_from_pdf(resume_pdf_path)
    resume_skills = set(match_skills_from_text(resume_text))
    jd_skills = set(match_skills_from_text(jd_text))

    missing = jd_skills - resume_skills
    return {
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
        "missing_skills": sorted(missing)
    }
