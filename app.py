import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="NEXUS Pro AI", page_icon="🤖", layout="wide")

css_text = '<style>'
css_text += '@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap");'
css_text += '* { box-sizing: border-box; }'
css_text += 'html, body, [class*="css"], [class*="st-"] { font-family: "Inter", sans-serif !important; }'
css_text += '#MainMenu, footer, header { visibility: hidden; height: 0; }'
css_text += '.block-container { padding-top: 1rem !important; padding-bottom: 6rem !important; max-width: 900px !important; }'
css_text += '.nexus-header { background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.5); border-radius: 20px; padding: 1.2rem 2rem; margin-bottom: 1.2rem; box-shadow: 0 8px 32px rgba(99,102,241,0.12); display: flex; align-items: center; justify-content: space-between; }'
css_text += '.nexus-logo { font-size: 1.6rem; font-weight: 800; background: linear-gradient(135deg, #6366f1, #8b5cf6, #a855f7, #6366f1); background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gs 4s ease infinite; }'
css_text += '@keyframes gs { 0%,100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }'
css_text += '.nexus-badge { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; font-size: 0.65rem; font-weight: 700; padding: 0.25rem 0.6rem; border-radius: 20px; letter-spacing: 0.5px; text-transform: uppercase; margin-left: 0.6rem; vertical-align: middle; }'
css_text += '.nexus-creator { font-size: 0.8rem; color: #64748b; font-weight: 500; }'
css_text += '.nexus-creator span { color: #6366f1; font-weight: 600; }'
css_text += '.nexus-actions { display: flex; gap: 0.5rem; }'
css_text += '.nexus-btn { border: 1px solid #e2e8f0; background: white; color: #475569; font-size: 0.78rem; font-weight: 600; padding: 0.5rem 1rem; border-radius: 12px; cursor: pointer; transition: all 0.25s; display: flex; align-items: center; gap: 0.35rem; }'
css_text += '.nexus-btn:hover { background: #6366f1; color: white; border-color: #6366f1; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99,102,241,0.3); }'
css_text += '.nexus-btn.danger:hover { background: #ef4444; border-color: #ef4444; }'
css_text += '.nexus-chat { background: rgba(255,255,255,0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); border-radius: 20px; padding: 1.5rem; min-height: 58vh; max-height: 65vh; overflow-y: auto; box-shadow: 0 8px 32px rgba(0,0,0,0.06); scroll-behavior: smooth; }'
css_text += '.nexus-chat::-webkit-scrollbar { width: 6px; }'
css_text += '.nexus-chat::-webkit-scrollbar-track { background: transparent; }'
css_text += '.nexus-chat::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }'
css_text += '.msg-row { margin-bottom: 1.2rem; display: flex; animation: ms 0.4s cubic-bezier(0.16,1,0.3,1); }'
css_text += '.msg-row.user { justify-content: flex-end; }'
css_text += '.msg-row.bot { justify-content: flex-start; }'
css_text += '@keyframes ms { from { opacity: 0; transform: translateY(16px) scale(0.97); } to { opacity: 1; transform: translateY(0) scale(1); } }'
css_text += '.msg-bubble { max-width: 78%; padding: 1rem 1.3rem; border-radius: 18px; line-height: 1.6; font-size: 0.92rem; }'
css_text += '.msg-bubble.user-bubble { background: linear-gradient(135deg, #3b82f6, #2563eb, #1d4ed8); color: white; border-bottom-right-radius: 6px; box-shadow: 0 6px 24px rgba(37,99,235,0.25); }'
css_text += '.msg-bubble.bot-bubble { background: white; color: #1e293b; border: 1px solid #e2e8f0; border-bottom-left-radius: 6px; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }'
css_text += '.msg-meta { font-size: 0.7rem; font-weight: 600; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem; opacity: 0.85; }'
css_text += '.msg-bubble.user-bubble .msg-meta { color: rgba(255,255,255,0.8); }'
css_text += '.msg-bubble.bot-bubble .msg-meta { color: #6366f1; }'
css_text += '.msg-text strong { color: #6366f1; }'
css_text += '.msg-text code { font-family: monospace; background: #f1f5f9; padding: 0.15rem 0.4rem; border-radius: 6px; font-size: 0.82rem; color: #e11d48; }'
css_text += '.msg-text pre { background: #0f172a; color: #e2e8f0; padding: 1rem; border-radius: 12px; overflow-x: auto; margin: 0.6rem 0; font-family: monospace; font-size: 0.8rem; }'
css_text += '.model-tag { font-size: 0.6rem; background: rgba(99,102,241,0.1); color: #6366f1; padding: 0.1rem 0.4rem; border-radius: 6px; font-weight: 600; text-transform: uppercase; }'
css_text += '.empty-state { text-align: center; padding: 4rem 2rem; }'
css_text += '.empty-icon { font-size: 4.5rem; margin-bottom: 1.2rem; animation: fl 3s ease-in-out infinite; }'
css_text += '@keyframes fl { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }'
css_text += '.empty-state h3 { color: #1e293b; font-size: 1.4rem; font-weight: 700; margin-bottom: 0.5rem; }'
css_text += '.empty-state p { color: #94a3b8; font-size: 0.95rem; margin-bottom: 1.5rem; }'
css_text += '.suggestion-chips { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5rem; margin-top: 1rem; }'
css_text += '.chip { background: white; border: 1px solid #e2e8f0; color: #475569; font-size: 0.8rem; font-weight: 500; padding: 0.45rem 1rem; border-radius: 25px; cursor: pointer; transition: all 0.2s; }'
css_text += '.chip:hover { background: #6366f1; color: white; border-color: #6366f1; transform: scale(1.05); }'
css_text += '.nexus-input-wrap { position: fixed; bottom: 0; left: 50%; transform: translateX(-50%); width: 100%; max-width: 920px; padding: 1rem 1.5rem 1.5rem; background: linear-gradient(180deg, transparent 0%, rgba(255,255,255,0.95) 20%, white 100%); z-index: 999; }'
css_text += '.nexus-input-box { display: flex; align-items: center; gap: 0.7rem; background: white; border: 2px solid #e2e8f0; border-radius: 18px; padding: 0.5rem 0.6rem 0.5rem 1.2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.08); transition: all 0.3s; }'
css_text += '.nexus-input-box:focus-within { border-color: #6366f1; box-shadow: 0 8px 32px rgba(99,102,241,0.15); }'
css_text += '.nexus-input-box input { flex: 1; border: none !important; outline: none !important; box-shadow: none !important; font-size: 0.95rem; background: transparent !important; padding: 0.5rem 0 !important; color: #1e293b !important; }'
css_text += '.nexus-input-box input::placeholder { color: #94a3b8; }'
css_text += '.typing-indicator { display: flex; align-items: center; gap: 0.4rem; padding: 0.6rem 1rem; background: white; border: 1px solid #e2e8f0; border-radius: 18px; border-bottom-left-radius: 6px; width: fit-content; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }'
css_text += '.typing-dot { width: 8px; height: 8px; background: #6366f1; border-radius: 50%; animation: tb 1.4s infinite; }'
css_text += '.typing-dot:nth-child(2) { animation-delay: 0.2s; }'
css_text += '.typing-dot:nth-child(3) { animation-delay: 0.4s; }'
css_text += '@keyframes tb { 0%,60%,100% { transform: translateY(0); opacity: 0.4; } 30% { transform: translateY(-8px); opacity: 1; } }'
css_text += '.stats-bar { display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem; }'
css_text += '.stat-item { display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; color: #64748b; font-weight: 500; }'
css_text += '.stat-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }'
css_text += '.stat-dot.green { background: #10b981; box-shadow: 0 0 8px rgba(16,185,129,0.4); }'
css_text += '.stat-dot.blue { background: #3b82f6; box-shadow: 0 0 8px rgba(59,130,246,0.4); }'
css_text += '.stat-dot.purple { background: #6366f1; box-shadow: 0 0 8px rgba(99,102,241,0.4); }'
css_text += '[data-testid="stSidebar"] { background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%) !important; }'
css_text += '</style>'
st.markdown(css_text, unsafe_allow_html=True)

