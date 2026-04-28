import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="🤖 NEXUS Pro AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"]  {font-family: 'Inter', sans-serif;}
.main-header {font-size: 2.5rem !important; font-weight: 700 !important; 
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin: 1rem 0;}
.chat-container {height: 70vh; overflow-y: auto; padding: 2rem;
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 20px; margin: 1rem 0; box-shadow: 0 20px 60px rgba(0,0,0,0.1);}
.message-bubble {margin: 1rem 0; padding: 1.2rem 1.5rem; border-radius: 20px; 
    max-width: 75%; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    animation: fadeInUp 0.3s ease;}
.user-message {background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white;
    margin-left: auto; border-bottom-right-radius: 5px;}
.ai-message {background: linear-gradient(135deg, #10b981, #059669); color: white;
    margin-right: auto; border-bottom-left-radius: 5px;}
.input-container {position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%);
    width: 90%; max-width: 800px; background: white; padding: 1.5rem;
    border-radius: 25px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); z-index: 1000;}
.btn-icon {border-radius: 50%; width: 45px; height: 45px; padding: 0; 
    border: none; font-size: 1.2rem; transition: all 0.3s; cursor: pointer;}
.btn-primary {background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white;}
.btn-secondary {background: #f1f5f9; color: #64748b;}
.btn-danger {background: linear-gradient(135deg, #ef4444, #dc2626); color: white;}
.header-bar {background: white; padding: 1rem 2rem; border-radius: 15px; 
    box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-bottom: 1rem;}
@keyframes fadeInUp {from {opacity: 0; transform: translateY(20px);} to {opacity: 1; transform: translateY(0);}}
.modal {display: none; position: fixed; z-index: 2000; left: 0; top: 0; 
    width: 100%; height: 100%; background-color: rgba(0,0,0,0.5);}
.modal-content {background: white; margin: 15% auto; padding: 2rem; 
    border-radius: 15px; width: 90%; max-width: 500px; text-align: center;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client(): 
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# Initialize session state
if "chat_history" not in st.session_state: 
    st.session_state.chat_history = []
if "input_key" not in st.session_state: 
    st.session_state.input_key = 0
if "last_time" not in st.session_state: 
    st.session_state.last_time = 0

def safe_time(chat):
    try: 
        return datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
    except: 
        return "Now"

def save_chat_history():
    try:
        os.makedirs("chat_history", exist_ok=True)
        fname = "chat_history/all_chats.json"
        with open(fname, "w") as f: 
            json.dump(st.session_state.chat_history, f, indent=2)
    except: 
        pass

def load_chat_history():
    try:
        fname = "chat_history/all_chats.json"
        if os.path.exists(fname):
            with open(fname, "r") as f:
                chats = json.load(f)
                for chat in chats:
                    if 'timestamp' not in chat: 
                        chat['timestamp'] = datetime.now().isoformat()
                st.session_state.chat_history = chats
                return True
    except: 
        pass
    return False

def clear_chat():
    st.session_state.chat_history = []
    save_chat_history()
    st.rerun()

def rate_limit():
    now = time.time()
    if now - st.session_state.last_time < 2: 
        st.rerun()
    st.session_state.last_time = now

def ai_respond(prompt):
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    for model in models:
        try:
            with st.spinner("🤖 Engr Babar Ali Jatoi ka AI soch raha hai..."):
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": """
You are NEXUS Pro AI - Professional AI Assistant.
Creator: Engr Babar Ali Jatoi (Pakistan)
Built with ❤️ using Streamlit + Groq AI

Jab koi puche:
- "Kaun banaya?" → "Engr Babar Ali Jatoi ne banaya!"
- "Developer?" → "Engr Babar Ali Jatoi from Pakistan"
- "Team?" → "Solo project by Engr Babar Ali Jatoi"

User ki language mein jawab do. Professional raho!
                        """},
                        {"role": "user", "content": prompt}
                    ]
                )
                return resp.choices[0].message.content, model
        except: 
            continue
    return "Kuch galat ho gaya, dobara try karo!", "Error"

# Load chat history on start
load_chat_history()

# Main Header
st.markdown('<h1 class="main-header">🤖 NEXUS Pro AI</h1>', unsafe_allow_html=True)
st.markdown("### by Engr Babar Ali Jatoi | Fast • Smart • Professional")

# Header with functional buttons
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div class="header-bar">
        <h2 style='margin: 0; color: #1e293b;'>🤖 NEXUS Pro AI</h2>
        <p style='margin: 0; color: #64748b;'>by Engr Babar Ali Jatoi • Ready to help!</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("📋 History", key="history", help="Load chat history"):
            load_chat_history()
            st.success("✅ Chat history loaded!")
            st.rerun()
    with col_btn2:
        if st.button("🗑️ Clear Chat", key="clear", help="Clear all messages"):
            if st.session_state.chat_history:
                st.session_state.chat_history = []
                save_chat_history()
                st.success("✅ Chat cleared!")
                st.rerun()
            else:
                st.warning("ℹ️ Chat already empty!")
    with col_btn3:
        if st.button("🔄 New Chat", key="new", help="Start fresh"):
            clear_chat()

# Chat Display
st.markdown('<div class="chat-container" id="messages">', unsafe_allow_html=True)

if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        col1, col2 = st.columns([3, 1]) if 'user' in chat else st.columns([1, 3])
        ts = safe_time(chat)
        
        if 'user' in chat:
            with col2:
                st.markdown(f"""
                <div class="message-bubble user-message">
                    <div style='font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.5rem;'>
                        You • {ts}
                    </div>
                    {chat['user']}
                </div>
                """, unsafe_allow_html=True)
            with col1: st.empty()
        else:
            with col1:
                st.markdown(f"""
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
    <div style='text-align: center; color: #64748b; margin-top: 8rem;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>🤖</div>
        <h3>Engr Babar Ali Jatoi ka NEXUS Pro AI</h3>
        <p>Pehla message bhejo shuru karne ke liye!</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input Area
st.markdown("""
<div class="input-container">
    <div style='display: flex; gap: 1rem; align-items: center;'>
""", unsafe_allow_html=True)

user_input = st.text_input("", key=f"inp_{st.session_state.input_key}", 
                          placeholder="Engr Babar Ali Jatoi ke AI se kuch poocho...", 
                          label_visibility="collapsed")

col_input, col_send = st.columns([5, 1])
with col_input:
    user_input = st.text_input("", key=f"inp_{st.session_state.input_key}", 
                              placeholder="Engr Babar Ali Jatoi ke AI se kuch poocho...", 
                              label_visibility="collapsed")
with col_send:
    if st.button("📤", key="send_btn", use_container_width=True, type="primary"):
        if user_input.strip():
            rate_limit()
            st.session_state.input_key += 1
            
            # Add user message with timestamp
            user_msg = {"user": user_input, "timestamp": datetime.now().isoformat()}
            st.session_state.chat_history.append(user_msg)
            save_chat_history()
            
            # Get AI response
            with st.spinner("🤖 Engr Babar Ali Jatoi ka AI..."):
                answer, model = ai_respond(user_input)
                ai_msg = {"bot": answer, "timestamp": datetime.now().isoformat()}
                st.session_state.chat_history.append(ai_msg)
                save_chat_history()
            
            st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# Auto-scroll script
st.markdown("""
<script>
const chat = document.getElementById('messages');
if (chat) {
    chat.scrollTop = chat.scrollHeight;
    const observer = new MutationObserver(() => {
        chat.scrollTop = chat.scrollHeight;
    });
    observer.observe(chat, {childList: true, subtree: true});
}
</script>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 3rem; color: #94a3b8; font-size: 0.9rem;'>
    🤖 NEXUS Pro AI • Made by Engr Babar Ali Jatoi • Powered by Groq • © 2026 Pakistan
</div>
""", unsafe_allow_html=True)
