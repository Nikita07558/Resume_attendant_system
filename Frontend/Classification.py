# frontend/Classification.py

import streamlit as st
import requests
import fitz  # PyMuPDF
import io

def show_role_classifier():
    st.set_page_config(page_title="Resume Classifier", page_icon="🧠")
    st.title("🧠 Resume Role Classifier")
    st.write("Upload a resume and get its predicted job role.")

    # 📁 Upload resume
    uploaded = st.file_uploader("Upload your resume (.pdf or .txt)", type=["pdf", "txt"])

    def extract_text_from_pdf(file):
        text = ""
        with fitz.open(stream=io.BytesIO(file.read()), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

    def send_to_backend(text):
        url = "http://localhost:8000/classify"
        try:
            res = requests.post(url, json={"text": text})
            if res.status_code == 200:
                return res.json()["predicted_label"]
            else:
                return f"Error: {res.status_code} - {res.text}"
        except Exception as e:
            return f"❌ Failed to connect to backend: {e}"

    if uploaded:
        # 🧠 Extract text
        if uploaded.name.endswith(".pdf"):
            text = extract_text_from_pdf(uploaded)
        else:
            text = uploaded.read().decode("utf-8")

        # 🧪 Show preview
        with st.expander("📄 Resume Preview"):
            st.write(text[:1000] + "..." if len(text) > 1000 else text)

        # 🔍 Predict button
        if st.button("🧠 Predict Job Role"):
            with st.spinner("Predicting..."):
                label = send_to_backend(text)
            st.success(f"🎯 Predicted Job Role: `{label}`")
