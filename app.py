import os
import time
import base64
from typing import List, Dict, Optional

import streamlit as st
from openai import OpenAI
from groq import Groq


# -------------------------
# Page setup
# -------------------------
st.set_page_config(
    page_title="Babar AI Dual System",
    page_icon="🤖",
    layout="wide",
)


# -------------------------
# Helpers
# -------------------------
def load_css() -> None:
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }
        .sub-title {
            color: #6b7280;
            margin-bottom: 1rem;
        }
        .status-box {
            padding: 0.75rem 1rem;
            border-radius: 12px;
            margin: 0.5rem 0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .ok-box { background: rgba(16, 185, 129, 0.1); }
        .warn-box { background: rgba(245, 158, 11, 0.1); }
        .err-box { background: rgba(239, 68, 68, 0.1); }
        .small-note {
            font-size: 0.9rem;
            color: #9ca3af;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_provider" not in st.session_state:
        st.session_state.last_provider = None


def file_to_data_url(uploaded_file) -> str:
    data = uploaded_file.read()
    mime = uploaded_file.type or "image/png"
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def get_openai_client() -> Optional[OpenAI]:
    api_key = st.session_state.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def get_groq_client() -> Optional[Groq]:
    api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def safe_openai_response(client: OpenAI, model: str, messages: List[Dict], temperature: float, max_tokens: int) -> str:
    last_error = None
    retry_delays = [1, 2, 4]

    for attempt, delay in enumerate(retry_delays, start=1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content or "No response returned."
        except Exception as e:
            last_error = e
            error_text = str(e).lower()

            if any(k in error_text for k in ["rate limit", "quota", "429", "insufficient_quota"]):
                if attempt < len(retry_delays):
                    time.sleep(delay)
                    continue
                raise RuntimeError(
                    "OpenAI rate limit/quota issue. API key, billing, ya request limit check karein."
                ) from e

            if any(k in error_text for k in ["invalid_api_key", "authentication", "unauthorized", "401"]):
                raise RuntimeError("OpenAI API key invalid ya missing hai.") from e

            raise RuntimeError(f"OpenAI request failed: {e}") from e

    raise RuntimeError(f"OpenAI request failed: {last_error}")


def safe_groq_response(client: Groq, model: str, messages: List[Dict], temperature: float, max_tokens: int) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or "No response returned."
    except Exception as e:
        error_text = str(e).lower()
        if any(k in error_text for k in ["rate limit", "quota", "429"]):
            raise RuntimeError("Groq rate limit hit hua hai. Kuch der baad dobara try karein.") from e
        if any(k in error_text for k in ["invalid_api_key", "authentication", "unauthorized", "401"]):
            raise RuntimeError("Groq API key invalid ya missing hai.") from e
        raise RuntimeError(f"Groq request failed: {e}") from e


def build_messages(prompt: str, system_prompt: str, image_data_url: Optional[str] = None) -> List[Dict]:
    messages: List[Dict] = [{"role": "system", "content": system_prompt}]

    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})

    if image_data_url:
        messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            }
        )
    else:
        messages.append({"role": "user", "content": prompt})

    return messages


