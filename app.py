import os
import base64
from typing import List, Dict, Optional

import streamlit as st
from groq import Groq


# -------------------------
# Page Setup
# -------------------------
st.set_page_config(
    page_title="🚀 Babar AI - Groq Turbo",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------
# Modern CSS + Auto-scroll
# -------------------------
def load_perfect_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main-container {
        padding: 2rem 2rem 1rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #64748b;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .status-badge {
        display: inline-flex;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .success-badge { background: rgba(34, 197, 94, 0.2); color: #059669; border: 1px solid rgba(34, 197, 94, 0.3); }
    .info-badge { background: rgba(59, 130, 246, 0.2); color: #2563eb; border: 1px solid rgba(59, 130, 246, 0.3); }
    
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.2);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
    }
    
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 1rem;
        margin-bottom: 1rem;
        scrollbar-width: thin;
        scrollbar-color: rgba(148, 163, 184, 0.3) transparent;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.3);
        border-radius: 3px;
    }
    
    .chat-bubble {
        border-radius: 20px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-bubble { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
        max-width: 80%;
    }
    
    .ai-bubble { 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        margin-right: 2rem;
        max-width: 80%;
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        padding: 1.5rem;
        border: 2px solid rgba(148, 163, 184, 0.2);
        backdrop-filter: blur(10px);
        position: sticky;
        bottom: 0;
        z-index: 10;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        height: auto;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)


# -------------------------
# Core Functions
# -------------------------
def init_session():
    defaults = {
        "messages": [],
        "last_model": None,
        "total_chats": 0,
        "response_time": 0,
        "auto_scroll": True
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_groq_client() -> Optional[Groq]:
    api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def safe_groq_response(client: Groq, model: str, messages: List[Dict], temp: float, max_tokens: int) -> str:
    import time
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temp,
            max_tokens=max_tokens,
        )
        response_time = round((time.time() - start_time) * 1000, 1)
        st.session_state.response_time = response_time
        return response.choices[0].message.content or "No response returned."
    except Exception as e:
        error_msg = str(e).lower()
        if "rate limit" in error_msg or "429" in error_msg:
            raise RuntimeError("🚫 Groq rate limit! 1-2 min wait karein.")
        if "invalid_api_key" in error_msg or "401" in error_msg:
            raise RuntimeError("🔑 Groq API key check karein!")
        raise RuntimeError(f"❌ Error: {str(e)[:80]}...")


def build_messages(prompt: str, system_prompt: str) -> List[Dict]:
    messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": prompt})
    return messages


# -------------------------
# Main App
# -------------------------
load_perfect_css()
init_session()

# Header
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">🚀 Babar AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Lightning Fast • Auto-scroll • Perfect Chat Experience</div>', unsafe_allow_html=True)

# Perfect Stats (No Tokens)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem; font-weight: 700; color: #667eea;">{st.session_state.total_chats}</div>
        <div style="color: #64748b; font-weight: 500;">Chats</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_time = st.session_state.response_time if st.session_state.total_chats > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem; font-weight: 700; color: #10b981;">{avg_time}ms</div>
        <div style="color: #64748b; font-weight: 500;">Avg Response</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.session_state.last_model:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.1rem; font-weight: 600; color: #059669;">{st.session_state.last_model.split('-')[0].upper()}</div>
            <div style="color: #64748b; font-size: 0.9rem;">Model</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.groq_api_key = st.text_input(
        "🔑 Groq API Key", type="password",
        value=st.session_state.get("groq_api_key", ""),
        placeholder="gsk_..."
    )
    
    model_options = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    selected_model = st.selectbox("🤖 Model", model_options, index=0)
    
    temperature = st.slider("🎚️ Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("📏 Max Tokens", 256, 8192, 2048, 256)
    
    st.divider()
    system_prompt = st.text_area(
        "🎭 System Prompt",
        value="You are Babar AI - helpful, intelligent assistant. Urdu aur English mein clear jawab do.",
        height=100
    )
    
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_chats = 0
        st.session_state.response_time = 0
        st.rerun()

# Main Chat Area - PERFECT AUTO-SCROLL
chat_col1, chat_col2 = st.columns([3, 1])

with chat_col1:
    # Chat Display with Auto-scroll
    chat_container = st.container(height=500)
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if st.session_state.messages:
            for i, msg in enumerate(st.session_state.messages):
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-bubble user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble ai-bubble"><strong>🤖</strong> {msg["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input - Always at Bottom
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    prompt = st.text_area(
        "💬 Message likhein...", 
        height=100, 
        placeholder="Yahan type karein aur Enter daba dein...",
        key="main_input"
    )
    
    col_btn1, col_status = st.columns([1, 3])
    with col_btn1:
        send = st.button("🚀 Send", type="primary", use_container_width=True)
    with col_status:
        if st.session_state.last_model:
            st.markdown(f'<span class="status-badge info-badge">Last: {st.session_state.last_model.split("-")[0]}</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Send Logic
if send and prompt.strip():
    client = get_groq_client()
    
    if not client:
        st.error("🔑 Sidebar mein Groq API key daalein!")
        st.rerun()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_chats += 1
    
    with chat_container.container():
        st.markdown('<div class="chat-bubble user-bubble">' + prompt + '</div>', unsafe_allow_html=True)
    
    with chat_container.container():
        with st.spinner("🤖 AI soch raha hai..."):
            try:
                messages = build_messages(prompt, system_prompt)
                response = safe_groq_response(client, selected_model, messages, temperature, max_tokens)
                
                st.session_state.last_model = selected_model
                st.markdown(f'<div class="chat-bubble ai-bubble"><strong>🤖</strong> {response}</div>', unsafe_allow_html=True)
                st.markdown(f'<span class="status-badge success-badge">✅ Response ready!</span>', unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.markdown(f'<div class="chat-bubble ai-bubble" style="background: linear-gradient(135deg, #ef4444, #dc2626);">❌ {str(e)}</div>', unsafe_allow_html=True)
    
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # main-container
