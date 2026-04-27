import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="NEXUS Pro AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {font-family: 'Inter', sans-serif;}

.main-header {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin: 1rem 0;
}

/* Chat Container */
.chat-container {
    height: calc(100vh - 250px);
    overflow-y: auto;
    padding: 1.5rem;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 24px;
    margin: 0.5rem 0 1rem 0;
    scroll-behavior: smooth;
}

/* Message Bubbles */
.message-group {
    margin: 1rem 0;
    display: flex;
    flex-direction: column;
}

.user-wrapper {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 0.5rem;
}

.ai-wrapper {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 0.5rem;
}

.message-bubble {
    max-width: 70%;
    padding: 1rem 1.25rem;
    border-radius: 20px;
    position: relative;
    animation: slideIn 0.3s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 5px;
}

.ai-message {
    background: white;
    color: #1e293b;
    border-bottom-left-radius: 5px;
    border: 1px solid #e2e8f0;
}

.message-time {
    font-size: 0.7rem;
    opacity: 0.7;
    margin-top: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.copy-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 0.8rem;
    padding: 0 0.25rem;
    border-radius: 4px;
    transition: all 0.2s;
}

.copy-btn:hover {
    background: rgba(0,0,0,0.1);
}

/* Input Container */
.input-container {
    position: fixed;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    width: 85%;
    max-width: 900px;
    background: white;
    padding: 1rem;
    border-radius: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    z-index: 1000;
    border: 1px solid rgba(102,126,234,0.3);
}

.input-wrapper {
    display: flex;
    gap: 0.75rem;
    align-items: center;
}

.stTextInput > div > div > input {
    border-radius: 25px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 0.75rem 1.25rem !important;
    font-size: 1rem !important;
    transition: all 0.3s !important;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.1) !important;
}

.send-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    font-size: 1.2rem;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.send-button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(102,126,234,0.4);
}

