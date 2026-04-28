import streamlit as st  
import json  
import os  
from datetime import datetime  
from groq import Groq  
import re  
import base64  

# ===== CONFIGURATION =====  
st.set_page_config(  
    page_title="NEXUS Pro AI",  
    page_icon="🤖",  
    layout="wide",  
    initial_sidebar_state="collapsed"  
)  

# ===== CUSTOM CSS =====  
st.markdown("""  
<style>  
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }  

.main-header {  
    font-size: 2.8rem !important;  
    font-weight: 800 !important;  
    background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);  
    -webkit-background-clip: text;  
    -webkit-text-fill-color: transparent;  
    text-align: center;  
    margin: 1.5rem 0 0.5rem 0;  
}  

.sub-header {  
    text-align: center;  
    color: #94a3b8;  
    margin-bottom: 2rem;  
    font-size: 1rem;  
}  

/* Control Bar */  
.control-bar {  
    background: white;  
    padding: 0.8rem 1.5rem;  
    border-radius: 16px;  
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);  
    margin-bottom: 1.5rem;  
    display: flex;  
    justify-content: space-between;  
    align-items: center;  
    border: 1px solid #f1f5f9;  
}  

.control-bar .title { font-weight: 600; color: #1e293b; font-size: 1.1rem; }  
.control-bar .subtitle { color: #94a3b8; font-size: 0.85rem; }  

/* Chat Container */  
.chat-container {  
    height: 55vh;  
    overflow-y: auto;  
    padding: 1.5rem;  
    background: linear-gradient(180deg, #f8fafc, #f1f5f9);  
    border-radius: 20px;  
    margin-bottom: 1rem;  
    border: 1px solid #e2e8f0;  
}  

/* Messages */  
.message {  
    margin-bottom: 1rem;  
    padding: 1rem 1.5rem;  
    border-radius: 16px;  
    max-width: 80%;  
    animation: fadeIn 0.3s ease;  
    line-height: 1.6;  
    position: relative;  
}  

.message-user {  
    background: linear-gradient(135deg, #3b82f6, #2563eb);  
    color: white;  
    margin-left: auto;  
    border-bottom-right-radius: 4px;  
}  

.message-ai {  
    background: linear-gradient(135deg, #10b981, #059669);  
    color: white;  
    margin-right: auto;  
    border-bottom-left-radius: 4px;  
}  

.message .meta {  
    font-size: 0.75rem;  
    opacity: 0.8;  
    margin-bottom: 0.4rem;  
    display: flex;  
    align-items: center;  
    gap: 0.5rem;  
}  

.message .actions {  
    position: absolute;  
    top: 0.5rem;  
    right: 0.5rem;  
    display: flex;  
    gap: 0.3rem;  
    opacity: 0;  
    transition: opacity 0.3s;  
}  

.message:hover .actions { opacity: 1; }  

.action-btn {  
    background: rgba(255,255,255,0.2);  
    border: none;  
    border-radius: 8px;  
    padding: 0.3rem 0.5rem;  
    color: white;  
    font-size: 0.8rem;  
    cursor: pointer;  
    transition: all 0.3s;  
}  

.action-btn:hover { background: rgba(255,255,255,0.4); transform: scale(1.1); }  

/* Empty State */  
.empty-state { text-align: center; padding: 4rem 2rem; color: #94a3b8; }  
.empty-state .icon { font-size: 4rem; margin-bottom: 1rem; }  
.empty-state h3 { color: #64748b; }  

/* Chat Input */  
.chat-input-container {  
    background: white;  
    padding: 0.8rem;
