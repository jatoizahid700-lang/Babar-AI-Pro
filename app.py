import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="🤖 NEXUS Pro AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; }
html, body, [class*="css"], [class*="st-"] { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; height: 0; }
.block-container { padding-top: 1rem !important; padding-bottom: 6rem !important; max-width: 900px !important; }
.nexus-header {
    background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.5); border-radius: 20px; padding: 1.2rem 2rem;
    margin-bottom: 1.2rem; box-shadow: 0 8px 32px rgba(99,102,241,0.12), 0 2px 8px rgba(0,0,0,0.04);
    display: flex; align-items: center; justify-content: space-between;
}
.nexus-logo {
    font-size: 1.6rem; font-weight: 800;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 30%, #a855f7 60%, #6366f1 100%);
    background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: gradientShift 4s ease infinite;
}
@keyframes gradientShift { 0%,100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }
.nexus-badge {
    background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; font-size: 0.65rem;
    font-weight: 700; padding: 0.25rem 0.6rem; border-radius: 20px; letter-spacing: 0.5px;
    text-transform: uppercase; margin-left: 0.6rem; vertical-align: middle;
}
.nexus-creator { font-size: 0.8rem; color: #64748b; font-weight: 500; }
.nexus-creator span { color: #6366f1; font-weight: 600; }
.nexus-actions { display: flex; gap: 0.5rem; }
.nexus-btn {
    border: 1px solid #e2e8f0; background: white; color: #475569; font-size: 0.78rem;
    font-weight: 600; padding: 0.5rem 1rem; border-radius: 12px; cursor: pointer;
    transition: all 0.25s ease; display: flex; align-items: center; gap: 0.35rem;
}
.nexus-btn:hover {
    background: #6366f1; color: white; border-color: #6366f1;
    transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99,102,241,0.3);
}
.nexus-btn.danger:hover { background: #ef4444; border-color: #ef4444; box-shadow: 0 6px 20px rgba(239,68,68,0.3); }
.nexus-chat {
    background: rgba(255,255,255,0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5);
    border-radius: 20px; padding: 1.5rem; min-height: 58vh; max-height: 65vh; overflow-y: auto;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06); scroll-behavior: smooth;
}
.nexus-chat::-webkit-scrollbar { width: 6px; }
.nexus-chat::-webkit-scrollbar-track { background: transparent; }
.nexus-chat::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.nexus-chat::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
.msg-row { margin-bottom: 1.2rem; display: flex; animation: msgSlide 0.4s cubic-bezier(0.16,1,0.3,1); }
.msg-row.user { justify-content: flex-end; }
.msg-row.bot { justify-content: flex-start; }
@keyframes msgSlide { from { opacity: 0; transform: translateY(16px) scale(0.97); } to { opacity: 1; transform: translateY(0) scale(1); } }
.msg-bubble { max-width: 78%; padding: 1rem 1.3rem; border-radius: 18px; position: relative; line-height: 1.6; font-size: 0.92rem; }
.msg-bubble.user-bubble {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%);
    color: white; border-bottom-right-radius: 6px; box-shadow: 0 6px 24px rgba(37,99,235,0.25);
}
.msg-bubble.bot-bubble {
    background: white; color: #1e293b; border: 1px solid #e2e8f0;
    border-bottom-left-radius: 6px; box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.msg-meta { font-size: 0.7rem; font-weight: 600; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem; opacity: 0.85; }
.msg-bubble.user-bubble .msg-meta { color: rgba(255,255,255,0.8); }
.msg-bubble.bot-bubble .msg-meta { color: #6366f1; }
.msg-bubble.bot-bubble .msg-text { font-family: 'Inter', sans-serif; }
.msg-bubble.bot-bubble .msg-text code {
    font-family: 'JetBrains Mono', monospace; background: #f1f5f9; padding: 0.15rem 0.4rem;
    border-radius: 6px; font-size: 0.82rem; color: #e11d48;
}
.msg-bubble.bot-bubble .msg-text pre {
    background: #0f172a; color: #e2e8f0; padding: 1rem; border-radius: 12px;
    overflow-x: auto; margin: 0.6rem 0; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; line-height: 1.5;
}
.msg-bubble.bot-bubble .msg-text ul, .msg-bubble.bot-bubble .msg-text ol { padding-left: 1.2rem; margin: 0.4rem 0; }
.msg-bubble.bot-bubble .msg-text li { margin-bottom: 0.25rem; }
.msg-bubble.bot-bubble .msg-text strong { color: #6366f1; }
.model-tag {
    font-size: 0.6rem; background: rgba(99,102,241,0.1); color: #6366f1;
    padding: 0.1rem 0.4rem; border-radius: 6px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px;
}
.empty-state { text-align: center; padding: 4rem 2rem; animation: fadeIn 0.8s ease; }
.empty-icon { font-size: 4.5rem; margin-bottom: 1.2rem; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.empty-state h3 { color: #1e293b; font-size: 1.4rem; font-weight: 700; margin-bottom: 0.5rem; }
.empty-state p { color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem; }
.suggestion-chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5rem; margin-top: 1rem; }
.chip {
    background: white; border: 1px solid #e2e8f0; color: #475569; font-size: 0.8rem;
    font-weight: 500; padding: 0.45rem 1rem; border-radius: 25px; cursor: pointer; transition: all 0.2s;
}
.chip:hover { background: #6366f1; color: white; border-color: #6366f1; transform: scale(1.05); }
.nexus-input-wrap {
    position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 100%; max-width: 920px; padding: 1rem 1.5rem 1.5rem;
    background: linear-gradient(180deg, transparent 0%, rgba(255,255,255,0.95) 20%, white 100%); z-index: 999;
}
.nexus-input-box {
    display: flex; align-items: center; gap: 0.7rem; background: white;
    border: 2px solid #e2e8f0; border-radius: 18px; padding: 0.5rem 0.6rem 0.5rem 1.2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08); transition: all 0.3s ease;
}
.nexus-input-box:focus-within { border-color: #6366f1; box-shadow: 0 8px 32px rgba(99,102,241,0.15); }
.nexus-input-box input {
    flex: 1; border: none !important; outline: none !important; box-shadow: none !important;
    font-size: 0.95rem; font-family: 'Inter', sans-serif; background: transparent !important;
    padding: 0.5rem 0 !important; color: #1e293b !important;
}
.nexus-input-box input::placeholder { color: #94a3b8; }
.send-btn {
    width: 44px; height: 44px; border-radius: 14px; border: none;
    background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; font-size: 1.2rem;
    cursor: pointer; display: flex; align-items: center; justify-content: center;
    transition: all 0.25s; flex-shrink: 0;
}
.send-btn:hover { transform: scale(1.08); box-shadow: 0 6px 20px rgba(99,102,241,0.4); }
.send-btn:active { transform: scale(0.95); }
.typing-indicator {
    display: flex; align-items: center; gap: 0.4rem; padding: 0.6rem 1rem;
    background: white; border: 1px solid #e2e8f0; border-radius: 18px;
    border-bottom-left-radius: 6px; width: fit-content; box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.typing-dot { width: 8px; height: 8px; background: #6366f1; border-radius: 50%; animation: typingBounce 1.4s infinite; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce { 0%,60%,100% { transform: translateY(0); opacity: 0.4; } 30% { transform: translateY(-8px); opacity: 1; } }
.stats-bar { display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem; }
.stat-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; color: #64748b; font-weight: 500; }
.stat-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.stat-dot.green { background: #10b981; box-shadow: 0 0 8px rgba(16,185,129,0.4); }
.stat-dot.blue { background: #3b82f6; box-shadow: 0 0 8px rgba(59,130,246,0.4); }
.stat-dot.purple { background: #6366f1; box-shadow: 0 0 8px rgba(99,102,241,0.4); }
.stToast { border-radius: 14px !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%) !important; }
[data-testid="stSidebar"] * { font-family: 'Inter', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown('<div style="text-align:center; padding: 1.5rem 1rem 1rem;"><div style="font-size: 3rem; margin-bottom: 0.5rem;">🤖</div><h2 style="font-size:1.3rem; font-weight:800; color:#1e293b; margin:0;">NEXUS Pro</h2><p style="color:#6366f1; font-size:0.75rem; font-weight:600; letter-spacing:1px; margin:0.2rem 0;">AI ASSISTANT</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**⚙️ Settings**")
    selected_model = st.selectbox("🧠 AI Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"], format_func=lambda x: x.replace("-", " ").title())
    temp_val = st.slider("🌡️ Temperature", 0.0, 1.0, 0.7, 0.1)
    st.markdown("---")
    st.markdown("**📊 Session Stats**")
    total_msgs = len(st.session_state.get("chat_history", []))
    user_msgs = sum(1 for c in st.session_state.get("chat_history", []) if "user" in c)
    bot_msgs = sum(1 for c in st.session_state.get("chat_history", []) if "bot" in c)
    c1, c2 = st.columns(2)
    c1.metric("Messages", total_msgs)
    c2.metric("Replies", bot_msgs)
    st.markdown("---")
    st.markdown("**💡 Quick Prompts**")
    quick_prompts = [
        "Python factorial program",
        "AI kya hai simple mein",
        "Portfolio website banao",
        "Pakistan 10 facts",
        "Kaun banaya is AI ko",
        "Math equation solve karo"
    ]
    for qp in quick_prompts:
        if st.button("💬 " + qp, key="qp_" + qp.replace(" ", "_"), use_container_width=True):
            st.session_state.quick_prompt = qp
    st.markdown("---")
    st.markdown('<div style="text-align:center; padding: 0.5rem;"><p style="font-size:0.75rem; color:#94a3b8; margin:0;">Made with ❤️ by<br><strong style="color:#6366f1;">Engr Babar Ali Jatoi</strong><br>🇵🇰 Pakistan</p></div>', unsafe_allow_html=True)

# ─── SESSION STATE ───
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_time" not in st.session_state:
    st.session_state.last_time = 0
if "processing" not in st.session_state:
    st.session_state.processing = False
if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

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
    return parts[0] + "-" + parts[1] if len(parts) >= 2 else model[:12]

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

def clean_text(text):
    t = str(text)
    t = t.replace("&", "&amp;")
    t = t.replace("<", "&lt;")
    t = t.replace(">", "&gt;")
    t = t.replace('"', "&quot;")
    t = t.replace("'", "&#39;")
    return t

def ai_respond(prompt, model, temperature):
    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": "You are NEXUS Pro AI - a professional, intelligent AI assistant. Creator: Engr Babar Ali Jatoi (Pakistan). Built with Streamlit + Groq AI. Jab koi pooche 'Kaun banaya?' ya 'Developer?' -> 'NEXUS Pro AI ko Engr Babar Ali Jatoi ne banaya hai! Pakistan'. User ki language mein jawab do. Professional but friendly. Code dene waqt proper formatting use karo."},
                {"role": "user", "content": prompt}
            ]
        )
        return resp.choices[0].message.content, model
    except Exception as e:
        err = str(e).lower()
        if "rate" in err:
            return "Thoda ruko, bohat requests aa rahi hain. 2-3 seconds baad try karo.", "rate-limited"
        elif "auth" in err:
            return "API key issue hai. Engr Babar Ali Jatoi se contact karo.", "auth-error"
        elif "timeout" in err:
            return "Server slow hai, dobara try karo.", "timeout"
        else:
            return "Kuch galat ho gaya. Dobar try karo!", "error"

load_chats()

# ─── HEADER ───
header_html = '<div class="nexus-header"><div><span class="nexus-logo">🤖 NEXUS Pro AI</span><span class="nexus-badge">v2.0</span><div class="nexus-creator">Built by <span>Engr Babar Ali Jatoi</span> 🇵🇰</div></div><div class="nexus-actions">'
header_html += '<button class="nexus-btn" onclick="document.querySelector(\'[data-testid=\"stSidebarToggle\"]\').click()">⚙️ Settings</button>'
header_html += '<button class="nexus-btn" onclick="window.location.reload()">🔄 Refresh</button>'
header_html += '<button class="nexus-btn danger" id="clearAllBtn">🗑️ Clear</button>'
header_html += '</div></div>'
st.markdown(header_html, unsafe_allow_html=True)

# Hidden clear button
if st.button("hidden_clear_trigger", key="hclear", label_visibility="collapsed"):
    st.session_state.chat_history = []
    save_chats()
    st.success("Sab clear ho gaya!")
    st.rerun()

# ─── STATS BAR ───
stats_html = '<div class="stats-bar">'
stats_html += '<div class="stat-item"><span class="stat-dot green"></span> Online</div>'
stats_html += '<div class="stat-item"><span class="stat-dot blue"></span> ' + str(user_msgs) + ' messages</div>'
stats_html += '<div class="stat-item"><span class="stat-dot purple"></span> ' + short_model(selected_model) + '</div>'
stats_html += '</div>'
st.markdown(stats_html, unsafe_allow_html=True)

# ─── BUILD CHAT HTML (NO TRIPLE QUOTES ISSUE) ───
chat_parts = []
chat_parts.append('<div class="nexus-chat" id="nexusChat">')

if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        ts = safe_time(chat)
        model_name = chat.get("model", "llama-3.3-70b-versatile")
        
        if "user" in chat:
            safe_text = clean_text(chat["user"])
            row = '<div class="msg-row user"><div class="msg-bubble user-bubble">'
            row += '<div class="msg-meta">👤 You &bull; ' + ts + '</div>'
            row += '<div>' + safe_text + '</div>'
            row += '</div></div>'
            chat_parts.append(row)
        
        elif "bot" in chat:
            safe_bot = clean_text(chat["bot"])
            safe_bot = safe_bot.replace("\n", "<br>")
            row = '<div class="msg-row bot"><div class="msg-bubble bot-bubble">'
            row += '<div class="msg-meta">🤖 NEXUS Pro AI &bull; ' + ts
            row += ' <span class="model-tag">' + short_model(model_name) + '</span></div>'
            row += '<div class="msg-text">' + safe_bot + '</div>'
            row += '</div></div>'
            chat_parts.append(row)
else:
    chat_parts.append('<div class="empty-state">')
    chat_parts.append('<div class="empty-icon">🤖</div>')
    chat_parts.append('<h3>NEXUS Pro AI se baat karo!</h3>')
    chat_parts.append('<p>Engr Babar Ali Jatoi ka advanced AI assistant</p>')
    chat_parts.append('<div class="suggestion-chips">')
    chat_parts.append('<span class="chip" onclick="window._sendSuggestion(\'Python mein factorial program likho\')">🐍 Python Code</span>')
    chat_parts.append('<span class="chip" onclick="window._sendSuggestion(\'AI kya hai simple words mein\')">🧠 AI Kya Hai?</span>')
    chat_parts.append('<span class="chip" onclick="window._sendSuggestion(\'Portfolio website banana hai\')">🌐 Portfolio Website</span>')
    chat_parts.append('<span class="chip" onclick="window._sendSuggestion(\'Pakistan ke 10 interesting facts\')">🇵🇰 Pakistan Facts</span>')
    chat_parts.append('<span class="chip" onclick="window._sendSuggestion(\'Kaun banaya is AI ko?\')">👤 Developer Kaun?</span>')
    chat_parts.append('<span class="chip" onclick="window._sendSuggestion(\'15x + 25 = 100 solve karo\')">🧮 Math Solve</span>')
    chat_parts.append('</div></div>')

if st.session_state.processing:
    chat_parts.append('<div class="msg-row bot"><div class="typing-indicator">')
    chat_parts.append('<div class="typing-dot"></div>')
    chat_parts.append('<div class="typing-dot"></div>')
    chat_parts.append('<div class="typing-dot"></div>')
    chat_parts.append('<span style="font-size:0.75rem;color:#6366f1;font-weight:600;margin-left:0.3rem;">NEXUS soch raha hai...</span>')
    chat_parts.append('</div></div>')

chat_parts.append('</div>')
st.markdown("".join(chat_parts), unsafe_allow_html=True)

# ─── INPUT AREA ───
input_wrap = '<div class="nexus-input-wrap"><div class="nexus-input-box">'
st.markdown(input_wrap, unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    c_in, c_bt = st.columns([6, 1])
    with c_in:
        user_input = st.text_input("msg", placeholder="✍️ Message likho ya suggestion click karo...", label_visibility="collapsed", key="chat_input_field")
    with c_bt:
        submitted = st.form_submit_button("📤", use_container_width=True, type="primary")

st.markdown('</div><div style="text-align:center;margin-top:0.5rem;"><span style="font-size:0.68rem;color:#94a3b8;">Powered by Groq AI &bull; Response &lt; 2s &bull; Built by Engr Babar Ali Jatoi</span></div></div>', unsafe_allow_html=True)

# ─── PROCESS MESSAGE ───
def process_message(text):
    if not text or not text.strip():
        return
    now = time.time()
    if now - st.session_state.last_time < 1.5:
        time.sleep(1.5 - (now - st.session_state.last_time))
    st.session_state.last_time = now
    st.session_state.processing = True
    st.rerun()

if submitted and user_input.strip():
    process_message(user_input)

qp = st.session_state.get("quick_prompt")
if qp:
    st.session_state.quick_prompt = None
    process_message(qp)

# ─── BACKGROUND PROCESSING ───
if st.session_state.processing:
    last_user_msg = ""
    for chat in reversed(st.session_state.chat_history):
        if "user" in chat:
            last_user_msg = chat["user"]
            break
    if not last_user_msg and qp:
        last_user_msg = qp
        st.session_state.chat_history.append({"user": qp, "timestamp": datetime.now().isoformat()})
        save_chats()
    if last_user_msg:
        answer, model = ai_respond(last_user_msg, selected_model, temp_val)
        st.session_state.chat_history.append({"bot": answer, "timestamp": datetime.now().isoformat(), "model": model})
        save_chats()
    st.session_state.processing = False
    st.rerun()

# ─── JAVASCRIPT ───
js_code = """
<script>
function scrollToBottom(){
    var c=document.getElementById('nexusChat');
    if(c){c.
