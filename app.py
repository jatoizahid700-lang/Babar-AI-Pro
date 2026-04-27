import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq
import hashlib

st.set_page_config(
    page_title="NEXUS Pro AI - Enterprise Edition",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Ultra Professional Look
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Main Container */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Sidebar Styling */
.css-1d391kg {
    background: rgba(255, 255, 255, 0.98) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(0,0,0,0.05);
}

/* Main Content */
.main-content {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    border-radius: 0;
}

/* Header */
.pro-header {
    background: white;
    padding: 1rem 2rem;
    border-radius: 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    position: sticky;
    top: 0;
    z-index: 100;
}

/* Chat Container */
.chat-messages {
    height: calc(100vh - 200px);
    overflow-y: auto;
    padding: 2rem;
    background: transparent;
    scroll-behavior: smooth;
}

/* Message Bubbles */
.message {
    margin-bottom: 1.5rem;
    display: flex;
    animation: slideIn 0.3s ease;
}

.message.user {
    justify-content: flex-end;
}

.message.ai {
    justify-content: flex-start;
}

.message-content {
    max-width: 70%;
    padding: 1rem 1.5rem;
    border-radius: 20px;
    position: relative;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.user .message-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 5px;
}

.ai .message-content {
    background: white;
    color: #1e293b;
    border-bottom-left-radius: 5px;
    border: 1px solid #e2e8f0;
}

.message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    font-size: 0.75rem;
    opacity: 0.7;
}

.message-text {
    line-height: 1.5;
    font-size: 0.95rem;
    word-wrap: break-word;
}

.message-actions {
    margin-top: 0.5rem;
    display: flex;
    gap: 0.5rem;
    justify-content: flex-end;
}

.action-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0.25rem 0.5rem;
    border-radius: 6px;
    font-size: 0.75rem;
    transition: all 0.2s;
    color: inherit;
    opacity: 0.6;
}

.action-btn:hover {
    opacity: 1;
    background: rgba(0,0,0,0.1);
}

/* Input Area */
.input-area {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 1.5rem;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
    z-index: 1000;
}

.input-wrapper {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    gap: 1rem;
    align-items: center;
}

.input-field {
    flex: 1;
    padding: 1rem 1.5rem;
    border: 2px solid #e2e8f0;
    border-radius: 30px;
    font-size: 1rem;
    transition: all 0.3s;
    background: white;
}

.input-field:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
}

.send-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.send-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(102,126,234,0.4);
}

.send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Sidebar Elements */
.sidebar-header {
    text-align: center;
    padding: 1rem;
    border-bottom: 2px solid #f1f5f9;
    margin-bottom: 1rem;
}

.stat-card {
    background: #f8fafc;
    padding: 1rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    text-align: center;
}

.stat-number {
    font-size: 1.5rem;
    font-weight: bold;
    color: #667eea;
}

/* Toast Notification */
.toast-notification {
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
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.toast-error {
    background: #ef4444;
}

/* Loading Animation */
.loading-dots {
    display: inline-flex;
    gap: 4px;
}

.loading-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #667eea;
    animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
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
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #764ba2;
}

/* Button Styles */
.pro-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s;
    width: 100%;
    margin: 0.25rem 0;
}

.pro-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102,126,234,0.4);
}

.danger-btn {
    background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);
}

/* Typing Indicator */
.typing-indicator {
    background: white;
    padding: 0.75rem 1.5rem;
    border-radius: 20px;
    display: inline-flex;
    gap: 4px;
    margin-bottom: 1rem;
}

.typing-indicator span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #667eea;
    animation: typing 1.4s infinite ease-in-out;
}

