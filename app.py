import streamlit as st  
import json  
import os  
from datetime import datetime  
from groq import Groq  
import hashlib  
import re  
import base64  
import pyttsx3  
from io import BytesIO  

# ===== CONFIGURATION =====  
st.set_page_config(  
    page_title="NEXUS Pro AI",  
    page_icon="🤖",  
    layout="wide",  
    initial_sidebar_state="collapsed"  
)  

# ===== ADVANCED CUSTOM CSS =====  
st.markdown("""  
<style>  
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');  

* {  
    font-family: 'Inter', sans-serif;  
    box-sizing: border-box;  
}  

/* Main Gradient Background */  
.stApp {  
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);  
}  

/* Main Container */  
.main-container {  
    max-width: 1000px;  
    margin: 0 auto;  
    padding: 1rem;  
}  

/* Animated Header */  
.main-header {  
    font-size: 3rem !important;  
    font-weight: 800 !important;  
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);  
    -webkit-background-clip: text;  
    -webkit-text-fill-color: transparent;  
    text-align: center;  
    margin: 1.5rem 0 0.5rem 0;  
    letter-spacing: -1px;  
    animation: gradientShift 3s ease infinite;  
    background-size: 200% 200%;  
}  

@keyframes gradientShift {  
    0% { background-position: 0% 50%; }  
    50% { background-position: 100% 50%; }  
    100% { background-position: 0% 50%; }  
}  

.sub-header {  
    text-align: center;  
    color: #64748b;  
    font-weight: 400;  
    margin-bottom: 2rem;  
    font-size: 1rem;  
}  

.sub-header span {  
    color: #a855f7;  
    font-weight: 600;  
}  

/* Enhanced Control Bar */  
.control-bar {  
    background: rgba(255,255,255,0.05);  
    backdrop-filter: blur(10px);  
    padding: 1rem 1.5rem;  
    border-radius: 16px;  
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);  
    margin-bottom: 1.5rem;  
    display: flex;  
    justify-content: space-between;  
    align-items: center;  
    border: 1px solid rgba(255,255,255,0.1);  
}  

.control-bar .title {  
    font-weight: 700;  
    color: #f1f5f9;  
    font-size: 1.2rem;  
}  

.control-bar .subtitle {  
    color: #94a3b8;  
    font-size: 0.85rem;  
}  

.status-indicator {  
    display: inline-block;  
    width: 10px;  
    height: 10px;  
    background: #10b981;  
    border-radius: 50%;  
    margin-right: 0.5rem;  
    animation: pulse 2s infinite;  
}  

@keyframes pulse {  
    0% { opacity: 1; }  
    50% { opacity: 0.5; }  
    100% { opacity: 1; }  
}  

/* Chat Container with Glass Effect */  
.chat-container {  
    height: 55vh;  
    overflow-y: auto;  
    padding: 1.5rem;  
    background: rgba(255,255,255,0.03);  
    backdrop-filter: blur(10px);  
    border-radius: 20px;  
    margin-bottom: 1rem;  
    border: 1px solid rgba(255,255,255,0.08);  
    scroll-behavior: smooth;  
}  

/* Modern Message Bubbles */  
.message {  
    margin-bottom: 1rem;  
    padding: 1rem 1.5rem;  
    border-radius: 20px;  
    max-width: 80%;
