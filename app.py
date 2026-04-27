import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

# --- Configuration ---
st.set_page_config(page_title="🤖 NEXUS Pro AI", page_icon="🤖", layout="wide")

# Custom CSS for Fixed UI and Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
    
    /* Fixed Header */
    .header-bar {position: fixed; top: 0; left: 0; right: 0; background: white; z-index: 999; 
                 padding: 1rem 2rem; border-bottom: 1px solid #e2e8f0; box-shadow: 0 2px 10px rgba(0,0,0,0.05);}
    
    /* Chat Container adjustments for fixed header/footer */
    .chat-container {margin-top: 80px; margin-bottom: 120px; padding: 1rem;}
    
    .message-bubble {margin: 1rem 0; padding: 1rem 1.5rem; border-radius: 15px; position: relative; max-width: 80%;}
    .user-message {background: #3b82f6; color: white; margin-left: auto; border-bottom-right-radius: 2px;}
    .ai-message {background: #f1f5f9; color: #1e293b; margin-right: auto; border-bottom-left-radius: 2px; border: 1px solid #e2e8f0;}
    
    /* Fixed Input Bar */
    .input-wrapper {position: fixed; bottom: 0; left: 0; right: 0; background: white; 
                    padding: 1.5rem; border-top: 1px solid #e2e8f0; z-index: 999;}
    
    /* Utility Buttons Style */
    .util-btn {font-size: 0.8rem; cursor: pointer; margin-right: 10px; opacity: 0.6; transition: 0.3s;}
    .util-btn:hover {opacity: 1; color: #3b82f6;}
</style>
""", unsafe_allow_html=True)

# --- Initialization ---
if "user" not in st.session_state: st.session_state.user = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "input_key" not in st.session_state: st.session_state.input_key = 0

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- Functions ---
def save_chat():
    os.makedirs("memory", exist_ok=True)
    with open(f"memory/{st.session_state.user}.json", "w") as f:
        json.dump(st.session_state.chat_history, f)

def logout():
    st.session_state.user = None
    st.session_state.chat_history = []
    st.rerun()

def clear_chat():
    st.session_state.chat_history = []
    save_chat()
    st.rerun()

# --- Login Logic ---
if not st.session_state.user:
    st.title("🤖 NEXUS Pro AI Login")
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state.user = user_input
        # Load memory logic here
        st.rerun()
    st.stop()

# --- Main UI ---

# 1. Sidebar for History
with st.sidebar:
    st.title("📜 Chat History")
    if st.button("➕ New Chat", use_container_width=True):
        clear_chat()
    st.markdown("---")
    st.info("Aapki purani baatein yahan save hongi.")

# 2. Fixed Top Header
cols = st.columns([4, 1, 1])
with cols[0]:
    st.markdown(f"### 🤖 NEXUS Pro AI <br><small>Welcome, {st.session_state.user}</small>", unsafe_allow_html=True)
with cols[1]:
    if st.button("🗑️ Clear"): clear_chat()
with cols[2]:
    if st.button("🚪 Logout"): logout()

# 3. Chat Area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for i, chat in enumerate(st.session_state.chat_history):
    if "user" in chat:
        st.markdown(f'<div class="message-bubble user-message">{chat["user"]}</div>', unsafe_allow_html=True)
    else:
        # AI Message with Copy and Read Aloud
        text = chat["bot"].replace("'", "\\'")
        st.markdown(f"""
        <div class="message-bubble ai-message">
            {chat["bot"]}
            <div style="margin-top: 10px; border-top: 1px solid #ddd; padding-top: 5px;">
                <span class="util-btn" onclick="navigator.clipboard.writeText('{text}')">📋 Copy</span>
                <span class="util-btn" onclick="window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'))">🔊 Listen</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. Fixed Input Bar at Bottom
with st.container():
    st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        c1, c2 = st.columns([9, 1])
        with c1:
            user_msg = st.text_input("Message...", placeholder="Engr Babar Ali Jatoi ke AI se baat karein...", label_visibility="collapsed")
        with c2:
            submit = st.form_submit_button("🚀")
    
    if submit and user_msg:
        st.session_state.chat_history.append({"user": user_msg})
        
        # AI Response logic
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are NEXUS Pro AI by Engr Babar Ali Jatoi."},
                          {"role": "user", "content": user_msg}]
            )
            ans = response.choices[0].message.content
            st.session_state.chat_history.append({"bot": ans})
            save_chat()
            st.rerun()
        except Exception as e:
            st.error("Connection Error!")
    st.markdown('</div>', unsafe_allow_html=True)
