import streamlit as st
from groq import Groq
import base64
from PIL import Image

# Page Config
try:
    img = Image.open("logo.png")
    st.set_page_config(page_title="Babar's AI Pro", page_icon=img)
except:
    st.set_page_config(page_title="Babar's AI Pro", page_icon="🤖")

# API Key from Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Babar's AI Helper")

# Image Upload
uploaded_file = st.file_uploader("Pic upload karein", type=["jpg", "png", "jpeg"])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yahan sawal likhen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                # Agar photo upload ki hai
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
                # Agar sirf text msg hai
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
            
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Error: {e}")
            
