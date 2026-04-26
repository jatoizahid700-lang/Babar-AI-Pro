import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="⚡ NEXUS AI Pro", layout="wide", initial_sidebar_state="expanded")

# WhatsApp Style CSS - Messages UPWARDS
st.markdown("""
<style>
.main-header {font-size: 3rem !important; font-weight: 700 !important; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
    background-clip: text; text-align: center; margin-bottom: 2rem;}
.user-card {background: linear-gradient(135deg, #1e40af, #1e3a8a); 
    padding: 2rem; border-radius: 20px; color: white; margin-bottom: 2rem; 
    box-shadow: 0 20px 40px rgba(30,64,175,0.3);}
.chat-container {max-height: 600px; overflow-y: auto; padding: 1rem; 
    background: linear-gradient(135deg, #f0f2f5 0%, #e5e7eb 100%);
    border-radius: 20px; margin: 1rem 0;}
.chat-user {background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; 
    padding: 1rem 1.2rem; border-radius: 18px 18px 4px 18px; margin: 0.5rem 0; 
    max-width: 70%; box-shadow: 0 4px 12px rgba(59,130,246,0.4);
    margin-left: auto; text-align: right;}
.chat-bot {background: linear-gradient(135deg, #10b981, #059669); color: white; 
    padding: 1rem 1.2rem; border-radius: 18px 18px 18px 4px; margin: 0.5rem 0; 
    max-width: 70%; box-shadow: 0 4px 12px rgba(16,185,129,0.4);}
.btn-modern {background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
    border: none; border-radius: 12px; padding: 0.8rem 2rem; font-weight: 600; 
    color: white; transition: all 0.3s; box-shadow: 0 4px 15px rgba(59,130,246,0.3);}
.btn-modern:hover {transform: translateY(-3px); box-shadow: 0 8px 25px rgba(59,130,246,0.4);}
.input-section {background: white; padding: 1.5rem; border-radius: 25px; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 1rem;}
</style>
""", unsafe_allow_html=True)

# ========================
# UTILITY FUNCTIONS
# ========================
def safe_timestamp(chat):
    try:
        if 'timestamp' in chat and chat['timestamp']:
            return datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
    except: pass
    return "Now"

# ========================
# GROQ CLIENT
# ========================
@st.cache_resource
def get_client():
    try: return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        st.error("❌ API Key missing!")
        st.stop()

client = get_client()

# ========================
# SESSION
# ========================
def init_session():
    if "user" not in st.session_state: st.session_state.user = None
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    if "last_time" not in st.session_state: st.session_state.last_time = 0
    if "show_history" not in st.session_state: st.session_state.show_history = False
    if "input_key" not in st.session_state: st.session_state.input_key = 0

init_session()

# ========================
# USER SYSTEM
# ========================
def load_users():
    try:
        if os.path.exists("users.json"):
            with open("users.json", "r") as f: return json.load(f)
    except: pass
    return {}

def save_users(users):
    try: os.makedirs("data", exist_ok=True)
    except: pass
    try:
        with open("users.json", "w") as f: json.dump(users, f, indent=2)
    except: pass

def register_user(username, password):
    users = load_users()
    if username in users: return False, "❌ Exists!"
    users[username] = password
    save_users(users)
    return True, "✅ Done!"

# ========================
# MEMORY
# ========================
def get_memory_file():
    os.makedirs("memory", exist_ok=True)
    return f"memory/{st.session_state.user}.json"

def load_memory():
    try:
        if os.path.exists(get_memory_file()):
            with open(get_memory_file(), "r") as f:
                data = json.load(f)
                for chat in data:
                    if 'timestamp' not in chat: chat['timestamp'] = datetime.now().isoformat()
                    if 'model' not in chat: chat['model'] = 'AI'
                return data
    except: pass
    return []

def save_memory(data):
    try:
        with open(get_memory_file(), "w") as f: json.dump(data, f, indent=2)
    except: pass

