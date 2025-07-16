# frontend/Matching.py

import streamlit as st
import requests

def show_jd_skill_matcher():
    st.set_page_config(page_title="Skill Matcher", page_icon="🔍")
    st.title("🔍 JD Skill Matcher")

    st.markdown("Upload your resume (PDF) and paste the job description below.")

    resume_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("💼 Paste Job Description Text", height=250)

    if st.button("🔍 Match Skills"):
        if not resume_file or not jd_text:
            st.warning("Please provide both a resume PDF and job description.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    files = {"resume_file": (resume_file.name, resume_file, "application/pdf")}
                    data = {"jd_text": jd_text}

                    response = requests.post(
                        "https://resume-attendant-system.onrender.com/match_skills",
                        files=files,
                        data=data
                    )

                    if response.status_code == 200:
                        data = response.json()["data"]

                        st.success("✅ Skill matching complete!")
                        st.subheader("✅ Skills in Resume")
                        st.write(", ".join(data["resume_skills"]) or "None")

                        st.subheader("💼 Skills Required in JD")
                        st.write(", ".join(data["jd_skills"]) or "None")

                        st.subheader("⚠️ Missing Skills")
                        st.write(", ".join(data["missing_skills"]) or "✅ All skills covered!")

                    else:
                        st.error(f"Server error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error contacting backend: {e}")
