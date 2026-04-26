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

# Professional CSS
st.markdown("""
<style>
.main-header {font-size: 3rem !important; font-weight: 700 !important; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
    background-clip: text; text-align: center; margin-bottom: 2rem;}
.user-card {background: linear-gradient(135deg, #1e40af, #1e3a8a); 
    padding: 2rem; border-radius: 20px; color: white; margin-bottom: 2rem; 
    box-shadow: 0 20px 40px rgba(30,64,175,0.3);}
.chat-user {background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; 
    padding: 1.2rem 1.5rem; border-radius: 25px 25px 5px 25px; margin: 1rem 0; 
    box-shadow: 0 5px 15px rgba(59,130,246,0.3);}
.chat-bot {background: linear-gradient(135deg, #10b981, #059669); color: white; 
    padding: 1.2rem 1.5rem; border-radius: 25px 25px 25px 5px; margin: 1rem 0; 
    box-shadow: 0 5px 15px rgba(16,185,129,0.3);}
.btn-modern {background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
    border: none; border-radius: 12px; padding: 0.8rem 2rem; font-weight: 600; 
    color: white; transition: all 0.3s; box-shadow: 0 4px 15px rgba(59,130,246,0.3);}
.btn-modern:hover {transform: translateY(-3px); box-shadow: 0 8px 25px rgba(59,130,246,0.4);}
.stats-card {background: linear-gradient(135deg, #f8fafc, #e2e8f0); 
    padding: 1.5rem; border-radius: 15px; text-align: center; 
    border-left: 5px solid #3b82f6;}
</style>
""", unsafe_allow_html=True)

# ========================
# UTILITY FUNCTIONS
# ========================
def safe_timestamp(chat):
    """Safe timestamp parsing"""
    try:
        if 'timestamp' in chat and chat['timestamp']:
            return datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
    except:
        pass
    return "Just now"

def safe_chat_length(chat):
    """Safe chat length calculation"""
    try:
        return len(str(chat.get('user', '')) + str(chat.get('bot', '')))
    except:
        return 0

# ========================
# GROQ CLIENT
# ========================
@st.cache_resource
def get_client():
    try:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        st.error("❌ GROQ_API_KEY missing in secrets.toml!")
        st.stop()

client = get_client()

# ========================
# SESSION INIT
# ========================
def init_session():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_time" not in st.session_state:
        st.session_state.last_time = 0
    if "show_history" not in st.session_state:
        st.session_state.show_history = False

init_session()

# ========================
# USER SYSTEM
# ========================
def load_users():
    try:
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    try:
        with open("users.json", "w") as f:
            json.dump(users, f, indent=2)
    except:
        pass

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "❌ User already exists!"
    users[username] = password
    save_users(users)
    return True, "✅ Registration successful!"

# ========================
# MEMORY SYSTEM
# ========================
def get_memory_file():
    os.makedirs("memory", exist_ok=True)
    return f"memory/{st.session_state.user}.json"

def load_memory():
    try:
        if os.path.exists(get_memory_file()):
            with open(get_memory_file(), "r") as f:
                data = json.load(f)
                # Fix old format chats
                for chat in data:
                    if 'user' not in chat or 'bot' not in chat:
                        continue
                    if 'timestamp' not in chat:
                        chat['timestamp'] = datetime.now().isoformat()
                    if 'model' not in chat:
                        chat['model'] = 'Unknown'
                return data
    except:
        pass
    return []

def save_memory(data):
    try:
        with open(get_memory_file(), "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Save error: {e}")

# ========================
# LOGIN
# ========================
def show_login():
    st.markdown('<h1 class="main-header">🔐 NEXUS AI Pro</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])
    
    with col1:
        st.markdown("### 🚀 Login")
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        if st.button("🚀 Login", key="login_btn"):
            users = load_users()
            if username in users and users[username] == password:
                st.session_state.user = username
                st.session_state.chat_history = load_memory()
                st.rerun()
            else:
                st.error("❌ Wrong credentials!")
    
    with col2:
        st.markdown("### 📝 Register")
        reg_user = st.text_input("👤 New Username", key="reg_u")
        reg_pass = st.text_input("🔒 New Password", type="password", key="reg_p")
        if st.button("📝 Register", key="reg_btn"):
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
        st.warning("⏳ Wait 2 seconds...")
        st.rerun()
    st.session_state.last_time = now

# ========================
# AI CHAT
# ========================
MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]

def get_response(prompt):
    for model in MODELS:
        try:
            with st.spinner(f"🤖 {model}..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are NEXUS AI Pro. Professional & helpful."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                return response.choices[0].message.content, model
        except:
            continue
    return "⚠️ All models failed", None

# ========================
# MAIN UI
# ========================
st.markdown('<h1 class="main-header">⚡ Welcome {}</h1>'.format(st.session_state.user), unsafe_allow_html=True)

# Stats
col1, col2, col3 = st.columns(3)
total_chats = len(st.session_state.chat_history)
avg_len = sum(safe_chat_length(c) for c in st.session_state.chat_history) / max(1, total_chats)

with col1:
    st.markdown(f"""
    <div class="stats-card">
        <h3>💬 Chats</h3>
        <h2>{total_chats}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-card">
        <h3>📊 Avg Length</h3>
        <h2>{int(avg_len)} chars</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.session_state.chat_history:
        last_model = st.session_state.chat_history[-1].get('model', 'None')
        st.markdown(f"""
        <div class="stats-card">
            <h3>🎯 Last Model</h3>
            <h2>{last_model}</h2>
        </div>
        """, unsafe_allow_html=True)

# Controls
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Clear History", key="clear"):
        st.session_state.chat_history = []
        save_memory([])
        st.rerun()
with col2:
    if st.button("🚪 Logout", key="logout"):
        st.session_state.clear()
        st.rerun()

st.markdown("---")

# Chat Input
col1, col2 = st.columns([4,1])
with col1:
    user_input = st.text_input("💭 Ask anything...", key="input")
with col2:
    if st.button("📤 Send", key="send"):
        if user_input.strip():
            rate_limit()
            answer, model = get_response(user_input)
            new_chat = {
                "user": user_input,
                "bot": answer,
                "timestamp": datetime.now().isoformat(),
                "model": model or "Unknown"
            }
            st.session_state.chat_history.append(new_chat)
            save_memory(st.session_state.chat_history)
            st.rerun()

if st.button("📋 Full History"):
    st.session_state.show_history = not st.session_state.show_history

# Recent Chats
st.subheader("💬 Recent Chats")
if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history[-10:]):
        col1, col2 = st.columns([1,1])
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
    st.info("👋 No chats yet. Send a message!")

# Full History
if st.session_state.show_history:
    st.markdown("---")
    st.subheader("📚 Complete History")
    for i, chat in enumerate(st.session_state.chat_history):
        with st.expander(f"#{i+1} {safe_timestamp(chat)}"):
            st.write(f"**👤** {chat['user']}")
            st.write(f"**🤖** {chat['bot']}")
    
    if st.button("❌ Close"):
        st.session_state.show_history = False
        st.rerun()

st.markdown("---")
st.markdown("<p style='text-align:center;color:#6b7280;'>🚀 NEXUS AI Pro © 2026</p>", unsafe_allow_html=True)
