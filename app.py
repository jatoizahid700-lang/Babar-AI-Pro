import streamlit as st
import base64

from openai import OpenAI
import google.generativeai as genai
from groq import Groq

# ---------------------------
# 🔐 API KEYS
# ---------------------------
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# ---------------------------
# 🎨 UI CONFIG
# ---------------------------
st.set_page_config(page_title="Babar AI Ultra 2.0", layout="wide")

st.title("🤖 Babar AI Ultra 2.0")
st.caption("Multi AI System (OpenAI + Gemini + Groq + Vision Support)")


# ---------------------------
# 🧠 MODEL SELECTOR
# ---------------------------
model_choice = st.selectbox(
    "Choose AI Model",
    ["OpenAI GPT-4o", "Gemini 1.5", "Groq Llama3"]
)


# ---------------------------
# 💬 INPUTS
# ---------------------------
prompt = st.text_area("💬 Enter your prompt")

uploaded_file = st.file_uploader(
    "🖼️ Upload Image (optional)",
    type=["png", "jpg", "jpeg"]
)

send = st.button("🚀 Send")


# ---------------------------
# 🧾 IMAGE CONVERT FUNCTION
# ---------------------------
def encode_image(file):
    return base64.b64encode(file.read()).decode("utf-8")


# ---------------------------
# 🤖 PROCESSING
# ---------------------------
if send:

    if not prompt and not uploaded_file:
        st.warning("Please enter prompt or upload image")
        st.stop()

    with st.spinner("Thinking... 🤔"):

        # =========================
        # OPENAI (VISION + TEXT)
        # =========================
        if model_choice == "OpenAI GPT-4o":

            content = [{"type": "text", "text": prompt}]

            if uploaded_file:
                img = encode_image(uploaded_file)
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
        # GEMINI (TEXT ONLY SAFE)
        # =========================
        elif model_choice == "Gemini 1.5":

            model = genai.GenerativeModel("gemini-1.5-pro")

            if uploaded_file:
                st.warning("Gemini demo mode: image support limited here (text only used)")
            
            response = model.generate_content(prompt)
            st.success(response.text)


        # =========================
        # GROQ (FAST TEXT)
        # =========================
        elif model_choice == "Groq Llama3":

            if uploaded_file:
                st.warning("Groq is text-only. Image ignored.")

            chat = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}]
            )

            st.success(chat.choices[0].message.content)


# ---------------------------
# 🔥 FOOTER
# ---------------------------
st.markdown("---")
st.caption("⚡ Built with OpenAI + Gemini + Groq | Babar AI System")
