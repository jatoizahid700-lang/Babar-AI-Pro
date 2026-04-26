import streamlit as st
from groq import Groq
import base64
from PIL import Image

# 1. Page Configuration (Yahan icon set hota hai)
# Agar logo.png hai to use karein, warna naya shield emoji use karein (monkey hatane ke liye)
try:
    img = Image.open("logo.png")
    st.set_page_config(page_title="Babar AI Pro", page_icon=img)
except:
    st.set_page_config(page_title="Babar AI Pro", page_icon="👨‍🔧") # Naya emoji shield hai

# 2. Styling (ChatGPT jaisa look, monkey hatane ke liye special style)
st.markdown("""
<style>
    /* Hide the monkey logo that was part of the original HTML */
    .stApp > header {
        display: none !important;
    }
    
    /* Ensure the logo area is clean */
    [data-testid="stSidebarNav"] div:first-child {
        display: none !important;
    }

    /* Styling main elements */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInputContainer { border-radius: 20px; }
    
</style>
""", unsafe_allow_html=True)

# 3. Connection with Latest 2026 Models
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN UI ---
# Displaying shield emoji instead of monkey
st.markdown("<h1 style='text-align: center;'>🛡️ Babar AI Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>2026 Advanced Vision Edition</b></p>", unsafe_allow_html=True)

# 4. File Uploader (Pic Option)
uploaded_file = st.file_uploader("Koi bhi photo upload karein", type=["jpg", "png", "jpeg"])

# Chat history dikhayen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Main Logic
if prompt := st.chat_input("Yahan apna sawal likhen..."):
    # Clear previous image if uploading a new one, to avoid vision/text mix errors
    if uploaded_file and "image_handled" not in st.session_state:
        st.session_state.image_handled = True

    # Check if a simple 'Hi' response is enough before doing a complex vision call
    if not uploaded_file and prompt.lower() in ["hi", "hello"]:
         st.session_state.messages.append({"role": "user", "content": prompt})
         with st.chat_message("user"):
            st.markdown(prompt)
         with st.chat_message("assistant"):
            st.markdown("It's nice to meet you. Is there something I can help you with or would you like to chat?")
            st.session_state.messages.append({"role": "assistant", "content": "It's nice to meet you. Is there something I can help you with or would you like to chat?"})
         st.stop() # Stop here for simple text response

    # Continue with vision analysis if photo exists
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                if uploaded_file and "image_handled" in st.session_state:
                    # Latest Vision Model jo 2026 mein active hai
                    base64_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                    response = client.chat.completions.create(
                        model="llama-3.2-90b-vision-preview", # Vision model
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }]
                    )
                    # Vision analysis often starts with simple text before describing the image.
                    # We will only store the first analysis message in history.
                    if len(response.choices) > 0 and len(response.choices[0].message.content) > 1:
                        vision_msg = response.choices[0].message.content
                        st.markdown(vision_msg)
                        st.session_state.messages.append({"role": "assistant", "content": vision_msg})
                    
                else:
                    # Sabse fast text model (Llama-3.3) for general text questions
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile", # Text only
                        messages=[{"role": "user", "content": prompt}]
                    )
                    text_msg = response.choices[0].message.content
                    st.markdown(text_msg)
                    st.session_state.messages.append({"role": "assistant", "content": text_msg})
                    
            except Exception as e:
                st.error(f"Error: {e}")