with st.sidebar:
    side_html = '<div style="text-align:center;padding:1.5rem 1rem 1rem;">'
    side_html += '<div style="font-size:3rem;margin-bottom:0.5rem;">🤖</div>'
    side_html += '<h2 style="font-size:1.3rem;font-weight:800;color:#1e293b;margin:0;">NEXUS Pro</h2>'
    side_html += '<p style="color:#6366f1;font-size:0.75rem;font-weight:600;letter-spacing:1px;margin:0.2rem 0;">AI ASSISTANT</p>'
    side_html += '</div>'
    st.markdown(side_html, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**⚙️ Settings**")
    selected_model = st.selectbox("🧠 AI Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"])
    temp_val = st.slider("🌡️ Temperature", 0.0, 1.0, 0.7, 0.1)
    st.markdown("---")
    st.markdown("**📊 Stats**")
    total_msgs = len(st.session_state.get("chat_history", []))
    user_msgs = sum(1 for c in st.session_state.get("chat_history", []) if "user" in c)
    bot_msgs = sum(1 for c in st.session_state.get("chat_history", []) if "bot" in c)
    s1, s2 = st.columns(2)
    s1.metric("Messages", total_msgs)
    s2.metric("Replies", bot_msgs)
    st.markdown("---")
    st.markdown("**💡 Quick Prompts**")
    quick_prompts = ["Python factorial program", "AI kya hai simple mein", "Portfolio website banao", "Pakistan 10 facts", "Kaun banaya is AI ko", "Math solve karo"]
    for qp in quick_prompts:
        safe_qp_key = qp.replace(" ", "_")
        if st.button("💬 " + qp, key="qp_" + safe_qp_key, use_container_width=True):
            st.session_state.quick_prompt = qp
    st.markdown("---")
    ft_html = '<div style="text-align:center;padding:0.5rem;">'
    ft_html += '<p style="font-size:0.75rem;color:#94a3b8;margin:0;">Made with ❤️ by<br><strong style="color:#6366f1;">Engr Babar Ali Jatoi</strong><br>🇵🇰 Pakistan</p>'
    ft_html += '</div>'
    st.markdown(ft_html, unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_time" not in st.session_state:
    st.session_state.last_time = 0
if "processing" not in st.session_state:
    st.session_state.processing = False
if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

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
    except:
        pass

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
                {"role": "system", "content": "You are NEXUS Pro AI - professional AI assistant. Creator: Engr Babar Ali Jatoi (Pakistan). Built with Streamlit + Groq AI. Jab koi pooche Kaun banaya ya Developer -> NEXUS Pro AI ko Engr Babar Ali Jatoi ne banaya hai Pakistan. User ki language mein jawab do. Professional but friendly."},
                {"role": "user", "content": prompt}
            ]
        )
        return resp.choices[0].message.content, model
    except Exception as e:
        err = str(e).lower()
        if "rate" in err:
            return "Thoda ruko, bohat requests aa rahi hain. Dobar try karo.", "rate-limited"
        elif "auth" in err:
            return "API key issue hai. Engr Babar Ali Jatoi se contact karo.", "auth-error"
        else:
            return "Kuch galat ho gaya. Dobar try karo!", "error"

