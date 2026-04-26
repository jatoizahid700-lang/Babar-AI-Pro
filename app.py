import os
import base64
import time
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
# Modern CSS
# -------------------------
def load_modern_css():
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
    }
    
    .chat-bubble {
        border-radius: 20px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .user-bubble { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .ai-bubble { 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        margin-right: 2rem;
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 24px;
        padding: 1.5rem;
        border: 2px solid rgba(148, 163, 184, 0.2);
        backdrop-filter: blur(10px);
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
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .stSelectbox > div > div > div {
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.2);
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
        "tokens_used": 0,
        "total_chats": 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_groq_client() -> Optional[Groq]:
    api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def file_to_data_url(uploaded_file):
    data = uploaded_file.read()
    mime = uploaded_file.type or "image/png"
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def safe_groq_response(client: Groq, model: str, messages: List[Dict], temp: float, max_tokens: int) -> tuple[str, int]:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temp,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content or "No response returned."
        tokens = response.usage.total_tokens if response.usage else 0
        return content, tokens
    except Exception as e:
        error_msg = str(e).lower()
        if "rate limit" in error_msg or "429" in error_msg:
            raise RuntimeError("🚫 Groq rate limit hit! 1-2 min wait kar ke try karein.")
        if "invalid_api_key" in error_msg or "401" in error_msg:
            raise RuntimeError("🔑 Groq API key invalid hai. Sidebar mein check karein.")
        raise RuntimeError(f"❌ Groq error: {str(e)[:100]}...")


def build_messages(prompt: str, system_prompt: str) -> List[Dict]:
    messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": prompt})
    return messages


# -------------------------
# Main App
# -------------------------
load_modern_css()
init_session()

# Header
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">🚀 Babar AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Lightning Fast Groq AI • Modern Chat Interface • Urdu/English Support</div>', unsafe_allow_html=True)

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem; font-weight: 700; color: #667eea;">{st.session_state.total_chats}</div>
        <div style="color: #64748b; font-weight: 500;">Total Chats</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2rem; font-weight: 700; color: #10b981;">{st.session_state.tokens_used}</div>
        <div style="color: #64748b; font-weight: 500;">Tokens Used</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.session_state.last_model:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 1.1rem; font-weight: 600; color: #059669;">{st.session_state.last_model}</div>
            <div style="color: #64748b; font-size: 0.9rem;">Last Model</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Groq Settings")
    
    st.session_state.groq_api_key = st.text_input(
        "🔑 Groq API Key", 
        type="password",
        value=st.session_state.get("groq_api_key", ""),
        placeholder="gsk_...",
        help="Groq console se copy karein"
    )
    
    model_options = [
        "llama-3.3-70b-versatile", 
        "llama-3.1-8b-instant", 
        "mixtral-8x7b-32768"
    ]
    
    selected_model = st.selectbox("🤖 AI Model", model_options, index=0)
    
    temp = st.slider("🎚️ Temperature", 0.0, 2.0, 0.7, 0.1)
    max_toks = st.slider("📏 Max Tokens", 256, 8192, 2048, 256)
    
    st.divider()
    system_prompt = st.text_area(
        "🎭 System Prompt",
        value="You are Babar AI - ek helpful aur intelligent assistant. Urdu aur English dono mein clear, accurate jawab do.",
        height=100
    )
    
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_chats = 0
        st.session_state.tokens_used = 0
        st.rerun()

# Main Chat Area
col_left, col_right = st.columns([3, 1])

with col_left:
    # Chat Input
    with st.container():
        st.markdown('<div class="glass-card input-container">', unsafe_allow_html=True)
        prompt = st.text_area(
            "💬 Apna sawal likhein...", 
            height=120, 
            placeholder="Yahan apna message type karein...",
            key="chat_input"
        )
        
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            send = st.button("🚀 Send", type="primary", use_container_width=True)
        with col_btn2:
            if st.session_state.last_model:
                st.markdown(f'<span class="status-badge info-badge">Last: {st.session_state.last_model}</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Chat Display
st.markdown('<div class="glass-card" style="height: 500px; overflow-y: auto; margin-top: 2rem;">', unsafe_allow_html=True)

if st.session_state.messages:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble ai-bubble"><strong>🤖 AI:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Send Logic
if send and prompt.strip():
    client = get_groq_client()
    
    if not client:
        st.error("🔑 Pehle sidebar mein Groq API key daalein!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(f'<div class="chat-bubble user-bubble">{prompt}</div>', unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            with st.spinner(f"🤖 {selected_model} soch raha hai..."):
                try:
                    messages = build_messages(prompt, system_prompt)
                    response, tokens = safe_groq_response(
                        client, selected_model, messages, temp, max_toks
                    )
                    
                    st.session_state.last_model = selected_model
                    st.session_state.tokens_used += tokens
                    st.session_state.total_chats += 1
                    
                    st.markdown(f'<div class="chat-bubble ai-bubble">{response}</div>', unsafe_allow_html=True)
                    st.markdown(f'<span class="status-badge success-badge">✅ {tokens} tokens | {selected_model}</span>', unsafe_allow_html=True)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(str(e))
        
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # Close main-container
