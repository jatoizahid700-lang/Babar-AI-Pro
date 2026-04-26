import streamlit as st
from groq import Groq
from openai import OpenAI
import base64

# 🔑 API Clients
groq = Groq(api_key=st.secrets["GROQ_API_KEY"])
openai = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Babar AI Ultra Lite", page_icon="🤖")

st.title("🤖 Babar AI Ultra Lite")
st.caption("Fast Chat + Image AI")

# 📂 Image Upload
image = st.file_uploader("🖼️ Photo upload karein", type=["jpg","png","jpeg"])

# 💬 User Input
prompt = st.chat_input("Apna sawal likhein...")

# 🔥 MAIN LOGIC
if prompt:

    st.chat_message("user").write(prompt)

    try:
        # 🖼️ IMAGE CASE → OpenAI Vision
        if image:
            img_bytes = image.read()
            b64 = base64.b64encode(img_bytes).decode()

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64}"
                            }
                        }
                    ]
                }]
            )

        # 💬 TEXT CASE → Groq
        else:
            response = groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

        reply = response.choices[0].message.content

        st.chat_message("assistant").write(reply)

    except Exception as e:
        st.error(f"Error: {e}")
