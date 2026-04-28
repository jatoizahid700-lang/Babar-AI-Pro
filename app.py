import streamlit as st
import json
import os
import time
from datetime import datetime
from groq import Groq

st.set_page_config(page_title="🤖 NEXUS Pro AI", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
* {font-family: 'Inter', sans-serif;}
html, body, [class*="css"] {font-family: 'Inter', sans-serif !important;}

.main-header { 
    font-size: 3.5rem !important; 
    font-weight: 800 !important; 
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 25%, #ec4899 50%, #f59e0b 75%, #10b981 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center; 
    margin: 2rem 0 1rem 0;
    animation: gradientShift 4s ease-in-out infinite, fadeInDown 1s ease-out;
    text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.welcome-screen {
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 30px;
    margin: 2rem;
    box-shadow: 0 40px 100px rgba(0,0,0,0.2);
    animation: welcomePulse 2s ease-in-out infinite;
}

@keyframes welcomePulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}

.robot-icon {
    font-size: 8rem;
    margin-bottom: 2rem;
    animation: bounceIn 1.5s ease-out, float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

.chat-container { 
    height: 70vh; 
    overflow-y: auto; 
    padding: 2.5rem;
    background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
    border-radius: 25px; 
    margin: 2rem 0; 
    box-shadow: 0 25px 80px rgba(0,0,0,0.15);
    border: 1px solid rgba(99, 102, 241, 0.1);
}

.message-bubble { 
    margin: 1.5rem 0; 
    padding: 1.5rem 2rem; 
    border-radius: 25px; 
    max-width: 80%; 
    box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    animation: messageSlide 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
    backdrop-filter: blur(10px);
}

@keyframes messageSlide {
    from { opacity: 0; transform: translateX(50px) scale(0.9); }
    to { opacity: 1; transform: translateX(0) scale(1); }
}

.user-message { 
    background: linear-gradient(135deg, #3b82f6, #1d4ed8, #1e40af); 
    color: white;
    margin-left: auto; 
    border-bottom-right-radius: 8px;
    box-shadow: 0 10px 40px rgba(59, 130, 246, 0.4);
}

.ai-message { 
    background: linear-gradient(135deg, #10b981, #059669, #047857); 
    color: white;
    margin-right: auto; 
    border-bottom-left-radius: 8px;
    box-shadow: 0 10px 40px rgba(16, 185, 129, 0.4);
}

.input-container { 
    position: fixed; 
    bottom: 2rem; 
    left: 50%; 
    transform: translateX(-50%);
    width: 92%; 
    max-width: 900px; 
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(20px);
    padding: 2rem;
    border-radius: 30px; 
    box-shadow: 0 30px 100px rgba(0,0,0,0.25); 
    z-index: 1000;
    border: 1px solid rgba(99, 102, 241, 0.2);
}

.header-bar { 
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(20px);
    padding: 1.5rem 2.5rem; 
    border-radius: 20px; 
    box-shadow: 0 15px 50px rgba(0,0,0,0.15); 
    margin-bottom: 2rem;
    border: 1px solid rgba(99, 102, 241, 0.1);
}

.btn-icon { 
    border-radius: 50%; 
    width: 50px; 
    height: 50px; 
    padding: 0; 
    border: none; 
    font-size: 1.3rem; 
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-icon:hover {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.btn-primary { 
    background: linear-gradient(135deg, #3b82f6, #1d4ed8); 
    color: white;
    box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
}

.btn-secondary { 
    background: linear-gradient(135deg, #f8fafc, #e2e8f0); 
    color: #64748b;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.btn-danger {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    color: white;
    box-shadow: 0 5px 20px rgba(239, 68, 68, 0.4);
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.typing-dots {
    display: flex;
    gap: 0.3rem;
}

.typing-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255,255,255,0.7);
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

.status-bar {
    position: fixed;
    top: 1rem;
    right: 2rem;
    background: rgba(16, 185, 129, 0.9);
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 25px;
    font-weight: 600;
    box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
    animation: slideInRight 0.5s ease-out;
    z-index: 1001;
    display: none;
}

@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@media (max-width: 768px) {
    .main-header { font-size: 2.5rem !important; }
    .input-container { width: 95%; bottom: 1rem; padding: 1.5rem; }
    .chat-container { height: 65vh; padding: 1.5rem; margin: 1rem 0; }
}
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
if "show_welcome" not in st.session_state: 
    st.session_state.show_welcome = True

def safe_time(chat):
    try: 
        return datetime.fromisoformat(chat['timestamp']).strftime("%H:%M")
    except: 
        return "Just now"

def save_memory():
    try:
        os.makedirs("memory", exist_ok=True)
        fname = "memory/nexus_chat.json"
        with open(fname, "w") as f: 
            json.dump(st.session_state.chat_history, f, indent=2, default=str)
    except: 
        pass

def load_memory():
    try:
        fname = "memory/nexus_chat.json"
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

def rate_limit():
    now = time.time()
    if now - st.session_state.last_time < 1.5: 
        time.sleep(1.5 - (now - st.session_state.last_time))
    st.session_state.last_time = time.time()

def ai_respond(prompt):
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    for model in models:
        try:
            with st.spinner(""):
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system", 
                            "content": """You are NEXUS Pro AI - Professional AI Assistant.
Creator: Engr Babar Ali Jatoi (Pakistan)
Built with ❤️ using Streamlit + Groq AI

Key responses:
- "Kaun banaya?" → "Engr Babar Ali Jatoi ne banaya!"
- "Developer?" → "Engr Babar Ali Jatoi from Pakistan"
- "Team?" → "Solo project by Engr Babar Ali Jatoi"

User ki language mein jawab do. Professional, helpful aur fast raho!"""
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                return resp.choices[0].message.content.strip(), model
        except Exception as e:
            continue
    return "Sorry, temporarily busy hoon. Thoda wait kar ke dobara try karo! 🚀", "Error"

# Load chat history on startup
if st.session_state.chat_history == []:
    st.session_state.chat_history = load_memory()

# Welcome Screen with Animation
if st.session_state.show_welcome or not st.session_state.chat_history:
    st.markdown("""
    <div class="welcome-screen animate__animated animate__fadeIn">
        <div class="robot-icon">🤖</div>
        <h1 class="main-header">NEXUS Pro AI</h1>
        <p style='font-size: 1.5rem; color: rgba(255,255,255,0.95); margin-bottom: 3rem; font-weight: 500;'>
            by <span style='background: linear-gradient(135deg, #fbbf24, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Engr Babar Ali Jatoi</span>
        </p>
        <div style='font-size: 1.2rem; color: rgba(255,255,255,0.8); max-width: 600px; line-height: 1.6;'>
            Pakistan ka sabse fast aur smart AI assistant. Abhi shuru karo!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-hide welcome after 3 seconds
    time.sleep(2)
    st.session_state.show_welcome = False
    st.rerun()
    st.stop()

# Main Chat Interface
st.markdown("""
<div class="header-bar animate__animated animate__fadeInDown">
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h2 style='margin: 0; background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;'>
                🤖 NEXUS Pro AI
            </h2>
            <p style='margin: 0.5rem 0 0 0; color: #64748b; font-weight: 500;'>
                by Engr Babar Ali Jatoi • {chat_count} messages
            </p>
        </div>
        <div style='display: flex; gap: 1rem;'>
            <button class="btn-icon btn-secondary" id="history-btn" title="History">📋</button>
            <button class="btn-icon btn-danger" id="clear-btn" title="Clear Chat">🗑️</button>
        </div>
    </div>
</div>
""".format(chat_count=len(st.session_state.chat_history)//2), unsafe_allow_html=True)

# Chat Container
with st.container():
    st.markdown('<div class="chat-container" id="messages">', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        for i, chat in enumerate(st.session_state.chat_history):
            col1, col2 = st.columns([3, 1]) if 'user' in chat else st.columns([1, 3])
            ts = safe_time(chat)
            
            if 'user' in chat:
                with col2: 
                    st.markdown(f"""
                    <div class="message-bubble user-message animate__animated animate__fadeInRight">
                        <div style='font-size: 0.85rem; opacity: 0.9; margin-bottom: 0.8rem; font-weight: 500;'>
                            You • {ts}
                        </div>
                        <div style='line-height: 1.6; font-size: 1.05rem;'>
                            {chat['user']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col1: 
                    st.empty()
            else:
                with col1: 
                    st.markdown(f"""
                    <div class="message-bubble ai-message animate__animated animate__fadeInLeft">
                        <div style='font-size: 0.85rem; opacity: 0.9; margin-bottom: 0.8rem; font-weight: 500;'>
                            NEXUS Pro AI • {ts}
                        </div>
                        <div style='line-height: 1.6; font-size: 1.05rem; white-space: pre-wrap;'>
                            {chat['bot']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2: 
                    st.empty()
    else:
        st.markdown("""
        <div style='text-align: center; color: #94a3b8; margin-top: 10rem;'>
            <div style='font-size: 6rem; margin-bottom: 2rem;'>🤖</div>
            <h3 style='color: #475569; margin-bottom: 1rem;'>Welcome to NEXUS Pro AI!</h3>
            <p>Pehla message type karo aur shuru karo chat karne ke liye...</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input Container
st.markdown("""
<div class="input-container animate__animated animate__fadeInUp">
    <form style='display: flex; gap: 1.5rem; align-items: center;'>
""", unsafe_allow_html=True)

user_input = st.text_input(
    "", 
    key=f"inp_{st.session_state.input_key}", 
    placeholder="Engr Babar Ali Jatoi ke NEXUS Pro AI se kuch poocho... (Ctrl+Enter)", 
    label_visibility="collapsed",
    autocomplete="off"
)

col1, col2 = st.columns([1, 6])

with col1:
    if st.button("📤", key="send_btn", use_container_width=True, type="primary"):
        if user_input.strip():
            rate_limit()
            st.session_state.input_key += 1
            timestamp = datetime.now().isoformat()
            st.session_state.chat_history.append({"user": user_input, "timestamp": timestamp})
            save_memory()
            
            with st.spinner("🤖 NEXUS Pro AI soch raha hai..."):
                answer, model = ai_respond(user_input)
                st.session_state.chat_history.append({"bot": answer, "timestamp": timestamp})
                save_memory()
            
            st.rerun()

with col2:
    st.empty()

st.markdown("""
    </form>
</div>
""", unsafe_allow_html=True)

# JavaScript for enhanced functionality
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('messages');
    const clearBtn = document.getElementById('clear-btn');
    const historyBtn = document.getElementById('history-btn');
    
    // Auto-scroll to bottom
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    scrollToBottom();
    
    // Mutation observer for new messages
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(chatContainer, { childList: true, subtree: true });
    
    // Clear chat functionality
    clearBtn.addEventListener('click', function() {
        if (confirm('Chat history clear karna chahte ho? Ye permanent hoga!')) {
            window.parent.document.querySelector('[data-testid="stAppViewContainer"]').style.opacity = '0.5';
            window.location.href = window.location.pathname + '?clear=true';
        }
    });
    
    // History button (reload chat)
    historyBtn.addEventListener('click', function() {
        window.location.reload();
    });
    
    // Clear chat on URL param
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('clear') === 'true') {
        window.parent.Streamlit.setComponentValue('clear');
        setTimeout(() => {
            window.location.href = window.location.pathname;
        }, 500);
    }
    
    // Enter key support
    document.addEventListener('keypress', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            document.querySelector('button[kind="primary"]').click();
        }
    });
});
</script>
""", unsafe_allow_html=True)

# Clear chat functionality
if st.query_params.get("clear"):
    st.session_state.chat_history = []
    save_memory()
    st.query_params.clear()
    st.rerun()

# Footer
st.markdown("""
<div style='text-align: center; padding: 4rem 2rem; color: #94a3b8; font-size: 0.95rem;'>
    <div style='margin-bottom: 1rem; font-weight: 600; color: #64748b;'>
        🚀 NEXUS Pro AI • Made with ❤️ by Engr Babar Ali Jatoi
    </div>
    <div>
        Powered by <strong>Groq AI</strong> • 🇵🇰 Pakistan • © 2026
    </div>
</div>
""", unsafe_allow_html=True)
