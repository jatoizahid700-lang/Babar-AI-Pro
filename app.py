import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq
import hashlib

# Page Configuration
st.set_page_config(
    page_title="NEXUS Pro AI - Professional Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Ultra Professional Design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}

/* Main Container */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-right: 1px solid rgba(255,255,255,0.1);
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Chat Container */
.chat-container {
    height: calc(100vh - 180px);
    overflow-y: auto;
    padding: 2rem;
    background: transparent;
    scroll-behavior: smooth;
}

/* Message Styling */
.message-wrapper {
    margin-bottom: 1.5rem;
    animation: slideIn 0.3s ease;
}

.user-wrapper {
    display: flex;
    justify-content: flex-end;
}

.ai-wrapper {
    display: flex;
    justify-content: flex-start;
}

.message-bubble {
    max-width: 75%;
    padding: 1rem 1.5rem;
    border-radius: 20px;
    position: relative;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.user-bubble {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    border-bottom-right-radius: 5px;
}

.ai-bubble {
    background: rgba(255,255,255,0.95);
    color: #1e293b;
    border-bottom-left-radius: 5px;
    backdrop-filter: blur(10px);
}

.message-time {
    font-size: 0.7rem;
    opacity: 0.7;
    margin-top: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.message-actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 0.5rem;
}

.action-icon {
    background: rgba(0,0,0,0.1);
    border: none;
    padding: 0.25rem 0.5rem;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.7rem;
    transition: all 0.2s;
    color: inherit;
}

.action-icon:hover {
    background: rgba(0,0,0,0.2);
    transform: translateY(-2px);
}

/* Input Container */
.input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(30,41,59,0.95);
    backdrop-filter: blur(20px);
    padding: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    z-index: 1000;
}

.input-wrapper {
    max-width: 1000px;
    margin: 0 auto;
    display: flex;
    gap: 1rem;
    align-items: center;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 30px !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.3) !important;
}

.send-button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    border: none;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}

.send-button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(59,130,246,0.4);
}

/* Header */
.header-main {
    background: rgba(30,41,59,0.95);
    backdrop-filter: blur(10px);
    padding: 1rem 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 1rem;
}

/* Buttons */
.custom-btn {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s;
    width: 100%;
    margin: 0.25rem 0;
}

.custom-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(59,130,246,0.3);
}

.danger-btn {
    background: linear-gradient(135deg, #ef4444, #dc2626);
}

/* Toast Notification */
.toast {
    position: fixed;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
    background: #10b981;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    z-index: 2000;
    animation: fadeOut 2s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.toast-error {
    background: #ef4444;
}

/* Typing Indicator */
.typing {
    display: inline-flex;
    gap: 4px;
    padding: 0.5rem 1rem;
    background: rgba(255,255,255,0.1);
    border-radius: 20px;
}

.typing span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #3b82f6;
    animation: typing 1.4s infinite;
}

@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeOut {
    0% { opacity: 1; }
    70% { opacity: 1; }
    100% { opacity: 0; visibility: hidden; }
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #1e293b;
}

::-webkit-scrollbar-thumb {
    background: #3b82f6;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #1d4ed8;
}

/* Welcome Screen */
.welcome-screen {
    text-align: center;
    padding: 4rem;
    color: white;
}

/* Stats Card */
.stats-card {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 1rem;
    margin: 0.5rem 0;
    text-align: center;
}

/* Loading Spinner */
.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>

<script>
// JavaScript functions for copy and read
function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
    showToast('✅ Copied to clipboard!');
}

function readMessage(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        utterance.pitch = 1;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
        showToast('🔊 Reading message...');
    } else {
        showToast('❌ Text-to-speech not supported', true);
    }
}

