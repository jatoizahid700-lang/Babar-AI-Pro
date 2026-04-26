import streamlit as st
import json
import os
import time
from groq import Groq

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="NEXUS AI", page_icon="⚡")

# ========================
# LOAD API
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
# LOAD USERS
# ========================
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

# ========================
# LOGIN SYSTEM
# ========================
def login():
    st.title("🔐 NEXUS AI Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()

        if username in users and users[username] == password:
            st.session_state.user = username
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Credentials ❌")

if not st.session_state.user:
    login()
    st.stop()

# ========================
# MEMORY SYSTEM
# ========================
def get_memory_file():
    return f"memory/{st.session_state.user}.json"

def load_memory():
    file = get_memory_file()

    if not os.path.exists(file):
        return []

    with open(file, "r") as f:
        return json.load(f)

def save_memory(chat):
    file = get_memory_file()

    os.makedirs("memory", exist_ok=True)

    with open(file, "w") as f:
        json.dump(chat, f)

chat_history = load_memory()

# ========================
# RATE LIMIT
# ========================
def rate_limit():
    if time.time() - st.session_state.last_time < 2:
        st.warning("Slow down...")
        st.stop()

    st.session_state.last_time = time.time()

# ========================
# UI
# ========================
st.title(f"⚡ NEXUS AI - Welcome {st.session_state.user}")

# Show history
for msg in chat_history:
    st.write(f"👤: {msg['user']}")
    st.write(f"🤖: {msg['bot']}")

# ========================
# INPUT
# ========================
user_input = st.text_input("Ask something...")

if user_input:
    rate_limit()

    # AI CALL
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a smart AI with memory."},
            {"role": "user", "content": user_input}
        ]
    )

    answer = response.choices[0].message.content

    # Save memory
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
