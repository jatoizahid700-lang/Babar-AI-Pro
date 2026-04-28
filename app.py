import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="🤖 NEXUS Pro AI", page_icon="🤖", layout="wide")

# -------------------- CUSTOM CSS --------------------
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
.btn-primary {background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white;}
.header-bar {background: white; padding: 1rem 2rem; border-radius: 15px; 
    box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-bottom: 1rem;}
@keyframes fadeInUp {from {opacity: 0; transform: translateY(20px);} to {opacity: 1; transform: translateY(0);}}
</style>
""", unsafe_allow_html=True)

# -------------------- CLIENT --------------------
@st.cache_resource
def get_client(): 
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# -------------------- SESSION STATE --------------------
if "chat_history" not in st.session_state: 
    st.session_state.chat_history = []
if "last_time" not in st.session_state: 
    st.session_state.last_time = 0
if "processing" not in st.session_state:
    st.session_state.processing = False

# -------------------- HELPERS --------------------
def safe_time(chat):
    try: 
        return datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
    except: 
        return "Now"

def save_chat_history():
    os.makedirs("chat_history", exist_ok=True)
    fname = "chat_history/all_chats.json"
    with open(fname, "w") as f: 
        json.dump(st.session_state.chat_history, f, indent=2)

def load_chat_history():
    fname = "chat_history/all_chats.json"
    if os.path.exists(fname):
        with open(fname, "r") as f:
            chats = json.load(f)
            for chat in chats:
                if 'timestamp' not in chat: 
                    chat['timestamp'] = datetime.now().isoformat()
            st.session_state.chat_history = chats
            return True
    return False

def clear_chat():
    st.session_state.chat_history = []
    save_chat_history()
    st.rerun()

def rate_limit():
    now = time.time()
    if now - st.session_state.last_time < 2: 
        st.warning("⏳ Slow down! Please wait a moment...")
        st.stop()
    st.session_state.last_time = now

def ai_respond(prompt):
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    for model in models:
        try:
            with st.spinner("🤖 NEXUS Pro AI soch raha hai..."):
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
                return resp.choices[0].message.content
        except: 
            continue
    return "⚠️ Kuch galat ho gaya, dobara try karo!"

# -------------------- LOAD HISTORY --------------------
load_chat_history()

# -------------------- HEADER --------------------
st.markdown('<h1 class="main-header">🤖 NEXUS Pro AI</h1>', unsafe_allow_html=True)
st.markdown("### by Engr Babar Ali Jatoi | Fast • Smart • Professional")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div class="header-bar">
        <h2 style='margin: 0; color: #1e293b;'>🤖 NEXUS Pro AI</h2>
        <p style='margin: 0; color: #64748b;'>by Engr Babar Ali Jatoi • Ready to help!</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    if st.button("📋 History"):
        if load_chat_history():
            st.success("✅ Chat history loaded!")
        else:
            st.warning("ℹ️ No saved history found!")
        st.rerun()
    if st.button("🗑️ Clear"):
        clear_chat()
    if st.button("🔄 New"):
        st.session_state.chat_history = []
        save_chat_history()
        st.success("✅ New chat started!")
        st.rerun()

# -------------------- CHAT DISPLAY --------------------
st.markdown('<div class="chat-container" id="chat_messages">', unsafe_allow_html=True)
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        ts = safe_time(chat)
        if 'user' in chat:
            st.markdown(f"""
            <div class="message-bubble user-message">
                <div style='font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.5rem;'>
                    You • {ts}
                </div>
                {chat['user']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-bubble ai-message">
                <div style='font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.5rem;'>
                    NEXUS Pro AI • {ts}
                </div>
                {chat['bot']}
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align: center; color: #64748b; margin-top: 8rem;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>🤖</div>
        <h3>Engr Babar Ali Jatoi ka NEXUS Pro AI</h3>
        <p>Pehla message bhejo shuru karne ke liye!</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- INPUT AREA --------------------
if not st.session_state.processing:
    user_input = st.text_input(
        "Type your message here...", 
        key="main_input",
        placeholder="Engr Babar Ali Jatoi ke AI se kuch poocho...", 
        label_visibility="collapsed"
    )
    if st.button("📤 Send", use_container_width=True):
        if user_input.strip():
            st.session_state.processing = True
            rate_limit()
            st.session_state.chat_history.append({"user": user
