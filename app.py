import streamlit as st
import json
import os
import time
from groq import Groq

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="⚡ NEXUS AI", layout="centered")

# ========================
# LOAD API KEY
# ========================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ========================
# SESSION INIT
# ========================
if "user" not in st.session_state:
    st.session_state.user = None

if "last_time" not in st.session_state:
    st.session_state.last_time = 0

# ========================
# LOGIN SYSTEM
# ========================
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def login():
    st.title("🔐 NEXUS AI Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if u in users and users[u] == p:
            st.session_state.user = u
            st.success("Login Success ✅")
            st.rerun()
        else:
            st.error("Wrong login ❌")

if not st.session_state.user:
    login()
    st.stop()

# ========================
# MEMORY SYSTEM
# ========================
def memory_file():
    return f"memory/{st.session_state.user}.json"

def load_memory():
    if not os.path.exists(memory_file()):
        return []
    with open(memory_file(), "r") as f:
        return json.load(f)

def save_memory(data):
    os.makedirs("memory", exist_ok=True)
    with open(memory_file(), "w") as f:
        json.dump(data, f)

chat_history = load_memory()

# ========================
# RATE LIMIT
# ========================
def rate_limit():
    if time.time() - st.session_state.last_time < 2:
        st.warning("⏳ Wait 2 sec...")
        st.stop()
    st.session_state.last_time = time.time()

# ========================
# MODEL AUTO SWITCH (🔥)
# ========================
MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "mixtral-8x7b-32768"
]

def get_ai_response(prompt):
    for m in MODELS:
        try:
            response = client.chat.completions.create(
                model=m,
                messages=[
                    {"role": "system", "content": "You are a smart AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except:
            continue
    return "⚠️ All models failed"

# ========================
# UI
# ========================
st.title(f"⚡ NEXUS AI - Welcome {st.session_state.user}")

# Show history
for chat in chat_history:
    st.write(f"👤: {chat['user']}")
    st.write(f"🤖: {chat['bot']}")

# ========================
# INPUT
# ========================
user_input = st.text_input("Ask something...")

if user_input and user_input.strip() != "":
    rate_limit()

    answer = get_ai_response(user_input)

    chat_history.append({
        "user": user_input,
        "bot": answer
    })

    save_memory(chat_history)

    st.write("🤖:", answer)

# ========================
# LOGOUT
# ========================
if st.button("Logout"):
    st.session_state.user = None
    st.rerun()
