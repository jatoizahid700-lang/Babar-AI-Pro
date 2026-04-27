import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

# --- Configuration & UI Styling ---
st.set_page_config(page_title="🤖 NEXUS Pro AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"]  {font-family: 'Inter', sans-serif;}

/* Header styling */
.main-header {font-size: 2.5rem !important; font-weight: 700 !important; 
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin: 1rem 0;}

/* Scrollable Chat Area */
.chat-container {height: 65vh; overflow-y: auto; padding: 2rem;
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 20px; margin-bottom: 100px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);}

/* Messages */
.message-bubble {margin: 1rem 0; padding: 1.2rem 1.5rem; border-radius: 20px; 
    max-width: 80%; position: relative; animation: fadeInUp 0.3s ease;}
.user-message {background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white;
    margin-left: auto; border-bottom-right-radius: 5px;}
.ai-message {background: white; color: #1e293b;
    margin-right: auto; border-bottom-left-radius: 5px; border: 1px solid #e2e8f0;}

/* Fixed Bottom Input */
.input-fixed {position: fixed; bottom: 0; left: 0; right: 0; background: white; 
              padding: 1.5rem 5rem; z-index: 1000; border-top: 1px solid #eee;}

/* Action Buttons (Copy/Listen) */
.action-btn {cursor: pointer; background: #f1f5f9; border: none; padding: 5px 10px; 
             border-radius: 8px; font-size: 0.75rem; margin-top: 10px; margin-right: 5px; transition: 0.3s;}
.action-btn:hover {background: #e2e8f0;}

@keyframes fadeInUp {from {opacity: 0; transform: translateY(10px);} to {opacity: 1; transform: translateY(0);}}
</style>
""", unsafe_allow_html=True)

# --- Logic Functions ---
def clear_chat():
    st.session_state.chat_history = []
    st.rerun()

def logout():
    st.session_state.user = None
    st.rerun()

# --- Initialize Session ---
if "user" not in st.session_state: st.session_state.user = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- Login UI (Same as your original) ---
if not st.session_state.user:
    st.markdown('<h1 class="main-header">🤖 NEXUS Pro AI</h1>', unsafe_allow_html=True)
    with st.container():
        u = st.text_input("👤 Username")
        p = st.text_input("🔒 Password", type="password")
        if st.button("🚀 Enter NEXUS"):
            st.session_state.user = u
            st.rerun()
    st.stop()

# --- Top Header Bar ---
st.markdown(f"""
<div style='display: flex; justify-content: space-between; align-items: center; background: white; padding: 1rem 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 1rem;'>
    <div>
        <h3 style='margin: 0;'>🤖 NEXUS Pro AI</h3>
        <p style='margin: 0; font-size: 0.8rem; color: #64748b;'>By Engr Babar Ali Jatoi</p>
    </div>
    <div style='display: flex; gap: 10px;'>
        <button onclick="window.location.reload()" style="background: #f1f5f9; border:none; padding: 10px; border-radius: 50%; cursor:pointer;">🗑️</button>
        <button onclick="window.location.reload()" style="background: #fee2e2; border:none; padding: 10px; border-radius: 50%; cursor:pointer;">🚪</button>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Chat Display ---
chat_placeholder = st.container()
with chat_placeholder:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for i, chat in enumerate(st.session_state.chat_history):
        if "user" in chat:
            st.markdown(f'<div class="message-bubble user-message">{chat["user"]}</div>', unsafe_allow_html=True)
        else:
            # JavaScript for Copy and Speech
            safe_text = chat["bot"].replace("'", "\\'").replace("\n", " ")
            st.markdown(f"""
            <div class="message-bubble ai-message">
                <div>{chat["bot"]}</div>
                <button class="action-btn" onclick="navigator.clipboard.writeText('{safe_text}')">📋 Copy</button>
                <button class="action-btn" onclick="window.speechSynthesis.speak(new SpeechSynthesisUtterance('{safe_text}'))">🔊 Listen</button>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Fixed Bottom Input ---
st.markdown('<div class="input-fixed">', unsafe_allow_html=True)
with st.form(key="chat_input", clear_on_submit=True):
    col1, col2 = st.columns([9, 1])
    with col1:
        user_input = st.text_input("", placeholder="Engr Babar Ali Jatoi ke AI se baat karein...", label_visibility="collapsed")
    with col2:
        submit = st.form_submit_button("🚀")

if submit and user_input:
    st.session_state.chat_history.append({"user": user_input})
    
    # AI Logic
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are NEXUS Pro AI by Engr Babar Ali Jatoi."},
                      {"role": "user", "content": user_input}]
        )
        st.session_state.chat_history.append({"bot": response.choices[0].message.content})
        st.rerun()
    except:
        st.error("Groq API Error!")
st.markdown('</div>', unsafe_allow_html=True)
