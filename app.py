import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

# ========================
# CONFIG - Professional Theme
# ========================
st.set_page_config(
    page_title="⚡ NEXUS AI Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
    }
    .user-card {
        background: linear-gradient(135deg, #1e40af, #1e3a8a);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(30,64,175,0.3);
    }
    .chat-user {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 25px 25px 5px 25px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(59,130,246,0.3);
    }
    .chat-bot {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 25px 25px 25px 5px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(16,185,129,0.3);
    }
    .btn-modern {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        color: white;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(59,130,246,0.3);
    }
    .btn-modern:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(59,130,246,0.4);
    }
    .btn-secondary {
        background: linear-gradient(135deg, #6b7280, #4b5563);
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        color: white;
        transition: all 0.3s;
    }
    .stats-card {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border-left: 5px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ========================
# GROQ CLIENT
# ========================
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# ========================
# SESSION STATE
# ========================
def init_session():
    defaults = {
        "user": None,
        "last_time": 0,
        "show_history": False,
        "chat_history": []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# ========================
# USER MANAGEMENT
# ========================
def load_users():
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

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
                return json.load(f)
    except:
        pass
    return []

def save_memory(data):
    try:
        with open(get_memory_file(), "w") as f:
            json.dump(data, f, indent=2)
    except:
        st.error("Failed to save memory!")

# ========================
# LOGIN SCREEN
# ========================
def show_login():
    st.markdown('<h1 class="main-header">🔐 NEXUS AI Pro</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🚀 Professional AI Assistant")
        st.markdown("*Fast • Smart • Secure*")
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            username = st.text_input("👤 Username", key="login_user")
            password = st.text_input("🔒 Password", type="password", key="login_pass")
            
            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("🚀 Login", key="login", use_container_width=True):
                    users = load_users()
                    if username in users and users[username] == password:
                        st.session_state.user = username
                        st.session_state.chat_history = load_memory()
                        st.success("✅ Login Successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
            
        with tab2:
            reg_username = st.text_input("👤 New Username", key="reg_user")
            reg_password = st.text_input("🔒 New Password", type="password", key="reg_pass")
            reg_confirm = st.text_input("🔒 Confirm Password", type="password", key="reg_confirm")
            
            if reg_password and reg_confirm and reg_password == reg_confirm:
                if st.button("📝 Register", key="register", use_container_width=True):
                    success, message = register_user(reg_username, reg_password)
                    st.info(message)
            elif st.button("📝 Register", key="register", use_container_width=True, disabled=True):
                pass

if not st.session_state.user:
    show_login()
    st.stop()

# ========================
# RATE LIMITER
# ========================
def check_rate_limit():
    current_time = time.time()
    if current_time - st.session_state.last_time < 2:
        st.warning("⏳ Please wait 2 seconds...")
        time.sleep(2)
        st.rerun()
    st.session_state.last_time = current_time

# ========================
# AI RESPONSE
# ========================
MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768"
]

def get_ai_response(prompt):
    for model in MODELS:
        try:
            with st.spinner(f"🤖 {model} is thinking..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are NEXUS AI Pro - Professional, helpful, accurate AI assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                return response.choices[0].message.content, model
        except Exception as e:
            st.warning(f"Model {model} failed, trying next...")
            continue
    return "⚠️ All models unavailable. Please try again later.", None

# ========================
# MAIN DASHBOARD
# ========================
# Header
st.markdown('<h1 class="main-header">⚡ NEXUS AI Pro</h1>', unsafe_allow_html=True)

# User Info & Controls
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"""
    <div class="user-card">
        <h3>👋 Welcome, <strong>{st.session_state.user}</strong>!</h3>
        <p>🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>💬 Total Messages: <strong>{len(st.session_state.chat_history)}</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🗑️ Clear History", key="clear", use_container_width=True):
            st.session_state.chat_history = []
            save_memory([])
            st.success("History cleared!")
            st.rerun()
    with col_btn2:
        if st.button("🚪 Logout", key="logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stats-card">
        <h3 style='color: #3b82f6; margin: 0;'>💬 Chats</h3>
        <h2 style='margin: 0; color: #1e40af;'>{}</h2>
    </div>
    """.format(len(st.session_state.chat_history)), unsafe_allow_html=True)

with col2:
    avg_length = sum(len(str(chat.get('user', '')) + str(chat.get('bot', ''))) for chat in st.session_state.chat_history) / max(1, len(st.session_state.chat_history))
    st.markdown(f"""
    <div class="stats-card">
        <h3 style='color: #10b981; margin: 0;'>📊 Avg Length</h3>
        <h2 style='margin: 0; color: #059669;'>{avg_length:.0f} chars</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stats-card">
        <h3 style='color: #f59e0b; margin: 0;'>⚡ Uptime</h3>
        <h2 style='margin: 0; color: #d97706;'>100%</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========================
# CHAT INPUT
# ========================
col_input1, col_input2 = st.columns([4, 1])
with col_input1:
    user_input = st.text_input(
        "💭 Ask anything...", 
        placeholder="Type your question here...",
        label_visibility="collapsed",
        key="user_input"
    )

with col_input2:
    send_message = st.button("📤 Send", key="send_message", use_container_width=True)

# History Button
if st.button("📋 Full History", key="show_history_btn", use_container_width=True):
    st.session_state.show_history = not st.session_state.show_history

# Send Message
if send_message and user_input.strip():
    check_rate_limit()
    answer, model = get_ai_response(user_input)
    
    new_chat = {
        "user": user_input,
        "bot": answer,
        "timestamp": datetime.now().isoformat(),
        "model": model or "Unknown"
    }
    
    st.session_state.chat_history.append(new_chat)
    save_memory(st.session_state.chat_history)
    st.rerun()

# ========================
# CHAT DISPLAY
# ========================
st.subheader("💬 Recent Conversations")

if st.session_state.chat_history:
    for chat in reversed(st.session_state.chat_history[-15:]):  # Last 15
        col1, col2 = st.columns([1, 1])
        
        ts = datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
        
        with col1:
            st.markdown(f"""
            <div class="chat-user">
                <small style='opacity: 0.8;'>{ts} 👤</small><br>
                {chat['user']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="chat-bot">
                <small style='opacity: 0.8;'>{ts} 🤖 {chat.get('model', 'AI')}</small><br>
                {chat['bot']}
            </div>
            """, unsafe_allow_html=True)

else:
    st.info("👋 Start a conversation!")

# ========================
# FULL HISTORY
# ========================
if st.session_state.show_history:
    st.markdown("---")
    st.subheader("📚 Complete History")
    
    for i, chat in enumerate(st.session_state.chat_history):
        with st.expander(f"Chat #{i+1} - {datetime.fromisoformat(chat['timestamp']).strftime('%Y-%m-%d %H:%M')}"):
            st.write("**👤 You:**", chat['user'])
            st.write("**🤖 AI:**", chat['bot'])
            if chat.get('model'):
                st.caption(f"Model: {chat['model']}")
    
    if st.button("❌ Close History", key="close_history"):
        st.session_state.show_history = False
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #6b7280;'>
    🚀 NEXUS AI Pro v2.0 | Powered by Groq | © 2026 | Made with ❤️
</div>
""", unsafe_allow_html=True)
