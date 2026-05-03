"""
CSS styling module for Milo AI.
Handles UI styling for authentication and chat interfaces.
"""

import streamlit as st


def load_auth_css() -> None:
    """Load CSS styles for authentication pages"""
    st.markdown(""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* ========== GLOBAL STYLES ========== */
    .stApp {
        background: radial-gradient(circle at top left, #102117, #060d07 60%);
        color: #ddeae0;
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }

    /* ========== AUTH BRANDING ========== */
    .auth-logo {
        font-size: 42px;
        text-align: center;
        margin-bottom: 4px;
    }

    .auth-appname {
        text-align: center;
        color: #7aab8a;
        letter-spacing: 0.22em;
        font-size: 13px;
        margin-bottom: 18px;
        font-weight: 600;
    }

    .auth-heading {
        text-align: center;
        font-size: 28px;
        color: #f0ead8;
        font-family: 'Lora', serif;
        margin-bottom: 6px;
        font-weight: 600;
    }

    .auth-subheading {
        text-align: center;
        color: #6a8f74;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 24px;
    }

    /* ========== FORM INPUTS ========== */
    .field-label {
        font-size: 13px;
        font-weight: 600;
        color: #c9d4ce;
        margin-bottom: 6px;
        display: block;
    }

    .stTextInput input {
        background: #111c14 !important;
        color: #fff !important;
        border: 1px solid rgba(122, 171, 138, 0.18) !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
    }

    .stTextInput input:focus {
        border-color: rgba(122, 171, 138, 0.4) !important;
        box-shadow: 0 0 0 3px rgba(122, 171, 138, 0.1) !important;
    }

    /* ========== CAPTCHA ========== */
    .captcha-box {
        background: #0a1310;
        border: 1px solid rgba(122, 171, 138, 0.2);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    }

    .captcha-question {
        color: #7aab8a;
        font-size: 16px;
        font-weight: 600;
        font-family: 'Courier New', monospace;
    }

    /* ========== BUTTONS ========== */
    .stButton button {
        width: 100%;
        border: none !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #7aab8a, #4d8a62) !important;
        color: #071009 !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #8abc9a, #5e9975) !important;
        transform: translateY(-2px);
    }

    /* ========== PASSWORD STRENGTH METER ========== */
    .strength-bar-wrap {
        background: #0a1310;
        border: 1px solid rgba(122, 171, 138, 0.2);
        border-radius: 8px;
        height: 6px;
        overflow: hidden;
        margin-bottom: 8px;
    }

    .strength-bar {
        height: 100%;
        transition: all 0.3s ease;
    }

    .strength-label {
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
    }

    /* ========== ALERTS ========== */
    .stAlert {
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    .st-emotion-cache-13ln4kf {
        border-radius: 12px !important;
    }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .auth-heading {
            font-size: 24px;
        }
        
        .auth-logo {
            font-size: 36px;
        }
    }
    </style>
    \"\"\", unsafe_allow_html=True)


def load_chat_css() -> None:
    \"\"\"Load CSS styles for chat interface\"\"\"
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    /* ========== GLOBAL STYLES ========== */
    .stApp {
        background: #f8f9fa !important;
        color: #1a1a1a !important;
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }

    .main .block-container {
        padding-bottom: 110px !important;
    }

    /* ========== HEADER ========== */
    .chat-header {
        background: linear-gradient(135deg, #102117, #1a3520);
        color: white;
        padding: 20px 24px;
        border-bottom: 1px solid rgba(122, 171, 138, 0.1);
    }

    .chat-header-title {
        font-size: 24px;
        font-weight: 700;
        margin: 0;
    }

    .chat-header-subtitle {
        font-size: 13px;
        color: #7aab8a;
        margin-top: 4px;
    }

    /* ========== SIDEBAR ========== */
    .stSidebar {
        background: #ffffff !important;
        border-right: 1px solid #e8eef0;
    }

    .stSidebar .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #7aab8a, #4d8a62) !important;
        border-radius: 10px !important;
        margin-bottom: 12px;
    }

    .chat-item {
        padding: 12px;
        background: #f5f6f7;
        border-radius: 10px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        border-left: 3px solid transparent;
    }

    .chat-item:hover {
        background: #eef2f5;
        border-left-color: #7aab8a;
    }

    .chat-item-active {
        background: #e8f5e9;
        border-left-color: #7aab8a;
    }

    /* ========== MESSAGES ========== */
    .message-container {
        margin-bottom: 16px;
        display: flex;
        animation: slideIn 0.3s ease;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .user-message {
        justify-content: flex-end;
    }

    .assistant-message {
        justify-content: flex-start;
    }

    .message-bubble {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 16px;
        line-height: 1.5;
        font-size: 14px;
    }

    .user-bubble {
        background: linear-gradient(135deg, #7aab8a, #4d8a62);
        color: white;
        border-bottom-right-radius: 4px;
    }

    .assistant-bubble {
        background: #f0f0f0;
        color: #1a1a1a;
        border-bottom-left-radius: 4px;
        border: 1px solid #e0e0e0;
    }

    /* ========== INPUT AREA ========== */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e8eef0;
        padding: 16px 24px;
        box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
    }

    .stTextArea textarea {
        background: #f5f6f7 !important;
        color: #1a1a1a !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
    }

    .stTextArea textarea:focus {
        border-color: #7aab8a !important;
        box-shadow: 0 0 0 3px rgba(122, 171, 138, 0.1) !important;
    }

    /* ========== SENTIMENT INDICATOR ========== */
    .sentiment-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 8px;
    }

    .sentiment-high-risk {
        background: #ffebee;
        color: #c62828;
        border: 1px solid #ef5350;
    }

    .sentiment-low-risk {
        background: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #66bb6a;
    }

    /* ========== EMPTY STATE ========== */
    .empty-state {
        text-align: center;
        padding: 60px 24px;
        color: #999;
    }

    .empty-state-icon {
        font-size: 48px;
        margin-bottom: 16px;
    }

    .empty-state-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 8px;
        color: #333;
    }

    .empty-state-text {
        font-size: 14px;
        color: #999;
    }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 768px) {
        .message-bubble {
            max-width: 85%;
        }
        
        .chat-input-container {
            padding: 12px 16px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def load_custom_css() -> None:
    """Load combined custom CSS for entire app"""
    # This combines both auth and chat styles
    load_auth_css()
    load_chat_css()
