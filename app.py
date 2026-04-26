import streamlit as st
from groq import Groq

# -------------------------
# PAGE CONFIG (ICON CHANGED)
# -------------------------
st.set_page_config(
    page_title="NEXUS AI",
    page_icon="⚡",   # 🧠 removed → ⚡ new clean icon
    layout="wide"
)

st.title("⚡ NEXUS AI")
st.caption("Groq Powered Voice AI System")

# -------------------------
# GROQ CLIENT
# -------------------------
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -------------------------
# SESSION STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# DEFAULT MODEL (NO SELECTOR)
# -------------------------
MODEL = "llama-3.3-70b-versatile"


# -------------------------
# GROQ FUNCTION
# -------------------------
def ask_groq(prompt):
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# -------------------------
# 🎤 VOICE INPUT (WEB SPEECH API)
# -------------------------
st.subheader("🎤 Voice Input")

voice_html = """
<button onclick="startDictation()" style="padding:10px 15px;font-size:16px;">
🎤 Speak
</button>

<p id="text"></p>

<script>
function startDictation() {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';

    recognition.onresult = function(event) {
        var text = event.results[0][0].transcript;
        document.getElementById("text").innerText = text;
        window.parent.postMessage({type: "streamlit:setComponentValue", value: text}, "*");
    };

    recognition.start();
}
</script>
"""

voice_input = st.components.v1.html(voice_html, height=120)


# -------------------------
# TEXT INPUT
# -------------------------
prompt = st.text_area("💬 Type your message")
send = st.button("🚀 Send")


# -------------------------
# CHAT HISTORY
# -------------------------
st.divider()
st.subheader("💬 Chat")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -------------------------
# FINAL INPUT (VOICE + TEXT MERGE)
# -------------------------
final_prompt = voice_input if voice_input else prompt


# -------------------------
# SEND LOGIC
# -------------------------
if send:

    if not final_prompt:
        st.warning("Kuch likho ya bolo 🎤")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": final_prompt})

    with st.chat_message("user"):
        st.markdown(final_prompt)

    with st.chat_message("assistant"):
        with st.spinner("NEXUS AI thinking... ⚡"):
            try:
                reply = ask_groq(final_prompt)

                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                st.error("❌ Error")
                st.code(str(e))


# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("⚡ NEXUS AI | Voice Powered Groq Assistant")
