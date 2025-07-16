# 📁 Home.py

import streamlit as st
from Classification import show_role_classifier
from Chatbot import show_resume_chatbot
from Matching import show_jd_skill_matcher

st.set_page_config(page_title="Resume Pro Suite", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            background-color: #f9f9f9;
        }

        .main-title {
            font-size: 3rem;
            font-weight: 700;
            color: #4A90E2;
            margin-bottom: 0.5rem;
        }

        .sub-title {
            font-size: 1.25rem;
            color: #555;
            margin-top: 0;
        }

        .sidebar .sidebar-content {
            padding: 2rem 1rem;
        }

        .stRadio > div {
            gap: 0.75rem;
        }

        .stRadio div label {
            font-size: 1.1rem;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# 🧠 Main Title Section
st.markdown('<div class="main-title">📄 Resume Pro Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your All-in-One Resume Intelligence Toolkit 🚀</div>', unsafe_allow_html=True)
st.markdown("---")


st.sidebar.title("🧭 Resume Pro Toolkit")
st.sidebar.markdown("Navigate between the smart resume tools:")

page = st.sidebar.radio(
    "✨ Choose a Feature:",
    [
        "🧠 Resume Role Classifier",
        "🤖 Resume Improvement Chatbot",
        "🔍 JD Skill Matcher"
    ]
)

# 🔁 Page Routing
if page == "🧠 Resume Role Classifier":
    show_role_classifier()

elif page == "🤖 Resume Improvement Chatbot":
    show_resume_chatbot()

elif page == "🔍 JD Skill Matcher":
    show_jd_skill_matcher()
