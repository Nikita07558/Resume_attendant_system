# 🧠 Resume Intelligence Suite

An AI-powered resume analysis and enhancement platform with three powerful features:

1. 🎯 **Resume Role Classification**  
2. 🤖 **Resume Chatbot (RAG-powered Q&A)**  
3. 🧩 **Job Description vs Resume Skill Matcher**

---

## 🚀 Features

### 1. Resume Role Classifier
Predicts the most suitable job role for any uploaded resume (PDF or TXT). Uses sentence embeddings and a trained ML classifier.

### 2. Resume Chatbot
Ask questions directly from your resume using Retrieval-Augmented Generation (RAG). Example:
> "What are my top skills?"  
> "Describe my latest job experience."

### 3. JD vs Resume Skill Matcher
Paste a job description and see which required skills are **missing** in your resume. Uses:
- NER (Named Entity Recognition)
- O*NET skill taxonomy
- Fuzzy matching

---

## 🛠 Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Streamlit |
| Backend | Python |
| NLP Models | SentenceTransformers (`gtr-t5-base`), SpaCy |
| ML | Scikit-learn |
| RAG | Custom retriever with OpenAI/Groq LLM (optional) |
| Data | O*NET Skills, Labeled Resumes |


# Usage Flow
Go to Resume Role Classifier tab
→ Upload a resume → See predicted job role

Go to Resume Chatbot tab
→ Upload resume → Ask any question

Go to JD Matcher tab
→ Upload resume + paste job description → View missing skills


## 🧑‍💻 How to Run

### 🔧 Install Requirements

pip install -r requirements.txt

🚀 Run Backend
Backend code includes:

Embedding resumes
Training classifier
Skill extraction
Chatbot logic

To train the model:
python train_classifier.py

🖥 Run Frontend (Streamlit App)
streamlit run Home.py