load_chats()

hdr = '<div class="nexus-header"><div><span class="nexus-logo">🤖 NEXUS Pro AI</span><span class="nexus-badge">v2.0</span><div class="nexus-creator">Built by <span>Engr Babar Ali Jatoi</span> 🇵🇰</div></div><div class="nexus-actions">'
hdr += '<button class="nexus-btn" onclick="document.querySelector(\'[data-testid=&quot;stSidebarToggle&quot;]\').click()">⚙️ Settings</button>'
hdr += '<button class="nexus-btn" onclick="window.location.reload()">🔄 Refresh</button>'
hdr += '<button class="nexus-btn danger" id="clearAllBtn">🗑️ Clear</button>'
hdr += '</div></div>'
st.markdown(hdr, unsafe_allow_html=True)

if st.button("hidden_clear_trigger", key="hclear", label_visibility="collapsed"):
    st.session_state.chat_history = []
    save_chats()
    st.success("Sab clear ho gaya!")
    st.rerun()

st_bar = '<div class="stats-bar">'
st_bar += '<div class="stat-item"><span class="stat-dot green"></span> Online</div>'
st_bar += '<div class="stat-item"><span class="stat-dot blue"></span> ' + str(user_msgs) + ' messages</div>'
st_bar += '<div class="stat-item"><span class="stat-dot purple"></span> ' + short_model(selected_model) + '</div>'
st_bar += '</div>'
st.markdown(st_bar, unsafe_allow_html=True)

cp = []
cp.append('<div class="nexus-chat" id="nexusChat">')

if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        ts = safe_time(chat)
        mn = chat.get("model", "llama-3.3-70b-versatile")
        if "user" in chat:
            stxt = clean_text(chat["user"])
            r = '<div class="msg-row user"><div class="msg-bubble user-bubble">'
            r += '<div class="msg-meta">👤 You &bull; ' + ts + '</div>'
            r += '<div>' + stxt + '</div></div></div>'
            cp.append(r)
        elif "bot" in chat:
            sb = clean_text(chat["bot"])
            sb = sb.replace("\n", "<br>")
            r = '<div class="msg-row bot"><div class="msg-bubble bot-bubble">'
            r += '<div class="msg-meta">🤖 NEXUS Pro AI &bull; ' + ts
            r += ' <span class="model-tag">' + short_model(mn) + '</span></div>'
            r += '<div class="msg-text">' + sb + '</div></div></div>'
            cp.append(r)
