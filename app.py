import streamlit as st
from groq import Groq
import base64
from PIL import Image

# 1. Page Configuration
try:
    img = Image.open("logo.png")
    st.set_page_config(page_title="Babar's AI Pro", page_icon=img)
except:
    st.set_page_config(page_title="Babar's AI Pro", page_icon="🤖")

# 2. Connection with Latest Models
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Babar's AI Helper")
st.caption("2026 Updated Version | Vision Supported")

# 3. File Uploader
uploaded_file = st.file_uploader("Pic upload karein (Optional)", type=["jpg", "png", "jpeg"])

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
                # Naya 2026 Vision Model
                base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                response = client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview", # Sabse latest vision model
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }]
                )
            else:
                # Sabse Stable Text Model
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[{"role": "user", "content": prompt}]
                )
            
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Error: {e}")
            