# ========================
# LOGIN
# ========================
def show_login():
    st.markdown('<h1 class="main-header">🔐 NEXUS AI Pro</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Login")
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        if st.button("🚀 Login", key="login"):
            users = load_users()
            if username in users and users[username] == password:
                st.session_state.user = username
                st.session_state.chat_history = load_memory()
                st.rerun()
            st.error("❌ Wrong!")
    
    with col2:
        st.markdown("### 📝 Register")
        reg_user = st.text_input("👤 Username", key="reg_u")
        reg_pass = st.text_input("🔒 Password", type="password", key="reg_p")
        if st.button("📝 Register", key="reg"):
            success, msg = register_user(reg_user, reg_pass)
            st.info(msg)

if not st.session_state.user:
    show_login()
    st.stop()

# ========================
# RATE LIMIT
# ========================
def rate_limit():
    now = time.time()
    if now - st.session_state.last_time < 2:
        st.warning("⏳ Wait...")
        st.rerun()
    st.session_state.last_time = now

# ========================
# AI
# ========================
MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]

def get_response(prompt):
    for model in MODELS:
        try:
            with st.spinner(f"🤖 {model}..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": "NEXUS AI Pro - Professional assistant."},
                             {"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content, model
        except: continue
    return "⚠️ Try again", None

# ========================
# MAIN UI
# ========================
st.markdown(f'<h1 class="main-header">⚡ {st.session_state.user}</h1>', unsafe_allow_html=True)

st.markdown(f"""
<div class="user-card">
    <h3>👋 Welcome!</h3>
    <p>💬 {len(st.session_state.chat_history)} chats</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Clear", key="clear"): 
        st.session_state.chat_history = []
        save_memory([])
        st.rerun()
with col2:
    if st.button("🚪 Logout", key="logout"):
        st.session_state.clear()
        st.rerun()

# ========================
# CHAT CONTAINER - UPWARDS SCROLL
# ========================
st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

if st.session_state.chat_history:
    # Show NEWEST first (bottom of screen)
    for chat in reversed(st.session_state.chat_history):
        col1, col2 = st.columns([1, 1])
        ts = safe_timestamp(chat)
        
        with col1:
            st.markdown(f"""
            <div class="chat-user">
                <small>{ts}</small><br>{chat['user']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="chat-bot">
                <small>{ts} | {chat.get('model', 'AI')}</small><br>{chat['bot']}
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style='text-align:center; color:#6b7280; padding: 2rem;'>
        👋 Start chatting!<br>
        <small>Messages appear from bottom ↑</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ========================
# INPUT - BOTTOM
# ========================
st.markdown('<div class="input-section">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([3.5, 1, 0.5])
with col1:
    user_input = st.text_input("💭 Type message...", 
                              key=f"input_{st.session_state.input_key}",
                              label_visibility="collapsed")

with col2:
    if st.button("📤", key="send", use_container_width=True):
        if user_input.strip():
            rate_limit()
            st.session_state.input_key += 1  # Clear input
            answer, model = get_response(user_input)
            new_chat = {
                "user": user_input,
                "bot": answer,
                "timestamp": datetime.now().isoformat(),
                "model": model or "AI"
            }
            st.session_state.chat_history.append(new_chat)
            save_memory(st.session_state.chat_history)
            st.rerun()

with col3:
    if st.button("📋", key="history"):
        st.session_state.show_history = True

st.markdown('</div>', unsafe_allow_html=True)

# History Modal
if st.session_state.show_history:
    st.markdown("---")
    st.subheader("📚 History")
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"#{len(st.session_state.chat_history)-i} {safe_timestamp(chat)}"):
            st.write(f"**You:** {chat['user']}")
            st.write(f"**AI:** {chat['bot']}")
    if st.button("❌"):
        st.session_state.show_history = False
        st.rerun()

st.markdown("<p style='text-align:center;color:#6b7280;'>🚀 NEXUS AI Pro</p>", unsafe_allow_html=True)