/* Header */
.header-bar {
    background: white;
    padding: 1rem 1.5rem;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

.icon-btn {
    background: #f1f5f9;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
}

.icon-btn:hover {
    background: #e2e8f0;
    transform: translateY(-2px);
}

.sidebar-links {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
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

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* Toast Message */
.toast {
    position: fixed;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
    background: #10b981;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    z-index: 2000;
    animation: fadeOut 2s ease;
}

@keyframes fadeOut {
    0% { opacity: 1; }
    70% { opacity: 1; }
    100% { opacity: 0; visibility: hidden; }
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# Session state initialization
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
if "last_time" not in st.session_state:
    st.session_state.last_time = 0
if "toast_msg" not in st.session_state:
    st.session_state.toast_msg = None

def show_toast(msg):
    st.session_state.toast_msg = msg

def safe_time(chat):
    try:
        return datetime.fromisoformat(chat['timestamp']).strftime("%I:%M %p")
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
        return False
    st.session_state.last_time = now
    return True

def ai_respond(prompt):
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    for model in models:
        try:
            with st.spinner("🤖 NEXUS Pro AI is thinking..."):
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": """
You are NEXUS Pro AI - A Professional AI Assistant.
Creator: Engr Babar Ali Jatoi from Pakistan
Built with Streamlit + Groq AI

Response Guidelines:
- Respond in the user's language
- Be professional, helpful, and concise
- If asked about creator: "Engr Babar Ali Jatoi from Pakistan"
- If asked about developer: "Engr Babar Ali Jatoi (Pakistan)"
- Maintain a friendly yet professional tone
                        """},
                        {"role": "user", "content": prompt}
                    ]
                )
                return resp.choices[0].message.content, model
        except:
            continue
    return "⚠️ Service temporarily unavailable. Please try again.", "Error"

def clear_chat():
    st.session_state.chat_history = []
    if st.session_state.user:
        save_memory([])
    show_toast("Chat cleared successfully!")

def copy_message(text):
    st.write(f"📋 Copied to clipboard: {text[:50]}...")
    show_toast("Copied to clipboard!")

# Login/Signup Section
if not st.session_state.user:
    st.markdown('<h1 class="main-header">🤖 NEXUS Pro AI</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>by Engr Babar Ali Jatoi | Pakistan</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔐 Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("🚀 Login", use_container_width=True):
            users = load_users()
            if username in users and users[username] == password:
                st.session_state.user = username
                st.session_state.chat_history = load_memory()
                st.rerun()
            else:
                st.error("❌ Invalid credentials!")
    
    with col2:
        st.markdown("### 📝 Sign Up")
        new_user = st.text_input("Username", key="signup_user")
        new_pass = st.text_input("Password", type="password", key="signup_pass")
        if st.button("✨ Sign Up", use_container_width=True):
            users = load_users()
            if new_user and new_pass:
                if new_user not in users:
                    users[new_user] = new_pass
                    with open("users.json", "w") as f:
                        json.dump(users, f)
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("❌ Username already exists!")
            else:
                st.error("❌ Please fill all fields!")
    st.stop()

# Main App Interface
# Header with buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(f"""
    <div class="header-bar">
        <h2 style='margin: 0; color: #1e293b;'>🤖 NEXUS Pro AI</h2>
        <p style='margin: 0; color: #64748b;font-size:0.85rem;'>
            Welcome, {st.session_state.user} | by Engr Babar Ali Jatoi
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 History", use_container_width=True):
        if st.session_state.chat_history:
            st.info(f"Total {len(st.session_state.chat_history)//2} conversations")
        else:
            st.info("No chat history yet")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    col_clear, col_logout = st.columns(2)
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            clear_chat()
            st.rerun()
    with col_logout:
        if st.button("🚪 Exit", use_container_width=True):
            st.session_state.user = None
            st.session_state.chat_history = []
            st.rerun()

# Chat Container
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container" id="chatBox">', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for i in range(0, len(st.session_state.chat_history), 2):
            if i+1 < len(st.session_state.chat_history):
                user_msg = st.session_state.chat_history[i]
                ai_msg = st.session_state.chat_history[i+1]
                
                # User Message
                st.markdown(f"""
                <div class="user-wrapper">
                    <div class="message-bubble user-message">
                        <div>{user_msg.get('user', '')}</div>
                        <div class="message-time">
                            <span>{safe_time(user_msg)}</span>
                            <button class="copy-btn" onclick="navigator.clipboard.writeText(`{user_msg.get('user', '')}`)">📋</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # AI Message
                st.markdown(f"""
                <div class="ai-wrapper">
                    <div class="message-bubble ai-message">
                        <div>{ai_msg.get('bot', '')}</div>
                        <div class="message-time">
                            <span>🤖 NEXUS • {safe_time(ai_msg)}</span>
                            <button class="copy-btn" onclick="navigator.clipboard.writeText(`{ai_msg.get('bot', '')}`)">📋 Copy</button>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align: center; padding: 4rem; color: #64748b;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>💬</div>
            <h3>Welcome to NEXUS Pro AI</h3>
            <p>Start a conversation with Engr Babar Ali Jatoi's AI Assistant</p>
            <p style='font-size:0.85rem;'>Powered by Groq Cloud • Ultra Fast Responses</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input Section
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    col_input, col_send = st.columns([6, 1])
    
    with col_input:
        user_input = st.text_input(
            "",
            key=f"msg_{st.session_state.input_key}",
            placeholder="Ask NEXUS Pro AI anything...",
            label_visibility="collapsed"
        )
    
    with col_send:
        send_clicked = st.button("📤", key="send_btn", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if send_clicked and user_input.strip():
        if rate_limit():
            # Add user message
            new_user_msg = {
                "user": user_input,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.chat_history.append(new_user_msg)
            save_memory(st.session_state.chat_history)
            
            # Get AI response
            answer, model_used = ai_respond(user_input)
            
            # Add AI response
            new_ai_msg = {
                "bot": answer,
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.chat_history.append(new_ai_msg)
            save_memory(st.session_state.chat_history)
            
            # Reset input
            st.session_state.input_key += 1
            st.rerun()
        else:
            show_toast("Please wait 2 seconds between messages!")

# Toast message
if st.session_state.toast_msg:
    st.markdown(f'<div class="toast">{st.session_state.toast_msg}</div>', unsafe_allow_html=True)
    time.sleep(0.1)
    st.session_state.toast_msg = None

# Auto-scroll JavaScript
st.markdown("""
<script>
function scrollToBottom() {
    const chatContainer = document.querySelector('.chat-container');
    if(chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}
scrollToBottom();
setInterval(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem 1rem 1rem 1rem; color: #94a3b8; font-size: 0.8rem;'>
    <p>🤖 NEXUS Pro AI • Created by Engr Babar Ali Jatoi (Pakistan)</p>
    <p>Powered by Groq AI • Built with Streamlit • Real-time Conversations</p>
    <p>© 2026 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
