import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

# Title & Favicon
st.set_page_config(
    page_title="🤖 NEXUS Pro AI", 
    page_icon="🤖",
    layout="wide"
)

# ========================
# PROFESSIONAL CSS - Perplexity Style
# ========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
.main-header {
    font-size: 2.5rem !important; font-weight: 700 !important; 
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin: 1rem 0;
}
.chat-container {
    height: 70vh; overflow-y: auto; padding: 2rem;
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 20px; margin: 1rem 0; box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}
.message-bubble {
    margin: 1rem 0; padding: 1.2rem 1.5rem; border-radius: 20px; 
    max-width: 75%; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    animation: fadeInUp 0.3s ease;
}
.user-message {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white;
    margin-left: auto; border-bottom-right-radius: 5px;
}
.ai-message {
    background: linear-gradient(135deg, #10b981, #059669); color: white;
    margin-right: auto; border-bottom-left-radius: 5px;
}
.input-container {
    position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%);
    width: 90%; max-width: 800px; background: white; padding: 1.5rem;
    border-radius: 25px; box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    z-index: 1000;
}
.btn-icon {border-radius: 50%; width: 45px; height: 45px; padding: 0; 
    border: none; font-size: 1.2rem; transition: all 0.3s;}
.btn-primary {background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white;}
.btn-secondary {background: #f1f5f9; color: #64748b;}
.header-bar {background: white; padding: 1rem 2rem; border-radius: 15px; 
    box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-bottom: 1rem;}
@keyframes fadeInUp {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ========================
# CLIENT
# ========================
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# ========================
# SESSION
# ========================
if "user" not in st.session_state: st.session_state.user = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "input_key" not in st.session_state: st.session_state.input_key = 0
if "last_time" not in st.session_state: st.session_state.last_time = 0

# ========================
# FUNCTIONS
# ========================
def safe_time(chat):
    try: return datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
    except: return "Now"

def load_users():
    try:
        if os.path.exists("users.json"):
            with open("users.json") as f: return json.load(f)
    except: pass
    return {}

def load_memory():
    os.makedirs("memory", exist_ok=True)
    try:
        fname = f"memory/{st.session_state.user}.json"
        if os.path.exists(fname):
            with open(fname) as f:
                chats = json.load(f)
                for chat in chats:
                    if 'timestamp' not in chat: chat['timestamp'] = datetime.now().isoformat()
                return chats
    except: pass
    return []

def save_memory(data):
    try:
        fname = f"memory/{st.session_state.user}.json"
        with open(fname, "w") as f: json.dump(data, f, indent=2)
    except: pass

def rate_limit():
    now = time.time()
    if now - st.session_state.last_time < 2: st.rerun()
    st.session_state.last_time = now

def ai_respond(prompt):
    from groq import Groq
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    for model in models:
        try:
            with st.spinner("🤖 Thinking..."):
                resp = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": "You are NEXUS Pro AI. I'm a professional AI assistant built by Nexus AI team. Answer professionally and helpfully."},
                             {"role": "user", "content": prompt}]
                )
                return resp.choices[0].message.content, model
        except: continue
    return "Sorry, try again!", "Error"

# ========================
# LOGIN
# ========================
if not st.session_state.user:
    st.markdown('<h1 class="main-header">🤖 NEXUS Pro AI</h1>', unsafe_allow_html=True)
    st.markdown("### Fast • Smart • Professional")
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        if st.button("🚀 Login", use_container_width=True):
            users = load_users()
            if username in users and users[username] == password:
                st.session_state.user = username
                st.session_state.chat_history = load_memory()
                st.rerun()
            st.error("❌ Invalid!")
    
    with col2:
        ruser = st.text_input("👤 New User", key="ruser")
        rpass = st.text_input("🔒 Password", type="password", key="rpass")
        if st.button("📝 Sign Up", use_container_width=True):
            users = load_users()
            if ruser not in users:
                users[ruser] = rpass
                with open("users.json", "w") as f: json.dump(users, f)
                st.success("✅ Welcome!")
                st.rerun()
            st.error("❌ Exists!")
    st.stop()

# ========================
# MAIN INTERFACE
# ========================

# Header Bar with Icons
st.markdown("""
<div class="header-bar">
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h2 style='margin: 0; color: #1e293b;'>🤖 NEXUS Pro AI</h2>
            <p style='margin: 0; color: #64748b;'>Hi, {}</p>
        </div>
        <div style='display: flex; gap: 1rem;'>
            <button class="btn-icon btn-secondary" onclick="window.history_view.toggle()">📋</button>
            <button class="btn-icon btn-secondary" onclick="window.clear_chat()">🗑️</button>
            <button class="btn-icon btn-primary" onclick="window.logout()">🚪</button>
        </div>
    </div>
</div>
""".format(st.session_state.user), unsafe_allow_html=True)

# Chat Container - Auto Scroll to Bottom
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container" id="messages">', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        # Latest messages at BOTTOM
        for chat in st.session_state.chat_history:
            col1, col2 = st.columns([3, 1]) if 'user' in chat else st.columns([1, 3])
            
            ts = safe_time(chat)
            
            if 'user' in chat:
                with col2: st.markdown(f"""
                <div class="message-bubble user-message">
                    <div style='font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.5rem;'>
                        {ts}
                    </div>
                    {chat['user']}
                </div>
                """, unsafe_allow_html=True)
                with col1: st.empty()
            else:
                with col1: st.markdown(f"""
                <div class="message-bubble ai-message">
                    <div style='font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.5rem;'>
                        NEXUS Pro AI • {ts}
                    </div>
                    {chat['bot']}
                </div>
                """, unsafe_allow_html=True)
                with col2: st.empty()
    else:
        st.markdown("""
        <div style='text-align: center; color: #64748b; margin-top: 4rem;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🤖</div>
            <h3>Welcome to NEXUS Pro AI</h3>
            <p>Ask me anything! I'm here to help.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Fixed Input Bottom
st.markdown("""
<div class="input-container">
    <div style='display: flex; gap: 1rem; align-items: center;'>
""", unsafe_allow_html=True)

user_input = st.text_input("", key=f"inp_{st.session_state.input_key}", 
                          placeholder="Ask NEXUS Pro AI anything...", 
                          label_visibility="collapsed")

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("📤", key="send_btn", use_container_width=True, type="primary"):
        if user_input.strip():
            rate_limit()
            st.session_state.input_key += 1
            st.session_state.chat_history.append({"user": user_input})
            save_memory(st.session_state.chat_history)
            
            with st.spinner("NEXUS Pro AI is thinking..."):
                answer, model = ai_respond(user_input)
                st.session_state.chat_history.append({"bot": answer})
                save_memory(st.session_state.chat_history)
            
            st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# JavaScript for Auto-scroll
st.markdown("""
<script>
    window.onload = function() {
        const chat = document.getElementById('messages');
        chat.scrollTop = chat.scrollHeight;
    }
    // Auto scroll on new messages
    const observer = new MutationObserver(function() {
        const chat = document.getElementById('messages');
        chat.scrollTop = chat.scrollHeight;
    });
    observer.observe(document.getElementById('messages'), {childList: true});
</script>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #94a3b8; font-size: 0.9rem;'>
    🤖 NEXUS Pro AI • Powered by Groq • © 2026
</div>
""", unsafe_allow_html=True)
