import os
import streamlit as st
from groq import Groq

# Page Config
st.set_page_config(
    page_title="NEXUS AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Styling for "Khula-Khula" look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Background setup */
    .stApp {
        background-color: #0f172a;
    }

    /* Removing borders and making it spacious */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 800px; /* Chat width control */
    }

    /* Header styling */
    .hero-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }

    /* Chat Bubbles Styling */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1rem 0rem !important;
    }

    /* User Message Bubble */
    .st-emotion-cache-janw0x {
        background: linear-gradient(135deg, #667eea, #7c3aed) !important;
        border-radius: 20px 20px 0px 20px !important;
        color: white !important;
        padding: 15px 20px !important;
    }

    /* AI Message Bubble */
    .st-emotion-cache-1ghh6s0 {
        background: #1e293b !important;
        border-radius: 20px 20px 20px 0px !important;
        color: #e2e8f0 !important;
        padding: 15px 20px !important;
        border: 1px solid #334155 !important;
    }

    /* Hide redundant elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Input field styling */
    .stChatInputContainer {
        padding-bottom: 2rem !important;
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.markdown('<h1 class="hero-title">⚡ NEXUS AI</h1>', unsafe_allow_html=True)

# Sidebar settings (hidden by default)
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
    selected_model = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Display Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
prompt = st.chat_input("Apna sawal likhein...")

if prompt:
    if not api_key:
        st.error("Meherbani karke Sidebar mein API Key darj karein.")
    else:
        client = Groq(api_key=api_key)
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response
        with st.chat_message("assistant"):
            with st.spinner("Soch raha hoon..."):
                try:
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=[{"role": "m", "content": "You are a helpful assistant."}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    
