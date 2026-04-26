import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

html, body, [class*="css"] {
    background: radial-gradient(circle at top, #0f172a 0%, #020617 60%, #020617 100%);
    color: white;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 6rem;
    max-width: 900px;
}

.hero {
    text-align: center;
    margin-bottom: 1rem;
}

.hero h1 {
    margin: 0;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    margin: 0.4rem 0 0;
    color: #94a3b8;
    font-size: 0.95rem;
}

.stTextInput > div > div > input,
.stTextArea textarea {
    border-radius: 16px !important;
    border: 1px solid rgba(148,163,184,0.18) !important;
    background: rgba(15, 23, 42, 0.95) !important;
    color: white !important;
}

.stButton > button {
    border-radius: 16px;
    border: none;
    padding: 0.8rem 1.2rem;
    width: 100%;
    background: linear-gradient(135deg, #60a5fa, #a855f7);
    color: white;
    font-weight: 700;
}

.chat-bubble {
    max-width: 88%;
    padding: 0.95rem 1.05rem;
    border-radius: 18px;
    line-height: 1.55;
    font-size: 0.98rem;
    margin-bottom: 0.8rem;
    white-space: pre-wrap;
    word-wrap: break-word;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
}

.user {
    margin-left: auto;
    background: linear-gradient(135deg, #667eea, #7c3aed);
    color: white;
    border-bottom-right-radius: 6px;
}

.assistant {
    margin-right: auto;
    background: rgba(17,24,39,0.96);
    color: #e5e7eb;
    border: 1px solid rgba(255,255,255,0.08);
    border-bottom-left-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = os.getenv("GROQ_API_KEY", "").strip()
client = Groq(api_key=api_key) if api_key else None

st.markdown("""
<div class="hero">
    <h1>⚡ NEXUS AI</h1>
    <p>Fast, smart, clean chat experience powered by Groq</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    selected_model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    )

    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    max_tokens = st.slider("Max tokens", 128, 4096, 1024, 128)

    system_prompt = st.text_area(
        "System prompt",
        value="You are a hel
