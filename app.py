import streamlit as st
from groq import Groq

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 NEXUS AI")
st.caption("⚡ Powered by Groq | Fast AI Chat System")

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
# MODEL
# -------------------------
model = st.selectbox(
    "Choose AI Model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]
)

# -------------------------
# FUNCTION
# -------------------------
def ask_groq(prompt):
    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# -------------------------
# INPUT
# -------------------------
prompt = st.text_area("💬 Enter your message")
send = st.button("🚀 Send")


# -------------------------
# CHAT HISTORY
# -------------------------
st.divider()
st.subheader("🧠 Chat History")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -------------------------
# SEND MESSAGE
# -------------------------
if send:

    if not prompt.strip():
        st.warning("Message likho pehle")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("NEXUS AI thinking... ⚡"):
            try:
                reply = ask_groq(prompt)

                st.success("⚡ Response from NEXUS AI")
                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                st.error("❌ Error occurred")
                st.code(str(e))


# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("🧠 NEXUS AI | Built with Groq + Streamlit")
