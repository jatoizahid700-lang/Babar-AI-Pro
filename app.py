import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(
    page_title="NEXUS Pro AI",
    page_icon="🤖",
    layout="centered"
)

# --- PREMIUM DARK THEME ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap');

.stApp { background-color: #0f1116; }
header, [data-testid="stHeader"] { background: #0f1116!important; }

/* Hide default menu */
#MainMenu, footer {visibility: hidden;}

/* Main container */
.block-container { padding-top: 1rem!important; max-width: 800px!important; }

/* Header */
.app-header {
    display: flex; justify-content: space-between; align-items: center;
    background: #1a1d27; padding: 12px 20px; border-radius: 14px;
    border: 1px solid #252a3a; margin-bottom: 20px;
}
.app-header h2 { margin: 0; color: white; font-size: 1.1rem; font-weight: 700; }
.app-header p { margin: 0; color: #8b92a8; font-size: 0.8rem; }

/* Chat bubbles - NUXUS screenshot style fixed */
.chat-bubble {
    padding: 14px 18px; border-radius: 22px; margin: 12px 0;
    max-width: 80%; line-height: 1.5; font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2); animation: slideUp 0.3s ease;
}
.user-bubble {
    background: linear-gradient(135deg, #2f6bff, #204ac8);
    color: white; margin-left: auto; border-bottom-right-radius: 6px;
}
.ai-bubble {
    background: #1ec27f; background: linear-gradient(135deg, #19b975, #129e65);
    color: white; margin-right: auto; border-bottom-left-radius: 6px;
}
.bubble-meta { font-size: 0.75rem; opacity: 0.8; margin-bottom: 6px; font-weight: 500; }

/* Chat Input Styling */
div[data-testid="stChatInput"] {
    background: #1a1d27!important; border-radius: 25px!important;
    border: 1px solid #2a2f45!important;
}
div[data-testid="stChatInput"] textarea { color: white!important; }

@keyframes slideUp { from {opacity:0; transform: translateY(10px);} to {opacity:1; transform: translateY(0);} }
.empty-state { text-align: center; margin-top: 15vh; color: #5a637a; }
.empty-state h3 { color: #c8d0e2; }
</style>
""", unsafe_allow_html=True)

# --- CLIENT SETUP WITH ERROR HANDLING ---
@st.cache_resource
def get_client():
    try:
        api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except Exception:
        return None

client = get_client()

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# --- FUNCTIONS ---
def save_chat_history():
    try:
        os.makedirs("chat_history", exist_ok=True)
        with open("chat_history/all_chats.json", "w") as f:
            json.dump(st.session_state.chat_history, f, indent=2)
    except: pass

def load_chat_history():
    try:
        if os.path.exists("chat_history/all_chats.json"):
            with open("chat_history/all_chats.json", "r") as f:
                st.session_state.chat_history = json.load(f)
            return True
    except: pass
    return False

def ai_respond(prompt):
    if not client:
        return "⚠️ GROQ_API_KEY set nahi hai! Streamlit Cloud > Settings > Secrets me `GROQ_API_KEY = 'gsk_...'` add karo.", "No-Key"

    # Simple rate limit
    now = time.time()
    if now - st.session_state.last_time < 1.5:
        time.sleep(1.5)
    st.session_state.last_time = now

    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    for model in models:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": """
                    You are NEXUS Pro AI - Professional AI Assistant.
                    Creator: Engr Babar Ali Jatoi from Pakistan.
                    Built with Streamlit + Groq AI.
                    If asked "Kaun banaya?" -> "Mujhe Engr Babar Ali Jatoi ne banaya hai!"
                    Always reply in user's language. Be helpful, smart and concise.
                    """},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            return resp.choices[0].message.content, model
        except Exception as e:
            last_error = str(e)
            continue
    return f"Kuch galat ho gaya! Error: {last_error}. API Key check karo aur dobara try karo.", "Error"

# Load history once
if not st.session_state.chat_history:
    load_chat_history()

# --- HEADER BAR ---
col1, col2 = st.columns([4, 1.5])
with col1:
    st.markdown(f"""
    <div class="app-header">
        <div>
            <h2>🤖 NEXUS Pro AI</h2>
            <p>by Engr Babar Ali Jatoi • {len(st.session_state.chat_history)//2} chats</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    with st.popover("⚙️ Menu"):
        if st.button("📋 Load History", use_container_width=True):
            if load_chat_history(): st.toast("History loaded!")
            else: st.toast("No history found")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            save_chat_history()
            st.rerun()
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.chat_history = []
            save_chat_history()
            st.rerun()

# --- CHAT DISPLAY ---
if not st.session_state.chat_history:
    st.markdown("""
    <div class="empty-state">
        <div style='font-size:4rem;'>🤖</div>
        <h3>Engr Babar Ali Jatoi ka NEXUS Pro AI</h3>
        <p>Assalam-o-Alaikum! Kuch bhi poocho, main ready hun.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for chat in st.session_state.chat_history:
        ts = chat.get('time', 'Now')
        if 'user' in chat:
            st.markdown(f"""
            <div class="chat-bubble user-bubble">
                <div class="bubble-meta">You • {ts}</div>
                {chat['user']}
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bubble ai-bubble">
                <div class="bubble-meta">NEXUS Pro AI • {ts}</div>
                {chat['bot']}
            </div>""", unsafe_allow_html=True)

# --- CORRECT INPUT (st.chat_input) ---
if prompt := st.chat_input("Engr Babar Ali Jatoi ke AI se kuch poocho..."):
    # Add user msg
    st.session_state.chat_history.append({
        "user": prompt,
        "timestamp": datetime.now().isoformat(),
        "time": datetime.now().strftime("%H:%M")
    })
    save_chat_history()
    st.rerun()

# Show AI response after user input
if st.session_state.chat_history and "user" in st.session_state.chat_history[-1]:
    last_prompt = st.session_state.chat_history[-1]["user"]
    with st.chat_message("assistant"):
        with st.spinner("NEXUS soch raha hai..."):
            answer, model = ai_respond(last_prompt)
            st.markdown(f"""
            <div class="chat-bubble ai-bubble">
                <div class="bubble-meta">NEXUS Pro AI • {datetime.now().strftime("%H:%M")}</div>
                {answer}
            </div>""", unsafe_allow_html=True)

    st.session_state.chat_history.append({
        "bot": answer,
        "timestamp": datetime.now().isoformat(),
        "time": datetime.now().strftime("%H:%M"),
        "model": model
    })
    save_chat_history()
    st.rerun()
