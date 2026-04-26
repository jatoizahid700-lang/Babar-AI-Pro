
import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="âš¡",
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

.small-note {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 0.35rem;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")

st.markdown("""
<div class="hero">
    <h1>âš¡ NEXUS AI</h1>
    <p>Fast, smart, clean chat experience powered by Groq</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### âš™ï¸ Settings")
    st.session_state.groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.groq_api_key,
        placeholder="gsk_..."
    )

    selected_model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    )

    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    max_tokens = st.slider("Max tokens", 128, 4096, 1024, 128)

    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful assistant. Reply clearly, smartly, and in the same language as the user.",
        height=110
    )

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Message likhein...")

if prompt:
    if not st.session_state.groq_api_key.strip():
        st.error("Groq API key add karein.")
        st.stop()

    client = Groq(api_key=st.session_state.groq_api_key.strip())
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
            try:
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                reply = response.choices[0].message.content or "No response returned."
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(str(e))