def ask_ai(
    preferred_provider: str,
    openai_model: str,
    groq_model: str,
    prompt: str,
    system_prompt: str,
    temperature: float,
    max_tokens: int,
    image_data_url: Optional[str],
) -> Dict[str, str]:
    openai_client = get_openai_client()
    groq_client = get_groq_client()

    if preferred_provider == "OpenAI":
        provider_order = ["OpenAI", "Groq"]
    elif preferred_provider == "Groq":
        provider_order = ["Groq", "OpenAI"]
    else:
        provider_order = ["OpenAI", "Groq"]

    errors = []

    for provider in provider_order:
        try:
            if provider == "OpenAI":
                if not openai_client:
                    raise RuntimeError("OpenAI key configured nahi hai.")
                messages = build_messages(prompt, system_prompt, image_data_url=image_data_url)
                answer = safe_openai_response(
                    client=openai_client,
                    model=openai_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return {"provider": "OpenAI", "content": answer}

            if provider == "Groq":
                if image_data_url:
                    errors.append("Groq fallback skipped because image input sirf OpenAI ke sath enable hai.")
                    continue
                if not groq_client:
                    raise RuntimeError("Groq key configured nahi hai.")
                messages = build_messages(prompt, system_prompt)
                answer = safe_groq_response(
                    client=groq_client,
                    model=groq_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return {"provider": "Groq", "content": answer}
        except Exception as e:
            errors.append(f"{provider}: {e}")

    raise RuntimeError(" | ".join(errors) if errors else "Unknown failure while contacting AI providers.")


# -------------------------
# UI
# -------------------------
load_css()
init_state()

st.markdown('<div class="main-title">🤖 Babar AI Dual System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">OpenAI + Groq AI · Fast + Smart Chat + Image Support</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("⚙️ Settings")

    preferred_provider = st.selectbox(
        "Primary provider",
        ["Auto", "OpenAI", "Groq"],
        index=0,
        help="Auto mode mein app pehle selected default order try karega aur zarurat par fallback use karega.",
    )

    openai_model = st.selectbox(
        "OpenAI model",
        ["gpt-4o", "gpt-4.1-mini"],
        index=0,
    )

    groq_model = st.selectbox(
        "Groq model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0,
    )

    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    max_tokens = st.slider("Max tokens", 128, 4096, 1024, 128)

    st.divider()
    st.subheader("🔑 API Keys")
    st.session_state.openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.get("openai_api_key", os.getenv("OPENAI_API_KEY", "")),
        placeholder="sk-...",
    )
    st.session_state.groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.get("groq_api_key", os.getenv("GROQ_API_KEY", "")),
        placeholder="gsk_...",
    )

    st.divider()
    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful, advanced AI assistant. Answer clearly, accurately, and in the same language as the user unless asked otherwise.",
        height=120,
    )

    if st.button("🧹 Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_provider = None
        st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_area("💬 Enter your prompt", height=130, placeholder="Type your message here...")

with col2:
    uploaded_image = st.file_uploader(
        "🖼️ Upload image (OpenAI only)",
        type=["png", "jpg", "jpeg"],
        help="200MB per file · PNG, JPG, JPEG",
    )

if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded image preview", use_container_width=True)
    st.markdown('<div class="small-note">Image analysis OpenAI ke through chalegi.</div>', unsafe_allow_html=True)

send_col, info_col = st.columns([1, 2])
with send_col:
    send = st.button("🚀 Send", use_container_width=True, type="primary")
with info_col:
    if st.session_state.last_provider:
        st.info(f"Last successful provider: {st.session_state.last_provider}")

st.divider()
st.subheader("🧠 Chat")

for msg in st.session_state.messages:
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

if send:
    if not prompt.strip():
        st.warning("Please prompt likhein.")
    else:
        image_data_url = None
        if uploaded_image is not None:
            image_data_url = file_to_data_url(uploaded_image)

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = ask_ai(
                        preferred_provider=preferred_provider,
                        openai_model=openai_model,
                        groq_model=groq_model,
                        prompt=prompt,
                        system_prompt=system_prompt,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        image_data_url=image_data_url,
                    )
                    st.session_state.last_provider = result["provider"]
                    reply = result["content"]
                    st.success(f"Response generated via {result['provider']}")
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    error_message = str(e)
                    st.error("❌ Request failed")
                    st.markdown(
                        f"""
                        <div class="status-box err-box">
                        <strong>Details:</strong> {error_message}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.info(
                        "Common fixes: OpenAI/Groq API key check karein, billing/quota verify karein, aur model availability confirm karein."
                    )

st.divider()
with st.expander("🛠️ Why your old app was failing"):
    st.markdown(
        """
        1. Error `openai.RateLimitError` ka matlab hota hai ke OpenAI side par quota, billing, ya request limit issue aa gaya.

        2. Aapke traceback se lag raha hai ke fallback handling bhi properly isolate nahi thi, is liye app ne clean user-friendly error dikhane ke bajaye raw failure expose kar diya.

        3. Is updated version mein:
        - OpenAI aur Groq dono supported hain
        - Proper fallback logic hai
        - Rate-limit aur auth errors ke liye readable messages hain
        - Image upload sirf OpenAI path mein handle hota hai
        - Chat history محفوظ rehti hai
        """
        )
                
