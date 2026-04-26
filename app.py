import streamlit as st
from groq import Groq
import base64
from PIL import Image

# 1. Page Configuration (Yahan icon set hota hai)
try:
    img = Image.open("logo.png")
    st.set_page_config(page_title="Babar AI Pro", page_icon=img)
except:
    st.set_page_config(page_title="Babar AI Pro", page_icon="🤖")

# 2. Connection with Latest 2026 Models
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- NAAM CHANGE YAHAN HUA HAI ---
st.title("🤖 Babar AI Pro") 
st.caption("2026 Advanced Vision Edition")

# 3. File Uploader (Pic Option)
uploaded_file = st.file_uploader("Koi bhi photo upload karein", type=["jpg", "png", "jpeg"])

# Chat history dikhayen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Main Logic
if prompt := st.chat_input("Yahan apna sawal likhen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                # Latest Vision Model jo 2026 mein active hai
                base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                response = client.chat.completions.create(
                    model="llama-3.2-90b-vision-preview", 
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }]
                )
            else:
                # Sabse fast text model
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[{"role": "user", "content": prompt}]
                )
            
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Error: {e}")
            
