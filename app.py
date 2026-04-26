import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq
import plotly.express as px
import plotly.graph_objects as go

# ========================
# CONFIG - Professional Theme
# ========================
st.set_page_config(
    page_title="⚡ NEXUS AI Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    .user-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .chat-bubble-user {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
    }
    .chat-bubble-bot {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
    }
    .btn-primary {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        color: white;
        transition: all 0.3s;
    }
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(59,130,246,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ========================
# LOAD API KEY
# ========================
@st.cache_resource
def init_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = init_client()

# ========================
# SESSION INIT
# ========================
if "user" not in st.session_state:
    st.session_state.user = None
if "last_time" not in st.session_state:
    st.session_state.last_time = 0
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ========================
# LOGIN SYSTEM - Enhanced
# ========================
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "User already exists!"
    users[username] = password
    with open("users.json", "w") as f:
        json.dump(users, f)
    return True, "Registration successful!"

def login():
    # Full screen login
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.markdown('<h1 class="main-header">🔐 NEXUS AI Pro</h1>', unsafe_allow_html=True)
        st.markdown("### Professional AI Assistant")
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            u = st.text_input("👤 Username", key="login_user")
            p = st.text_input("🔒 Password", type="password", key="login_pass")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚀 Login", key="login_btn", use_container_width=True):
                    users = load_users()
                    if u in users and users[u] == p:
                        st.session_state.user = u
                        st.success("✅ Login Successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
            
        with tab2:
            reg_user = st.text_input("👤 New Username", key="reg_user")
            reg_pass = st.text_input("🔒 New Password", type="password", key="reg_pass")
            reg_confirm = st.text_input("🔒 Confirm Password", type="password", key="reg_confirm")
            
            if st.button("📝 Register", key="reg_btn", use_container_width=True):
                if reg_pass != reg_confirm:
                    st.error("❌ Passwords don't match!")
                else:
                    success, msg = register_user(reg_user, reg_pass)
                    if success:
                        st.success("✅ " + msg)
                    else:
                        st.error("❌ " + msg)

if not st.session_state.user:
    login()
    st.stop()

# ========================
# MEMORY SYSTEM - Enhanced
# ========================
def memory_file():
    os.makedirs("memory", exist_ok=True)
    return f"memory/{st.session_state.user}.json"

def load_memory():
    if not os.path.exists(memory_file()):
        return []
    with open(memory_file(), "r") as f:
        return json.load(f)

def save_memory(data):
    with open(memory_file(), "w") as f:
        json.dump(data, f, indent=2)

chat_history = load_memory()

# ========================
# RATE LIMIT
# ========================
def rate_limit():
    if time.time() - st.session_state.last_time < 2:
        st.warning("⏳ Please wait 2 seconds between messages...")
        time.sleep(2)
        st.rerun()
    st.session_state.last_time = time.time()

# ========================
# ENHANCED AI MODELS
# ========================
MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant", 
    "mixtral-8x7b-32768"
]

def get_ai_response(prompt):
    for model in MODELS:
        try:
            with st.spinner(f"🤖 Thinking with {model}..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are NEXUS AI Pro - a professional, helpful, and intelligent assistant. Provide detailed, accurate responses."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content, model
        except Exception as e:
            continue
    return "⚠️ All models unavailable. Please try again.", None

# ========================
# MAIN DASHBOARD
# ========================
# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f'<h1 class="main-header">⚡ NEXUS AI Pro</h1>', unsafe_allow_html=True)

# User Dashboard
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div class="user-card">
        <h3>👋 Welcome back!</h3>
        <p><strong>User:</strong> {}</p>
        <p><strong>Session:</strong> {}</p>
        <p><strong>Total Messages:</strong> {}</p>
    </div>
    """.format(st.session_state.user, datetime.now().strftime("%Y-%m-%d %H:%M"), len(chat_history)), 
    unsafe_allow_html=True)

with col2:
    if st.button("🔄 Clear History", use_container_width=True):
        chat_history.clear()
        save_memory(chat_history)
        st.success("History cleared!")
        st.rerun()
    
    if st.button("🚪 Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💬 Total Chats", len(chat_history))
with col2:
    st.metric("🤖 AI Responses", len([c for c in chat_history if 'bot' in c]))
with col3:
    model_used = chat_history[-1].get('model', 'Unknown') if chat_history else 'None'
    st.metric("🎯 Last Model", model_used)

# ========================
# CHAT INTERFACE
# ========================
st.markdown("---")

# Send Message Button Section
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input(
        "💭 Ask NEXUS AI anything...", 
        placeholder="Type your message here...",
        label_visibility="collapsed"
    )

with col2:
    send_clicked = st.button("📤 Send", key="send_btn", use_container_width=True, help="Send message")

# History Check Button
if st.button("📋 View Full History", key="history_btn"):
    st.session_state.show_history = True

# Process Message
if send_clicked and user_input.strip():
    rate_limit()
    
    with st.spinner("NEXUS AI is thinking..."):
        answer, model_used = get_ai_response(user_input)
        
        new_chat = {
            "user": user_input,
            "bot": answer,
            "timestamp": datetime.now().isoformat(),
            "model": model_used
        }
        
        chat_history.append(new_chat)
        save_memory(chat_history)
        st.rerun()

# ========================
# CHAT DISPLAY
# ========================
if chat_history:
    st.subheader("💬 Conversation History")
    
    for i, chat in enumerate(reversed(chat_history[-20:])):  # Last 20 messages
        with st.container():
            col1, col2 = st.columns([1, 1])
            
            with col1:
                timestamp = datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
                st.markdown(f"""
                <div class="chat-bubble-user">
                    <small>{timestamp} 👤</small><br>
                    {chat['user']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if 'model' in chat:
                    st.markdown(f"""
                    <div class="chat-bubble-bot">
                        <small>{timestamp} 🤖 ({chat['model']})</small><br>
                        {chat['bot']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-bubble-bot">
                        <small>{timestamp} 🤖</small><br>
                        {chat['bot']}
                    </div>
                    """, unsafe_allow_html=True)

# ========================
# FULL HISTORY MODAL
# ========================
if 'show_history' in st.session_state and st.session_state.show_history:
    st.markdown("---")
    st.subheader("📚 Complete Chat History")
    
    # History Stats Chart
    if len(chat_history) > 1:
        df = px.data.frame({
            'message': [f"Msg {i+1}" for i in range(len(chat_history))],
            'length': [len(chat['user']) + len(chat['bot']) for chat in chat_history]
        })
        fig = px.bar(df, x='message', y='length', title="Message Length Over Time")
        st.plotly_chart(fig, use_container_width=True)
    
    # Full history display
    for chat in chat_history:
        st.write(f"**👤 {chat['user'][:50]}...**")
        st.write(f"**🤖 {chat['bot'][:100]}...**")
        st.write("---")
    
    if st.button("❌ Close History"):
        del st.session_state.show_history
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280;'>
    🚀 NEXUS AI Pro | Powered by Groq & Streamlit | © 2026
</div>
""", unsafe_allow_html=True)
