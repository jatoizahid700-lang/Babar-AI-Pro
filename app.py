import streamlit as st
import base64

from openai import OpenAI
from groq import Groq

# ---------------------------
# 🔐 API KEYS
# ---------------------------
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# ---------------------------
# 🎨 UI SETUP
# ---------------------------
st.set_page_config(page_title="Babar AI Dual System", layout="wide")

st.title("🤖 Babar AI Dual System")
st.caption("OpenAI + Groq AI (Fast + Smart Chat + Image Support)")

# ---------------------------
# MODEL SELECT
# ---------------------------
model = st.selectbox("Choose AI Model", ["OpenAI GPT-4o", "Groq Llama3"])

# ---------------------------
# INPUTS
# ---------------------------
prompt = st.text_area("💬 Enter your prompt")
image = st.file_uploader("🖼️ Upload image (OpenAI only)", type=["png", "jpg", "jpeg"])

send = st.button("🚀 Send")


# ---------------------------
# IMAGE ENCODING
# ---------------------------
def encode_img(file):
    return base64.b64encode(file.read()).decode("utf-8")


# ---------------------------
# MAIN LOGIC
# ---------------------------
if send:

    if not prompt and not image:
        st.warning("Prompt ya image zaroor do")
        st.stop()

    with st.spinner("Thinking... 🤔"):

        # =========================
        # OPENAI (TEXT + IMAGE)
        # =========================
        if model == "OpenAI GPT-4o":

            content = [{"type": "text", "text": prompt}]

            if image:
                img = encode_img(image)
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{img}"
                    }
                })

            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": content}]
            )

            st.success(response.choices[0].message.content)


        # =========================
        # GROQ (FAST TEXT ONLY)
        # =========================
        elif model == "Groq Llama3":

            if image:
                st.warning("Groq image support nahi karta — sirf text use hoga")

            chat = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}]
            )

            st.success(chat.choices[0].message.content)


# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("⚡ Built with OpenAI + Groq | Babar AI System")
