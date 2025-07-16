# frontend/Chatbot.py

import streamlit as st
import requests

def show_resume_chatbot():
    st.set_page_config(page_title="Resume Chatbot", page_icon="🧠")
    st.title("🧠 Resume Chatbot ")

    st.markdown("Upload your resume (PDF) and ask a question about it!")

    resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
    query = st.text_input("❓ Ask something about your resume")

    if st.button("💬 Ask"):
        if not resume_file or not query.strip():
            st.warning("Please provide both a resume PDF and a question.")
        else:
            with st.spinner("Thinking..."):
                try:
                    files = {"file": resume_file}
                    data = {"query": query}
                    response = requests.post("https://resume-attendant-system.onrender.com/chat_resume", files=files, data=data)

                    if response.status_code == 200:
                        st.success("✅ Answer:")
                        st.markdown(response.json()["response"])
                    else:
                        st.error(f"❌ Server error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
