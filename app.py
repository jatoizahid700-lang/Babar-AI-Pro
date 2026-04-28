import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="🤖 NEXUS Pro AI", page_icon="🤖", layout="wide")

# ─── ADVANCED CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"], [class*="st-"] { font-family: 'Inter', sans-serif !important; }

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; height: 0; }
.block-container { padding-top: 1rem !important; padding-bottom: 6rem !important; max-width: 900px !important; }

/* ── GLASSMORPHISM HEADER ── */
.nexus-header {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 20px;
    padding: 1.2rem 2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 32px rgba(99,102,241,0.12), 0 2px 8px rgba(0,0,0,0.04);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.nexus-logo {
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 30%, #a855f7 60%, #6366f1 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 4s ease infinite;
}
@keyframes gradientShift {
    0%,100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
.nexus-badge {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.25rem 0.6rem;
    border-radius: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-left: 0.6rem;
    vertical-align: middle;
}
.nexus-creator {
    font-size: 0.8rem;
    color: #64748b;
    font-weight: 500;
}
.nexus-creator span { color: #6366f1; font-weight: 600; }

/* ── ACTION BUTTONS ── */
.nexus-actions { display: flex; gap: 0.5rem; }
.nexus-btn {
    border: 1px solid #e2e8f0;
    background: white;
    color: #475569;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}
.nexus-btn:hover {
    background: #6366f1;
    color: white;
    border-color: #6366f1;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99,102,241,0.3);
}
.nexus-btn.danger:hover {
    background: #ef4444;
    border-color: #ef4444;
    box-shadow: 0 6px 20px rgba(239,68,68,0.3);
}

/* ── CHAT AREA ── */
.nexus-chat {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 20px;
    padding: 1.5rem;
    min-height: 58vh;
    max-height: 65vh;
    overflow-y: auto;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    scroll-behavior: smooth;
}
.nexus-chat::-webkit-scrollbar { width: 6px; }
.nexus-chat::-webkit-scrollbar-track { background: transparent; }
.nexus-chat::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.nexus-chat::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ── MESSAGE BUBBLES ── */
.msg-row { margin-bottom: 1.2rem; display: flex; animation: msgSlide 0.4s cubic-bezier(0.16,1,0.3,1); }
.msg-row.user { justify-content: flex-end; }
.msg-row.bot { justify-content: flex-start; }
@keyframes msgSlide {
    from { opacity: 0; transform: translateY(16px) scale(0.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.msg-bubble {
    max-width: 78%;
    padding: 1rem 1.3rem;
    border-radius: 18px;
    position: relative;
    line-height: 1.6;
    font-size: 0.92rem;
}
.msg-bubble.user-bubble {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%);
    color: white;
    border-bottom-right-radius: 6px;
    box-shadow: 0 6px 24px rgba(37,99,235,0.25);
}
.msg-bubble.bot-bubble {
    background: white;
    color: #1e293b;
    border: 1px solid #e2e8f0;
    border-bottom-left-radius: 6px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.msg-meta {
    font-size: 0.7rem;
    font-weight: 600;
    margin-bottom: 0.35rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    opacity: 0.85;
}
.msg-bubble.user-bubble .msg-meta { color: rgba(255,255,255,0.8); }
.msg-bubble.bot-bubble .msg-meta { color: #6366f1; }
.msg-bubble.bot-bubble .msg-text { font-family: 'Inter', sans-serif; }
.msg-bubble.bot-bubble .msg-text code {
    font-family: 'JetBrains Mono', monospace;
    background: #f1f5f9;
    padding: 0.15rem 0.4rem;
    border-radius: 6px;
    font-size: 0.82rem;
    color: #e11d48;
}
.msg-bubble.bot-bubble .msg-text pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 1rem;
    border-radius: 12px;
    overflow-x: auto;
    margin: 0.6rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.5;
}
.msg-bubble.bot-bubble .msg-text ul, .msg-bubble.bot-bubble .msg-text ol {
    padding-left: 1.2rem;
    margin: 0.4rem 0;
}
.msg-bubble.bot-bubble .msg-text li { margin-bottom: 0.25rem; }
.msg-bubble.bot-bubble .msg-text strong { color: #6366f1; }
.msg-bubble.bot-bubble .msg-text h1, .msg-bubble.bot-bubble .msg-text h2,
.msg-bubble.bot-bubble .msg-text h3 { color: #1e293b; margin: 0.5rem 0 0.3rem; }
.model-tag {
    font-size: 0.6rem;
    background: rgba(99,102,241,0.1);
    color: #6366f1;
    padding: 0.1rem 0.4rem;
    border-radius: 6px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    animation: fadeIn 0.8s ease;
}
.empty-icon {
    font-size: 4.5rem;
    margin-bottom: 1.2rem;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.empty-state h3 {
    color: #1e293b;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.empty-state p { color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem; }
.suggestion-chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5rem; margin-top: 1rem; }
.chip {
    background: white;
    border: 1px solid #e2e8f0;
    color: #475569;
    font-size: 0.8rem;
    font-weight: 500;
    padding: 0.45rem 1rem;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover {
    background: #6366f1;
    color: white;
    border-color: #6366f1;
    transform: scale(1.05);
}

/* ── INPUT AREA ── */
.nexus-input-wrap {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 920px;
    padding: 1rem 1.5rem 1.5rem;
    background: linear-gradient(180deg, transparent 0%, rgba(255,255,255,0.95) 20%, white 100%);
    z-index: 999;
}
.nexus-input-box {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    background: white;
    border: 2px solid #e2e8f0;
    border-radius: 18px;
    padding: 0.5rem 0.6rem 0.5rem 1.2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}
.nexus-input-box:focus-within {
    border-color: #6366f1;
    box-shadow: 0 8px 32px rgba(99,102,241,0.15);
}
.nexus-input-box input {
    flex: 1;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
    background: transparent !important;
    padding: 0.5rem 0 !important;
    color: #1e293b !important;
}
.nexus-input-box input::placeholder { color: #94a3b8; }
.send-btn {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.25s;
    flex-shrink: 0;
}
.send-btn:hover {
    transform: scale(1.08);
    box-shadow: 0 6px 20px rgba(99,102,241,0.4);
}
.send-btn:active { transform: scale(0.95); }
.send-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
}

/* ── TYPING INDICATOR ── */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.6rem 1rem;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    border-bottom-left-radius: 6px;
    width: fit-content;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.typing-dot {
    width: 8px; height: 8px;
    background: #6366f1;
    border-radius: 50%;
    animation: typingBounce 1.4s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce {
    0%,60%,100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-8px); opacity: 1; }
}

/* ── STATS BAR ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 1rem;
}
.stat-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    color: #64748b;
    font-weight: 500;
}
.stat-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
}
.stat-dot.green { background: #10b981; box-shadow: 0 0 8px rgba(16,185,129,0.4); }
.stat-dot.blue { background: #3b82f6; box-shadow: 0 0 8px rgba(59,130,246,0.4); }
.stat-dot.purple { background: #6366f1; box-shadow: 0 0 8px rgba(99,102,241,0.4); }

/* ── TOAST ── */
.stToast { border-radius: 14px !important; font-family: 'Inter', sans-serif !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%) !important;
}
[data-testid="stSidebar"] * { font-family: 'Inter', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.5rem 1rem 1rem;'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🤖</div>
        <h2 style='font-size:1.3rem; font-weight:800; color:#1e293b; margin:0;'>NEXUS Pro</h2>
        <p style='color:#6366f1; font-size:0.75rem; font-weight:600; letter-spacing:1px; margin:0.2rem 0;'>AI ASSISTANT</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("**⚙️ Settings**")
    selected_model = st.selectbox(
        "🧠 AI Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
        format_func=lambda x: x.replace("-", " ").title()
    )
    
    temp = st.slider("🌡️ Temperature", 0.0, 1.0, 0.7, 0.1)
    
    st.markdown("---")
    st.markdown("**📊 Session Stats**")
    total_msgs = len(st.session_state.get("chat_history", []))
    user_msgs = sum(1 for c in st.session_state.get("chat_history", []) if "user" in c)
    bot_msgs = sum(1 for c in st.session_state.get("chat_history", []) if "bot" in c)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Messages", total_msgs)
    with col_s2:
        st.metric("Chats", bot_msgs)
    
    st.markdown("---")
    st.markdown("**💡 Suggestions**")
    suggestions = [
        "💻 Python code likho",
        "📝 Essay writing help",
        "🧮 Math solve karo",
        "🌐 Web development tips",
        "📱 App idea do",
        "📊 Data analysis help"
    ]
    for s in suggestions:
        if st.button(s, key=f"side_{s}", use_container_width=True):
            st.session_state.suggestion_clicked = s
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem;'>
        <p style='font-size:0.75rem; color:#94a3b8; margin:0;'>
            Made with ❤️ by<br>
            <strong style='color:#6366f1;'>Engr Babar Ali Jatoi</strong><br>
            🇵🇰 Pakistan
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─── SESSION STATE ───
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_time" not in st.session_state:
    st.session_state.last_time = 0
if "processing" not in st.session_state:
    st.session_state.processing = False
if "suggestion_clicked" not in st.session_state:
    st.session_state.suggestion_clicked = None
if "current_model" not in st.session_state:
    st.session_state.current_model = "llama-3.3-70b-versatile"

# ─── GROQ CLIENT ───
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# ─── HELPERS ───
def safe_time(chat):
    try:
        return datetime.fromisoformat(chat["timestamp"]).strftime("%I:%M %p")
    except:
        return "Now"

def short_model(model):
    parts = model.split("-")
    return f"{parts[0]}-{parts[1]}" if len(parts) >= 2 else model[:12]

def save_chats():
    try:
        os.makedirs("chat_history", exist_ok=True)
        with open("chat_history/all_chats.json", "w") as f:
            json.dump(st.session_state.chat_history, f, indent=2)
    except:
        pass

def load_chats():
    try:
        if os.path.exists("chat_history/all_chats.json"):
            with open("chat_history/all_chats.json", "r") as f:
                chats = json.load(f)
                for c in chats:
                    if "timestamp" not in c:
                        c["timestamp"] = datetime.now().isoformat()
                    if "model" not in c:
                        c["model"] = "llama-3.3-70b-versatile"
                st.session_state.chat_history = chats
                return True
    except:
        pass
    return False

def escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def ai_respond(prompt, model, temperature):
    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": """You are NEXUS Pro AI — a professional, intelligent AI assistant.

Creator: Engr Babar Ali Jatoi (Pakistan 🇵🇰)
Built with: Streamlit + Groq AI

KEY RULES:
- Jab koi pooche "Kaun banaya?" / "Developer?" / "Maker?" → "NEXUS Pro AI ko Engr Babar Ali Jatoi ne banaya hai! 🇵🇰"
- User ki language mein jawab do (Urdu, English, Roman Urdu — whatever they use)
- Professional but friendly tone rakho
- Code dene waqt proper formatting use karo with explanations
- Agar koi ghalat info de, politely correct karo
- Short, useful answers do — unnecessary padding mat karo"""},
                {"role": "user", "content": prompt}
            ]
        )
        return resp.choices[0].message.content, model
    except Exception as e:
        error_msg = str(e)
        if "rate" in error_msg.lower():
            return "⏳ Thoda ruko, bohat requests aa rahi hain. 2-3 seconds baad try karo.", "rate-limited"
        elif "auth" in error_msg.lower():
            return "🔑 API key issue hai. Engr Babar Ali Jatoi se contact karo.", "auth-error"
        elif "timeout" in error_msg.lower():
            return "⌛ Server slow hai, dobara try karo.", "timeout"
        else:
            return f"❌ Error: Kuch galat ho gaya. Dobar try karo!", "error"

# ─── LOAD HISTORY ───
load_chats()

# ─── HANDLE SUGGESTION CLICK ───
if st.session_state.suggestion_clicked:
    suggestion_text = st.session_state.suggestion_clicked
    st.session_state.suggestion_clicked = None
    st.session_state.trigger_send = suggestion_text
else:
    st.session_state.trigger_send = None

# ─── HEADER ───
st.markdown("""
<div class="nexus-header">
    <div>
        <span class="nexus-logo">🤖 NEXUS Pro AI</span>
        <span class="nexus-badge">v2.0</span>
        <div class="nexus-creator">Built by <span>Engr Babar Ali Jatoi</span> 🇵🇰</div>
    </div>
    <div class="nexus-actions">
        <button class="nexus-btn" onclick="document.querySelector('[data-testid=\"stSidebarToggle\"]').click()">⚙️ Settings</button>
        <button class="nexus-btn" onclick="window.location.reload()">🔄 Refresh</button>
        <button class="nexus-btn danger" id="clearAllBtn">🗑️ Clear All</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Clear button handler via Streamlit
if st.button("🗑️", key="hidden_clear", help="Clear all chats"):
    st.session_state.chat_history = []
    save_chats()
    st.success("✅ Sab clear ho gaya!")
    st.rerun()
st.markdown("<style> [data-testid=\"stButton\"] [data-testid=\"stBaseButton-secondary\"] { display: none; } </style>", unsafe_allow_html=True)

# ─── STATS BAR ───
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item"><span class="stat-dot green"></span> Online</div>
    <div class="stat-item"><span class="stat-dot blue"></span> {user_msgs} messages sent</div>
    <div class="stat-item"><span class="stat-dot purple"></span> {short_model(selected_model)}</div>
</div>
""", unsafe_allow_html=True)

# ─── CHAT DISPLAY ───
chat_html = '<div class="nexus-chat" id="nexusChat">'

if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        ts = safe_time(chat)
        model_name = chat.get("model", "llama-3.3-70b-versatile")
        
        if "user" in chat:
            safe_text = escape_html(chat["user"])
            chat_html += f"""
            <div class="msg-row user">
                <div class="msg-bubble user-bubble">
                    <div class="msg-meta">👤 You • {ts}</div>
                    <div>{safe_text}</div>
                </div>
            </div>"""
        elif "bot" in chat:
            bot_text = chat["bot"].replace("<", "&lt;").replace(">", "&gt;")
            # Restore code blocks
            bot_text = bot_text.replace("&lt;pre&gt;", "<pre>").replace("&lt;/pre&gt;", "</pre>")
            bot_text = bot_text.replace("&lt;code&gt;", "<code>").replace("&lt;/code&gt;", "</code>")
            # Restore markdown bold/italic/lists
            bot_text = bot_text.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            bot_text = bot_text.replace("\n", "<br>")
            
            chat_html += f"""
            <div class="msg-row bot">
                <div class="msg-bubble bot-bubble">
                    <div class="msg-meta">🤖 NEXUS Pro AI • {ts} <span class="model-tag">{short_model(model_name)}</span></div>
                    <div class="msg-text">{bot_text}</div>
                </div>
            </div>"""
else:
    chat_html += """
    <div class="empty-state">
        <div class="empty-icon">🤖</div>
        <h3>NEXUS Pro AI se baat karo!</h3>
        <p>Engr Babar Ali Jatoi ka advanced AI assistant</p>
        <div class="suggestion-chips">
            <span class="chip" onclick="window.sendSuggestion('Python mein factorial program likho')">🐍 Python Code</span>
            <span class="chip" onclick="window.sendSuggestion('AI kya hai? Simple words mein batao')">🧠 AI Kya Hai?</span>
            <span class="chip" onclick="window.sendSuggestion('Mujhe ek portfolio website banana hai')">🌐 Portfolio Website</span>
            <span class="chip" onclick="window.sendSuggestion('Pakistan ke bare mein 10 interesting facts')">🇵🇰 Pakistan Facts</span>
            <span class="chip" onclick="window.sendSuggestion('Kaun banaya is AI ko?')">👤 Developer Kaun?</span>
            <span class="chip" onclick="window.sendSuggestion('Math: 15x + 25 = 100 solve karo')">🧮 Math Solve</span>
        </div>
    </div>"""

if st.session_state.processing:
    chat_html += """
    <div class="msg-row bot">
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <span style="font-size:0.75rem; color:#6366f1; font-weight:600; margin-left:0.3rem;">NEXUS soch raha hai...</s
