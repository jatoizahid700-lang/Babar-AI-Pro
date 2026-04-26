import streamlit as st
import base64
from openai import OpenAI
from groq import Groq

# ---------------------------
# 🔐 KEYS
# ---------------------------
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------------------
# 🎨 UI
# ---------------------------
st.title("🤖 Babar AI Auto Fallback System")

prompt = st.text_area("💬 Enter your prompt")
send = st.button("🚀 Send")


# ---------------------------
# 🧠 GROQ FUNCTION
# ---------------------------
def ask_groq(prompt_text):
    response = groq_client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt_text}]
    )
    return response.choices[0].message.content


# ---------------------------
# 🧠 OPENAI FUNCTION
# ---------------------------
def ask_openai(prompt_text):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_text}]
    )
    return response.choices[0].message.content


# ---------------------------
# 🔥 AUTO FALLBACK LOGIC
# ---------------------------
if send:

    if not prompt.strip():
        st.error("Prompt required hai")
        st.stop()

    with st.spinner("AI thinking... 🤔"):

        # STEP 1: TRY GROQ FIRST
        try:
            result = ask_groq(prompt)
            st.success("⚡ Answer from GROQ (Fast AI)")
            st.write(result)

        except Exception as e:
            st.warning("⚠️ Groq failed, switching to OpenAI...")

            # STEP 2: FALLBACK OPENAI
            try:
                result = ask_openai(prompt)
                st.success("🧠 Answer from OpenAI (Fallback)")
                st.write(result)

            except Exception as e2:
                st.error("❌ Both AI failed")
                st.code(str(e2))
