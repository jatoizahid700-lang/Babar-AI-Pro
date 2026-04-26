import streamlit as st
from groq import Groq
import base64
from PIL import Image

# 1. Page Config
try:
    img = Image.open("logo.png")
    st.set_page_config(page_title="Babar's AI Pro", page_icon=img)
except:
    st.set_page_config(page_title="Babar's AI Pro", page_icon="🤖")

# 2. API Key setup
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Babar's AI Helper")

# 3. File Uploader
uploaded_file = st.file_uploader("Pic upload karein", type=["jpg", "png", "jpeg"])

# History dikhayen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Logic
if prompt := st.chat_input("Yahan sawal likhen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                # VISION LOGIC (Agar photo hai)
                base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }]
                )
            else:
                # TEXT ONLY LOGIC (Agar photo nahi hai)
                response = client.chat.completions.create(
                    model="llama3-8b-8192",  # Yeh text ke liye best aur fast hai
                    messages=[{"role": "user", "content": prompt}]
                )
            
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Groq Error: {e}")
            
