# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import classify
from api import match
from api import chatbot  # ✅ make sure this line is added

app = FastAPI()

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8501"] if strict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(classify.router)
app.include_router(match.router)
app.include_router(chatbot.router)  # ✅ include the chatbot routes here