@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
}
</style>
""", unsafe_allow_html=True)

# Initialize Groq Client
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# Session State Initialization
def init_session():
    defaults = {
        "user": None,
        "chat_history": [],
        "input_key": 0,
        "last_time": 0,
        "toast_msg": None,
        "is_typing": False,
        "sidebar_state": "expanded"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# Helper Functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_toast(msg, is_error=False):
    st.session_state.toast_msg = {"msg": msg, "error": is_error}

def safe_time(timestamp):
    try:
        return datetime.fromisoformat(timestamp).strftime("%I:%M %p")
    except:
        return datetime.now().strftime("%I:%M %p")

def load_users():
    try:
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def load_memory():
    os.makedirs("memory", exist_ok=True)
    try:
        fname = f"memory/{st.session_state.user}.json"
        if os.path.exists(fname):
            with open(fname, "r") as f:
                chats = json.load(f)
                for chat in chats:
                    if 'timestamp' not in chat:
                        chat['timestamp'] = datetime.now().isoformat()
                return chats
    except:
        pass
    return []

def save_memory(data):
    try:
        fname = f"memory/{st.session_state.user}.json"
        with open(fname, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

def rate_limit():
    now = time.time()
    if now - st.session_state.last_time < 2:
        show_toast("Please wait 2 seconds between messages!", True)
        return False
    st.session_state.last_time = now
    return True

def ai_respond(prompt):
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    for model in models:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": """
You are NEXUS Pro AI - Enterprise Grade AI Assistant
Creator: Engr Babar Ali Jatoi (Pakistan)
Built with: Streamlit + Groq AI Cloud

