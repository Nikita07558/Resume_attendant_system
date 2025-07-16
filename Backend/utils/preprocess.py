# backend/utils/preprocess.py
import re
import spacy

nlp = spacy.load("en_core_web_sm")
stopwords = nlp.Defaults.stop_words

def clean_text(text: str) -> str:
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'\b\d{10,}\b', '', text)
    text = re.sub(r'\b\d+\b', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()

    doc = nlp(text)
    tokens = [
        token.lemma_ for token in doc
        if token.text not in stopwords and not token.is_stop and not token.is_punct
    ]
    return " ".join(tokens)
