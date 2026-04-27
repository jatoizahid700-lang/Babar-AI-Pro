import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="🤖 NEXUS Pro AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

/* Hide Streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* Root layout */
.app-root {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: #0f0f13;
    color: #e2e8f0;
    overflow: hidden;
}

/* Header */
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.85rem 1.5rem;
    background: #16161d;
    border-bottom: 1px solid #2a2a3a;
    flex-shrink: 0;
    z-index: 100;
}
.top-bar-left { display: flex; align-items: center; gap: 0.75rem; }
.nexus-logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 0 20px rgba(99,102,241,0.4);
}
.top-bar-title { font-size: 1.1rem; font-weight: 700; color: #fff; }
.top-bar-sub { font-size: 0.78rem; color: #64748b; margin-top: 1px; }

.top-actions { display: flex; gap: 0.5rem; }
.icon-btn {
    width: 36px; height: 36px;
    border-radius: 10px;
    border: 1px solid #2a2a3a;
    background: #1e1e2e;
    color: #94a3b8;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    transition: all 0.2s;
}
.icon-btn:hover { background: #2a2a3a; color: #e2e8f0; border-color: #6366f1; }
.icon-btn.danger:hover { background: #2d1515; color: #f87171; border-color: #ef4444; }

/* Messages area */
.messages-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    scroll-behavior: smooth;
}
.messages-scroll::-webkit-scrollbar { width: 4px; }
.messages-scroll::-webkit-scrollbar-track { background: transparent; }
.messages-scroll::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 10px; }

/* Welcome screen */
.welcome-box {
    text-align: center;
    margin: auto;
    padding: 3rem 1rem;
}
.welcome-icon { font-size: 4rem; margin-bottom: 1rem; }
.welcome-title { font-size: 1.5rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.5rem; }
.welcome-sub { color: #64748b; font-size: 0.9rem; }

/* Message bubbles */
.msg-row {
    display: flex;
    align-items: flex-end;
    gap: 0.6rem;
    animation: fadeUp 0.25s ease;
}
.msg-row.user { flex-direction: row-reverse; }
.msg-row.bot { flex-direction: row; }

.msg-avatar {
    width: 32px; height: 32px;
    border-radius: 10px;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.msg-avatar.user-av { background: linear-gradient(135deg, #3b82f6, #1d4ed8); }
.msg-avatar.bot-av  { background: linear-gradient(135deg, #6366f1, #a855f7); }

.msg-content { max-width: 70%; }

.msg-meta {
    font-size: 0.72rem;
    color: #475569;
    margin-bottom: 0.3rem;
    padding: 0 0.5rem;
}
.msg-row.user .msg-meta { text-align: right; }

.msg-bubble {
    padding: 0.85rem 1.1rem;
    border-radius: 16px;
    font-size: 0.92rem;
    line-height: 1.6;
    position: relative;
    word-break: break-word;
}
.msg-bubble.user-bub {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: #fff;
    border-bottom-right-radius: 4px;
}
.msg-bubble.bot-bub {
    background: #1e1e2e;
    color: #e2e8f0;
    border: 1px solid #2a2a3a;
    border-bottom-left-radius: 4px;
}

/* Bubble actions */
.bubble-actions {
    display: flex;
    gap: 0.35rem;
    margin-top: 0.4rem;
    opacity: 0;
    transition: opacity 0.2s;
}
.msg-content:hover .bubble-actions { opacity: 1; }
.bubble-actions.user-side { justify-content: flex-end; }

.bub-btn {
    font-size: 0.72rem;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    border: 1px solid #2a2a3a;
    background: #16161d;
    color: #64748b;
    cursor: pointer;
    transition: all 0.15s;
}
.bub-btn:hover { background: #2a2a3a; color: #e2e8f0; }

/* TTS badge */
.tts-badge {
    display: inline-flex; align-items: center; gap: 0.3rem;
    font-size: 0.72rem; color: #a855f7;
    background: rgba(168,85,247,0.1);
    padding: 0.15rem 0.5rem; border-radius: 20px;
    margin-top: 0.3rem;
}

/* Typing indicator */
.typing-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #6366f1;
    display: inline-block;
    animation: bounce 1.2s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-6px)} }

/* Input bar */
.input-bar {
    padding: 1rem 1.5rem;
    background: #16161d;
    border-top: 1px solid #2a2a3a;
    flex-shrink: 0;
}
.input-inner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #1e1e2e;
    border: 1px solid #2a2a3a;
    border-radius: 16px;
    padding: 0.6rem 0.6rem 0.6rem 1rem;
    transition: border-color 0.2s;
}
.input-inner:focus-within { border-color: #6366f1; }

.chat-input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: #e2e8f0;
    font-size: 0.92rem;
    font-family: 'Space Grotesk', sans-serif;
    resize: none;
    max-height: 120px;
    min-height: 24px;
}
.chat-input::placeholder { color: #475569; }

.send-btn {
    width: 40px; height: 40px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    color: #fff;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    transition: all 0.2s;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(99,102,241,0.4);
}
.send-btn:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(99,102,241,0.5); }
.send-btn:active { transform: scale(0.96); }
.send-btn svg { width: 18px; height: 18px; fill: none; stroke: white; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; }

/* Auth page */
.auth-wrap {
    min-height: 100vh;
    background: #0f0f13;
    display: flex; align-items: center; justify-content: center;
    padding: 2rem;
}
.auth-card {
    background: #16161d;
    border: 1px solid #2a2a3a;
    border-radius: 24px;
    padding: 2.5rem;
    width: 100%; max-width: 440px;
}
.auth-logo {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    margin: 0 auto 1.2rem;
    box-shadow: 0 0 30px rgba(99,102,241,0.4);
}
.auth-title { text-align: center; font-size: 1.5rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem; }
.auth-sub { text-align: center; color: #64748b; font-size: 0.85rem; margin-bottom: 2rem; }

/* Modal overlay */
.modal-overlay {
    display: none;
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.7);
    z-index: 999;
    align-items: center; justify-content: center;
}
.modal-overlay.open { display: flex; }
.modal-box {
    background: #16161d;
    border: 1px solid #2a2a3a;
    border-radius: 20px;
    padding: 1.5rem;
    width: 90%; max-width: 500px;
    max-height: 80vh;
    overflow-y: auto;
}
.modal-title {
    font-size: 1rem; font-weight: 600; color: #fff;
    margin-bottom: 1rem;
    display: flex; justify-content: space-between; align-items: center;
}
.close-btn { cursor: pointer; color: #64748b; font-size: 1.2rem; }
.close-btn:hover { color: #e2e8f0; }

.hist-item {
    padding: 0.75rem;
    border: 1px solid #2a2a3a;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: background 0.15s;
}
.hist-item:hover { background: #1e1e2e; }
.hist-preview { font-size: 0.82rem; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.hist-time { font-size: 0.72rem; color: #475569; margin-top: 0.2rem; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Streamlit widget hiding */
.stTextInput > div > div { background: transparent !important; border: none !important; }
.stTextInput input {
    background: transparent !important;
    color: #e2e8f0 !important;
    border: none !important;
    box-shadow: none !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 0 !important;
    font-size: 0.92rem !important;
}
.stButton > button { display: none; }

/* Notification toast */
.toast {
    position: fixed;
    bottom: 5rem; left: 50%; transform: translateX(-50%);
    background: #1e1e2e;
    border: 1px solid #6366f1;
    color: #e2e8f0;
    padding: 0.6rem 1.2rem;
    border-radius: 20px;
    font-size: 0.85rem;
    z-index: 9999;
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
}
.toast.show { opacity: 1; }
</style>
""", unsafe_allow_html=True)


# ── helpers ──────────────────────────────────────────────────────────────────

@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

def load_users():
    try:
        if os.path.exists("users.json"):
            with open("users.json") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def load_memory(username):
    os.makedirs("memory", exist_ok=True)
    try:
        fname = f"memory/{username}.json"
        if os.path.exists(fname):
            with open(fname) as f:
                chats = json.load(f)
                for c in chats:
                    if 'timestamp' not in c:
                        c['timestamp'] = datetime.now().isoformat()
                return chats
    except:
        pass
    return []

def save_memory(username, data):
    try:
        fname = f"memory/{username}.json"
        with open(fname, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

def fmt_time(chat):
    try:
        return datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
    except:
        return "Now"

def ai_respond(prompt, history):
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    # Build messages with recent history for context
    messages = [
        {"role": "system", "content": (
            "You are NEXUS Pro AI – a professional, friendly AI assistant.\n"
            "Creator: Engr Babar Ali Jatoi (Pakistan).\n"
            "Built with Streamlit + Groq AI.\n"
            "When asked who made you: 'Engr Babar Ali Jatoi ne banaya!'\n"
            "Reply in the same language the user uses. Be concise and helpful."
        )}
    ]
    # Add last 10 exchanges as context
    for c in history[-20:]:
        if 'user' in c:
            messages.append({"role": "user", "content": c['user']})
        elif 'bot' in c:
            messages.append({"role": "assistant", "content": c['bot']})
    messages.append({"role": "user", "content": prompt})

    for model in models:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1024,
            )
            return resp.choices[0].message.content
        except:
            continue
    return "Kuch masla aa gaya, dobara try karo!"


# ── session defaults ──────────────────────────────────────────────────────────

for k, v in {
    "user": None,
    "chat_history": [],
    "input_key": 0,
    "last_time": 0,
    "show_history": False,
    "auth_tab": "login",
    "pending_msg": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# AUTH PAGE
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.user:
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="auth-card">
        <div class="auth-logo">🤖</div>
        <div class="auth-title">NEXUS Pro AI</div>
        <div class="auth-sub">by Engr Babar Ali Jatoi • Pakistan</div>
    </div>
    """, unsafe_allow_html=True)

    tab = st.radio("", ["🚀 Login", "📝 Sign Up"], horizontal=True,
                   label_visibility="collapsed")

    if tab == "🚀 Login":
        username = st.text_input("Username", placeholder="apna username likhein")
        password = st.text_input("Password", type="password", placeholder="password")
        if st.button("Login", key="login_btn"):
            users = load_users()
            if username in users and users[username] == password:
                st.session_state.user = username
                st.session_state.chat_history = load_memory(username)
                st.rerun()
            else:
                st.error("❌ Username ya password galat hai!")
    else:
        ruser = st.text_input("New Username", placeholder="naya username chunein")
        rpass = st.text_input("Password", type="password", placeholder="password set karein", key="rpass")
        if st.button("Sign Up", key="signup_btn"):
            if ruser.strip():
                users = load_users()
                if ruser in users:
                    st.error("❌ Yeh username pehle se maujood hai!")
                else:
                    users[ruser] = rpass
                    save_users(users)
                    st.session_state.user = ruser
                    st.session_state.chat_history = []
                    st.rerun()
            else:
                st.error("Username khali nahi ho sakta!")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CHAT PAGE
# ══════════════════════════════════════════════════════════════════════════════

# ── header action buttons (real Streamlit buttons hidden, JS triggers them) ──
col_hist, col_clear, col_logout = st.columns([1, 1, 1])

with col_hist:
    if st.button("__hist__", key="btn_hist"):
        st.session_state.show_history = not st.session_state.get("show_history", False)
        st.rerun()

with col_clear:
    if st.button("__clear__", key="btn_clear"):
        st.session_state.chat_history = []
        save_memory(st.session_state.user, [])
        st.rerun()

with col_logout:
    if st.button("__logout__", key="btn_logout"):
        st.session_state.user = None
        st.session_state.chat_history = []
        st.rerun()


# ── top bar HTML ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
    <div class="top-bar-left">
        <div class="nexus-logo">🤖</div>
        <div>
            <div class="top-bar-title">NEXUS Pro AI</div>
            <div class="top-bar-sub">Hi, {st.session_state.user} • by Engr Babar Ali Jatoi</div>
        </div>
    </div>
    <div class="top-actions">
        <button class="icon-btn" title="Chat History" onclick="document.querySelector('[data-testid=\\"stButton\\"] button[kind=\\"secondary\\"]').click()"
            onclick="triggerBtn('btn_hist')">📋</button>
        <button class="icon-btn" title="Chat Copy karein" onclick="copyAllChat()">📄</button>
        <button class="icon-btn" title="Clear Chat" onclick="triggerBtn('btn_clear')">🗑️</button>
        <button class="icon-btn danger" title="Logout" onclick="triggerBtn('btn_logout')">🚪</button>
    </div>
</div>
""", unsafe_allow_html=True)


# ── history modal ─────────────────────────────────────────────────────────────
if st.session_state.get("show_history", False):
    msgs = st.session_state.chat_history
    history_html = ""
    for i, c in enumerate(msgs):
        if 'user' in c:
            ts = fmt_time(c)
            preview = c['user'][:60] + ("…" if len(c['user']) > 60 else "")
            history_html += f"""
            <div class="hist-item">
                <div class="hist-preview">👤 {preview}</div>
                <div class="hist-time">{ts}</div>
            </div>"""

    st.markdown(f"""
    <div class="modal-overlay open" id="histModal" onclick="if(event.target===this)closeHist()">
        <div class="modal-box">
            <div class="modal-title">
                📋 Chat History
                <span class="close-btn" onclick="closeHist()">✕</span>
            </div>
            {history_html if history_html else '<div style="color:#64748b;text-align:center;padding:2rem">Koi history nahi hai abhi</div>'}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── messages area ─────────────────────────────────────────────────────────────
st.markdown('<div class="messages-scroll" id="msgScroll">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-icon">🤖</div>
        <div class="welcome-title">NEXUS Pro AI</div>
        <div class="welcome-sub">Engr Babar Ali Jatoi ka AI assistant<br>Pehla message bhejo shuru karne ke liye!</div>
    </div>
    """, unsafe_allow_html=True)
else:
    all_text_parts = []
    for i, c in enumerate(st.session_state.chat_history):
        ts = fmt_time(c)
        if 'user' in c:
            txt = c['user'].replace('<', '&lt;').replace('>', '&gt;')
            all_text_parts.append(f"You: {c['user']}")
            st.markdown(f"""
            <div class="msg-row user">
                <div class="msg-avatar user-av">👤</div>
                <div class="msg-content">
                    <div class="msg-meta">{ts}</div>
                    <div class="msg-bubble user-bub" id="msg-{i}">{txt}</div>
                    <div class="bubble-actions user-side">
                        <button class="bub-btn" onclick="copyMsg('msg-{i}')">📋 Copy</button>
                        <button class="bub-btn" onclick="speakMsg('msg-{i}')">🔊 Sun</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif 'bot' in c:
            txt = c['bot'].replace('<', '&lt;').replace('>', '&gt;')
            all_text_parts.append(f"AI: {c['bot']}")
            st.markdown(f"""
            <div class="msg-row bot">
                <div class="msg-avatar bot-av">🤖</div>
                <div class="msg-content">
                    <div class="msg-meta">NEXUS AI • {ts}</div>
                    <div class="msg-bubble bot-bub" id="msg-{i}">{txt}</div>
                    <div class="bubble-actions">
                        <button class="bub-btn" onclick="copyMsg('msg-{i}')">📋 Copy</button>
                        <button class="bub-btn" onclick="speakMsg('msg-{i}')">🔊 Sun</button>
                        <button class="bub-btn" onclick="stopSpeak()">⏹️ Ruko</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # end messages-scroll


# ── input bar ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-bar"><div class="input-inner">', unsafe_allow_html=True)

user_input = st.text_input(
    "",
    key=f"inp_{st.session_state.input_key}",
    placeholder="NEXUS AI se kuch poocho...",
    label_visibility="collapsed"
)

# Send button (hidden real button + custom HTML button)
send_clicked = st.button("Send", key="send_btn")

st.markdown("""
</div></div>
<div id="toast" class="toast">✅ Copy ho gaya!</div>
""", unsafe_allow_html=True)


# ── handle send ────────────────────────────────────────────────────
