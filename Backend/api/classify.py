
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

from utils.preprocess import clean_text
from utils.embedder import get_embedding

router = APIRouter()


model_path = os.path.join("models", "resume_classifier.pkl")
encoder_path = os.path.join("models", "label_encoder.pkl")

model = joblib.load(model_path)
label_encoder = joblib.load(encoder_path)

class ResumeRequest(BaseModel):
    text: str

@router.post("/classify")
def classify_resume(req: ResumeRequest):
    try:
        cleaned = clean_text(req.text)
        vec = get_embedding(cleaned).reshape(1, -1)
        pred = model.predict(vec)
        label = label_encoder.inverse_transform(pred)[0]
        return {"predicted_label": label}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
