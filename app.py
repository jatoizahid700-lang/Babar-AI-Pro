import streamlit as st
from groq import Groq

# -------------------------
# SETUP
# -------------------------
st.set_page_config(page_title="Babar AI Voice", page_icon="🎤", layout="wide")

st.title("🎤🤖 Babar AI (Groq + Voice)")

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# MODEL
# -------------------------
model = st.selectbox("Choose Model", [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
])


# -------------------------
# GROQ FUNCTION
# -------------------------
def ask_groq(text):
    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": text}],
    )
    return response.choices[0].message.content


# -------------------------
# VOICE INPUT (JS)
# -------------------------
st.subheader("🎤 Voice Input")

voice_html = """
<button onclick="startDictation()">🎤 Speak</button>

<p id="output"></p>

<script>
function startDictation() {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';

    recognition.onresult = function(event) {
        var text = event.results[0][0].transcript;
        document.getElementById("output").innerText = text;
        window.parent.postMessage({type: "streamlit:setComponentValue", value: text}, "*");
    };

    recognition.start();
}
</script>
"""

voice_text = st.components.v1.html(voice_html, height=100)


# -------------------------
# TEXT INPUT
# -------------------------
prompt = st.text_area("💬 Or type your message")

send = st.button("🚀 Send")


# -------------------------
# CHAT DISPLAY
# -------------------------
st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -------------------------
# SEND LOGIC
# -------------------------
final_prompt = voice_text if voice_text else prompt

if send:

    if not final_prompt:
        st.warning("Kuch bolo ya likho")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": final_prompt})

    with st.chat_message("user"):
        st.markdown(final_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... ⚡"):
            reply = ask_groq(final_prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