function showToast(msg, isError = false) {
    const toast = document.createElement('div');
    toast.className = 'toast' + (isError ? ' toast-error' : '');
    toast.innerHTML = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

// Auto scroll to bottom
function scrollToBottom() {
    const container = document.querySelector('.chat-container');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}
setInterval(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)

# Initialize Groq Client
@st.cache_resource
def init_groq():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = init_groq()

# Session State
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "last_msg_time" not in st.session_state:
    st.session_state.last_msg_time = 0
if "toast_msg" not in st.session_state:
    st.session_state.toast_msg = None

# Helper Functions
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_toast(msg, is_error=False):
    st.session_state.toast_msg = {"msg": msg, "error": is_error}

def get_time():
    return datetime.now().strftime("%I:%M %p")

def load_users():
    try:
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def load_chat():
    os.makedirs("chats", exist_ok=True)
    try:
        fname = f"chats/{st.session_state.user}.json"
        if os.path.exists(fname):
            with open(fname, "r") as f:
                return json.load(f)
    except:
        pass
    return []

def save_chat(data):
    try:
        fname = f"chats/{st.session_state.user}.json"
        with open(fname, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

def rate_limit_check():
    now = time.time()
    if now - st.session_state.last_msg_time < 2:
        show_toast("⚠️ Please wait 2 seconds between messages!", True)
        return False
    st.session_state.last_msg_time = now
    return True

def get_ai_response(prompt):
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are NEXUS Pro AI - Professional AI Assistant
                        Created by: Engr Babar Ali Jatoi (Pakistan)
                        Features: Fast responses, Professional tone, Multi-language support
                        
                        Guidelines:
                        - Respond in user's language
                        - Be helpful and professional
                        - If asked about creator: "Engr Babar Ali Jatoi from Pakistan"
                        - Keep responses concise but informative"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content, model
        except:
            continue
    
    return "⚠️ Service is busy. Please try again in a moment.", "error"

def clear_all_chat():
    st.session_state.chat_history = []
    if st.session_state.user:
        save_chat([])
    show_toast("🗑️ Chat cleared successfully!")

def delete_user_account():
    users = load_users()
    if st.session_state.user in users:
        del users[st.session_state.user]
        save_users(users)
        
        chat_file = f"chats/{st.session_state.user}.json"
        if os.path.exists(chat_file):
            os.remove(chat_file)
        
        st.session_state.user = None
        st.session_state.chat_history = []
        show_toast("✅ Account deleted successfully!")

# Login/Signup Screen
if not st.session_state.user:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: rgba(30,41,59,0.95); border-radius: 20px; padding: 2.5rem; margin-top: 3rem; backdrop-filter: blur(10px);">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 4rem;">🤖</div>
                <h1 style="color: white;">NEXUS Pro AI</h1>
                <p style="color: #94a3b8;">by Engr Babar Ali Jatoi</p>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            login_user = st.text_input("Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True):
                users = load_users()
                if login_user in users and users[login_user] == hash_pass(login_pass):
                    st.session_state.user = login_user
                    st.session_state.chat_history = load_chat()
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
        
        with tab2:
            reg_user = st.text_input("Username", key="reg_user")
            reg_pass = st.text_input("Password", type="password", key="reg_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")
            if st.button("Register", use_container_width=True):
                if reg_user and reg_pass and confirm_pass:
                    if reg_pass == confirm_pass:
                        users = load_users()
                        if reg_user not in users:
                            users[reg_user] = hash_pass(reg_pass)
                            save_users(users)
                            st.success("✅ Account created! Please login.")
                        else:
                            st.error("❌ Username already exists!")
                    else:
                        st.error("❌ Passwords don't match!")
                else:
                    st.error("❌ Please fill all fields!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Main App Interface
# Header
st.markdown(f"""
<div class="header-main">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="color: white; margin: 0;">🤖 NEXUS Pro AI</h2>
            <p style="color: #94a3b8; margin: 0;">Welcome, {st.session_state.user}</p>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <span style="background: #10b981; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem;">
                ● Active
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("---")
    
    # Stats
    total_msgs = len(st.session_state.chat_history)
    st.markdown(f"""
    <div class="stats-card">
        <div style="font-size: 2rem; font-weight: bold;">{total_msgs//2}</div>
        <div style="font-size: 0.85rem;">Total Conversations</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action Buttons
    if st.button("📋 Chat History", use_container_width=True):
        if st.session_state.chat_history:
            st.info(f"📊 You have {total_msgs//2} messages")
        else:
            st.info("No chat history yet")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        clear_all_chat()
        st.rerun()
    
    if st.button("💾 Export Chat", use_container_width=True):
        if st.session_state.chat_history:
            export_data = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                "📥 Download JSON",
                export_data,
                f"nexus_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )
    
    st.markdown("---")
    
    # Settings
    with st.expander("⚙️ Preferences"):
        st.caption("AI Settings")
        ai_temp = st.slider("Response Creativity", 0.0, 1.0, 0.7, 0.1)
        st.caption(f"Current: {ai_temp}")
    
    st.markdown("---")
    
    # Account
    if st.button("👤 My Profile", use_container_width=True):
        st.info(f"User: {st.session_state.user}\nMember since: {datetime.now().strftime('%Y-%m-%d')}")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.chat_history = []
        st.rerun()
    
    if st.button("⚠️ Delete Account", use_container_width=True, type="secondary"):
        delete_user_account()
        st.rerun()
    
    st.markdown("---")
    st.caption("© 2026 NEXUS Pro AI")
    st.caption("Made with ❤️ in Pakistan")

# Chat Area
chat_placeholder = st.container()
with chat_placeholder:
    st.markdown('<div class="chat-container" id="chatArea">', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for i in range(0, len(st.session_state.chat_history), 2):
            if i + 1 < len(st.session_state.chat_history):
                user_msg = st.session_state.chat_history[i]
                ai_msg = st.session_state.chat_history[i+1]
                
                # User Message
                st.markdown(f"""
                <div class="message-wrapper user-wrapper">
                    <div class="message-bubble user-bubble">
                        <div>{user_msg.get('text', '')}</div>
                        <div class="message-time">
                            <span>{user_msg.get('time', get_time())}</span>
                            <div class="message-actions">
                                <button class="action-icon" onclick="copyToClipboard(`{user_msg.get('text', '').replace('`', '\\`')}`)">📋 Copy</button>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # AI Message
                st.markdown(f"""
                <div class="message-wrapper ai-wrapper">
                    <div class="message-bubble ai-bubble">
                        <div>{ai_msg.get('text', '')}</div>
                        <div class="message-time">
                            <span>🤖 NEXUS • {ai_msg.get('time', get_time())}</span>
                            <div class="message-actions">
                                <button class="action-icon" onclick="copyToClipboard(`{ai_msg.get('text', '').replace('`', '\\`')}`)">📋 Copy</button>
                                <button class="action-icon" onclick="readMessage(`{ai_msg.get('text', '').replace('`', '\\`')}`)">🔊 Read</button>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="welcome-screen">
            <div style="font-size: 5rem;">💬</div>
            <h2>Welcome to NEXUS Pro AI</h2>
            <p>Your professional AI assistant by Engr Babar Ali Jatoi</p>
            <p style="font-size: 0.85rem; color: #94a3b8;">Start typing to begin conversation</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

user_message = st.text_input(
    "",
    key=f"msg_input_{st.session_state.input_key}",
    placeholder="Ask NEXUS Pro AI anything... (Press Enter to send)",
    label_visibility="collapsed"
)

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 8])
with col_btn2:
    send_clicked = st.button("📤", key="send_btn", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Handle Message Sending
if (send_clicked or (user_message and user_message.strip())) and user_message and user_message.strip():
    if rate_limit_check():
        # Add user message
        st.session_state.chat_history.append({
            "text": user_message,
            "time": get_time()
        })
        save_chat(st.session_state.chat_history)
        
        # Get AI response
        with st.spinner("🤖 NEXUS Pro AI is thinking..."):
            ai_response, model_used = get_ai_response(user_message)
            
            # Add AI response
            st.session_state.chat_history.append({
                "text": ai_response,
                "time": get_time()
            })
            save_chat(st.session_state.chat_history)
        
        # Clear input and refresh
        st.session_state.input_key += 1
        st.rerun()

# Show Toast Messages
if st.session_state.toast_msg:
    st.markdown(f"""
    <div class="toast {'toast-erro