Guidelines:
- Respond professionally in user's language
- Be helpful, accurate, and concise
- If asked about creator: "Engr Babar Ali Jatoi from Pakistan"
- If asked about capabilities: List all features professionally
- Maintain enterprise-level response quality
                    """},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return resp.choices[0].message.content, model
        except Exception as e:
            continue
    return "⚠️ Service temporarily unavailable. Please try again.", "Error"

def clear_chat():
    st.session_state.chat_history = []
    if st.session_state.user:
        save_memory([])
    show_toast("Chat cleared successfully!")

def delete_account():
    users = load_users()
    if st.session_state.user in users:
        del users[st.session_state.user]
        with open("users.json", "w") as f:
            json.dump(users, f)
        
        memory_file = f"memory/{st.session_state.user}.json"
        if os.path.exists(memory_file):
            os.remove(memory_file)
        
        st.session_state.user = None
        st.session_state.chat_history = []
        show_toast("Account deleted successfully!")

# Login/Signup Section
if not st.session_state.user:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 20px; padding: 2rem; margin-top: 3rem; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
            <div style="text-align: center; margin-bottom: 2rem;">
                <div style="font-size: 4rem;">🎯</div>
                <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">NEXUS Pro AI</h1>
                <p style="color: #64748b;">Enterprise AI Assistant by Engr Babar Ali Jatoi</p>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True):
                users = load_users()
                hashed_pass = hash_password(password)
                if username in users and users[username] == hashed_pass:
                    st.session_state.user = username
                    st.session_state.chat_history = load_memory()
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
        
        with tab2:
            new_user = st.text_input("Username", key="signup_user")
            new_pass = st.text_input("Password", type="password", key="signup_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")
            if st.button("Sign Up", use_container_width=True):
                if new_user and new_pass and confirm_pass:
                    if new_pass == confirm_pass:
                        users = load_users()
                        if new_user not in users:
                            users[new_user] = hash_password(new_pass)
                            with open("users.json", "w") as f:
                                json.dump(users, f)
                            st.success("Account created! Please login.")
                        else:
                            st.error("Username already exists!")
                    else:
                        st.error("Passwords don't match!")
                else:
                    st.error("Please fill all fields!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Main App - Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div style="font-size: 3rem;">🎯</div>
        <h3>NEXUS Pro AI</h3>
        <p style="color: #64748b; font-size: 0.8rem;">Enterprise Edition</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Stats
    total_msgs = len(st.session_state.chat_history)
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_msgs}</div>
        <div>Total Messages</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Buttons
    if st.button("📋 View History", use_container_width=True):
        if st.session_state.chat_history:
            st.info(f"📊 You have {total_msgs//2} conversations")
        else:
            st.info("No chat history yet")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()
    
    if st.button("📊 Export Chat", use_container_width=True):
        if st.session_state.chat_history:
            export_data = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button("Download JSON", export_data, "nexus_chat_history.json", "application/json")
    
    st.markdown("---")
    
    # Settings
    with st.expander("⚙️ Settings"):
        temp = st.slider("AI Creativity", 0.0, 1.0, 0.7, 0.1)
        st.caption(f"Current: {temp}")
        
        if st.button("💾 Save Settings"):
            show_toast("Settings saved!")
    
    st.markdown("---")
    
    if st.button("👤 Profile"):
        st.info(f"User: {st.session_state.user}")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.chat_history = []
        st.rerun()
    
    if st.button("⚠️ Delete Account", use_container_width=True):
        delete_account()
        st.rerun()
    
    st.markdown("---")
    st.caption(f"© 2026 NEXUS Pro AI\nby Engr Babar Ali Jatoi\nPakistan")

# Main Chat Area
st.markdown(f"""
<div class="pro-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="margin: 0;">🤖 NEXUS Pro AI</h2>
            <p style="margin: 0; color: #64748b;">Welcome back, {st.session_state.user}</p>
        </div>
        <div style="display: flex; gap: 1rem;">
            <span style="background: #10b981; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem;">● Online</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Messages Container
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-messages" id="chatMessages">', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for i in range(0, len(st.session_state.chat_history), 2):
            if i+1 < len(st.session_state.chat_history):
                user_msg = st.session_state.chat_history[i]
                ai_msg = st.session_state.chat_history[i+1]
                
                # User Message
                st.markdown(f"""
                <div class="message user">
                    <div class="message-content">
                        <div class="message-header">
                            <span>👤 {st.session_state.user}</span>
                            <span>{safe_time(user_msg.get('timestamp', ''))}</span>
                        </div>
                        <div class="message-text">{user_msg.get('user', '')}</div>
                        <div class="message-actions">
                            <button class="action-btn" onclick="copyToClipboard('{user_msg.get('user', '').replace("'", "\\'")}')">📋 Copy</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # AI Message
                st.markdown(f"""
                <div class="message ai">
                    <div class="message-content">
                        <div class="message-header">
                            <span>🤖 NEXUS Pro AI</span>
                            <span>{safe_time(ai_msg.get('timestamp', ''))}</span>
                        </div>
                        <div class="message-text">{ai_msg.get('bot', '')}</div>
                        <div class="message-actions">
                            <button class="action-btn" onclick="copyToClipboard('{ai_msg.get('bot', '').replace("'", "\\'")}')">📋 Copy</button>
                            <button class="action-btn" onclick="speakText('{ai_msg.get('bot', '').replace("'", "\\'")}')">🔊 Read</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 4rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">💬</div>
            <h3>Welcome to NEXUS Pro AI</h3>
            <p>Start a conversation with Engr Babar Ali Jatoi's AI Assistant</p>
            <p style="color: #64748b;">Enterprise-grade AI at your fingertips</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input Area
st.markdown("""
<div class="input-area">
    <div class="input-wrapper">
        <input type="text" class="input-field" id="userInput" placeholder="Ask NEXUS Pro AI anything..." autocomplete="off">
        <button class="send-btn" id="sendBtn">📤</button>
    </div>
</div>

<script>
function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
    showToast('Copied to clipboard! 📋');
}

function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.9;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
        showToast('Reading message... 🔊');
    } else {
        showToast('Text-to-speech not supported', true);
    }
}

function showToast(msg, isError = false) {
    const toast = document.createElement('div');
    toast.className = 'toast-notification' + (isError ? ' toast-error' : '');
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

// Auto-scroll
function scrollToBottom() {
    const container = document.querySelector('.chat-messages');
    if (container) container.scrollTop = container.scrollHeight;
}
scrollToBottom();
setInterval(scrollToBottom, 100);

// Send message on Enter
document.getElementById('userInput')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('sendBtn').click();
    }
});
</script>
""", unsafe_allow_html=True)

# Handle input via Streamlit
user_input = st.text_input("", key=f"input_{st.session_state.input_key}", label_visibility="collapsed")

col1, col2, col3 = st.columns([1, 1, 10])
with col2:
    if st.button("📤", key="send_message"):
        if user_input and user_input.strip():
            if rate_limit():
                # Add user message
                st.sess
