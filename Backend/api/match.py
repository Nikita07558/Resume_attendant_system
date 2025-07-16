# api/match.py

from fastapi import APIRouter, HTTPException, UploadFile, Form
from utils.skills_extractor import get_missing_skills_from_pdf
import os

router = APIRouter()

@router.post("/match_skills")
async def match_skills(resume_file: UploadFile, jd_text: str = Form(...)):
    try:
        # Save resume temporarily
        temp_path = f"temp_{resume_file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await resume_file.read())

        # Skill matching
        result = get_missing_skills_from_pdf(temp_path, jd_text)

        os.remove(temp_path)  # Clean up
        return {"status": "success", "data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