else:
    cp.append('<div class="empty-state"><div class="empty-icon">🤖</div>')
    cp.append('<h3>NEXUS Pro AI se baat karo!</h3>')
    cp.append('<p>Engr Babar Ali Jatoi ka advanced AI assistant</p>')
    cp.append('<div class="suggestion-chips">')
    cp.append('<span class="chip" onclick="window._sq(\'Python mein factorial program likho\')">🐍 Python Code</span>')
    cp.append('<span class="chip" onclick="window._sq(\'AI kya hai simple words mein\')">🧠 AI Kya Hai?</span>')
    cp.append('<span class="chip" onclick="window._sq(\'Portfolio website banana hai\')">🌐 Portfolio</span>')
    cp.append('<span class="chip" onclick="window._sq(\'Pakistan ke 10 interesting facts\')">🇵🇰 Pakistan Facts</span>')
    cp.append('<span class="chip" onclick="window._sq(\'Kaun banaya is AI ko?\')">👤 Developer Kaun?</span>')
    cp.append('<span class="chip" onclick="window._sq(\'15x + 25 = 100 solve karo\')">🧮 Math Solve</span>')
    cp.append('</div></div>')

if st.session_state.processing:
    cp.append('<div class="msg-row bot"><div class="typing-indicator">')
    cp.append('<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>')
    cp.append('<span style="font-size:0.75rem;color:#6366f1;font-weight:600;margin-left:0.3rem;">NEXUS soch raha hai...</span>')
    cp.append('</div></div>')

cp.append('</div>')
st.markdown("".join(cp), unsafe_allow_html=True)

iw = '<div class="nexus-input-wrap"><div class="nexus-input-box">'
st.markdown(iw, unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    ci, cb = st.columns([6, 1])
    with ci:
        user_input = st.text_input("msg", placeholder="✍️ Message likho ya suggestion click karo...", label_visibility="collapsed", key="chat_input_field")
    with cb:
        submitted = st.form_submit_button("📤", use_container_width=True, type="primary")

st.markdown('</div><div style="text-align:center;margin-top:0.5rem;"><span style="font-size:0.68rem;color:#94a3b8;">Powered by Groq AI &bull; Built by Engr Babar Ali Jatoi</span></div></div>', unsafe_allow_html=True)

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

qp_val = st.session_state.get("quick_prompt")
if qp_val:
    st.session_state.quick_prompt = None
    process_message(qp_val)

if st.session_state.processing:
    last_user_msg = ""
    for chat in reversed(st.session_state.chat_history):
        if "user" in chat:
            last_user_msg = chat["user"]
            break
    if not last_user_msg and qp_val:
        last_user_msg = qp_val
        st.session_state.chat_history.append({"user": qp_val, "timestamp": datetime.now().isoformat()})
        save_chats()
    if last_user_msg:
        answer, model = ai_respond(last_user_msg, selected_model, temp_val)
        st.session_state.chat_history.append({"bot": answer, "timestamp": datetime.now().isoformat(), "model": model})
        save_chats()
    st.session_state.processing = False
    st.rerun()

# ─── JAVASCRIPT — NO TRIPLE QUOTES ───
j1 = '<script>'
j2 = 'function scrollToBottom(){var c=document.getElementById("nexusChat");if(c){c.scrollTop=c.scrollHeight;}}'
j3 = 'scrollToBottom();setTimeout(scrollToBottom,300);setTimeout(scrollToBottom,800);'
j4 = 'var chatEl=document.getElementById("nexusChat");'
j5 = 'if(chatEl){var obs=new MutationObserver(function(){scrollToBottom();});obs.observe(chatEl,{childList:true,subtree:true});}'
j6 = 'window._sq=function(text){var inp=document.querySelector(\'input[aria-label="msg"]\');'
j7 = 'if(inp){var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,"value").set;'
j8 = 'setter.call(inp,text);inp.dispatchEvent(new Event("input",{bubbles:true}));'
j9 = 'var btns=document.querySelectorAll(\'button[type="submit"]\');if(btns.length>0){btns[btns.length-1].click();}}};'
j10 = 'document.getElementById("clearAllBtn")&&document.getElementById("clearAllBtn").addEventListener("click",function(){'
j11 = 'var btns=document.querySelectorAll("button");btns.forEach(function(b){if(b.textContent.includes("hidden_clear")){b.click();}});});'
j12 = '</script>'
st.markdown(j1 + j2 + j3 + j4 + j5 + j6 + j7 + j8 + j9 + j10 + j11 + j12, unsafe_allow_html=True)

ftr = '<div style="text-align:center;padding:4rem 1rem 1rem;color:#cbd5e1;font-size:0.78rem;">'
ftr += '🤖 NEXUS Pro AI v2.0 &bull; Crafted by <span style="color:#6366f1;font-weight:600;">Engr Babar Ali Jatoi</span> &bull; Powered by <span style="color:#f59e0b;">Groq</span> &bull; &copy; 2025 🇵🇰'
ftr += '</div>'
st.markdown(ftr, unsafe_allow_html=True)
