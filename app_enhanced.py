"""
Milo AI - Mental Health and Sentiment Detection System
A compassionate AI chatbot for mental health support and sentiment analysis.

Created by: Kartbya Kumar
Institution: Sathyabama Institute of Science and Technology, Chennai
"""

import streamlit as st
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

# Import services
from database import Database
from ai_service import AIService, get_ai_response
from sentiment_model import SentimentModel, predict_sentiment
from chat_service import (
    create_new_chat,
    save_chat_message,
    load_chat_history,
    get_all_user_chats,
    delete_user_chat,
    rename_user_chat
)

# Import UI modules
import ui_login
import ui_signup
import ui_styles

# Import utilities
from logger import setup_logger
from exceptions import MiloException


# ===================== SETUP =====================

logger = setup_logger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Milo AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===================== SESSION STATE INITIALIZATION =====================

def initialize_session_state() -> None:
    """Initialize Streamlit session state variables"""
    defaults = {
        "user": None,
        "page": "login",
        "chat_id": str(uuid.uuid4()),
        "chat_created": False,
        "messages": [],
        "thinking": False,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ===================== AUTHENTICATION FLOW =====================

def handle_auto_login() -> None:
    """Handle automatic login from query parameters"""
    if st.session_state.user is None and "user" in st.query_params:
        st.session_state.user = st.query_params["user"]
        st.session_state.page = "chat"


def show_auth_pages() -> None:
    """Show authentication pages (login/signup)"""
    if st.session_state.page == "login":
        ui_login.show_login()
    else:
        ui_signup.show_signup()


# ===================== CHAT INTERFACE =====================

def render_chat_header() -> None:
    """Render chat interface header"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(
            "<div style='font-size:24px; font-weight:700; color:#102117;'>"
            "🌿 Milo AI</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='font-size:13px; color:#7aab8a;'>"
            "Your mental health support companion</div>",
            unsafe_allow_html=True
        )
    
    with col3:
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()


def render_sidebar() -> None:
    """Render chat sidebar with chat history"""
    with st.sidebar:
        st.markdown(
            "<div style='text-align:center; margin-bottom:20px;'>"
            "<h3>💬 Chats</h3></div>",
            unsafe_allow_html=True
        )
        
        # New chat button
        if st.button("➕ New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.chat_id = str(uuid.uuid4())
            st.session_state.chat_created = False
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Load and display chat history
        try:
            chats = get_all_user_chats(st.session_state.user, limit=20)
            
            if chats:
                for chat in chats:
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        if st.button(
                            f"💬 {chat['title'][:30]}\",
                            key=f"chat_{chat['chat_id']}\",
                            use_container_width=True
                        ):
                            st.session_state.chat_id = chat["chat_id"]
                            st.session_state.messages = load_chat_history(
                                st.session_state.user,
                                chat["chat_id"]
                            )
                            st.rerun()
                    
                    with col2:
                        if st.button(
                            "🗑️",
                            key=f"delete_{chat['chat_id']}",
                            help="Delete chat"
                        ):
                            delete_user_chat(st.session_state.user, chat["chat_id"])
                            st.rerun()
            else:
                st.markdown(
                    "<div style='text-align:center; color:#999; font-size:13px;'>"
                    "No chats yet. Start a new conversation!</div>",
                    unsafe_allow_html=True
                )
        
        except Exception as e:
            logger.error(f\"Error loading chat history: {str(e)}\")
            st.error(\"Failed to load chat history\")


def render_messages() -> None:
    \"\"\"Render chat messages\"\"\"
    if not st.session_state.messages:
        # Welcome message
        st.markdown(\"\"\"
        <div style='text-align:center; padding:60px 20px; color:#999;'>
            <div style='font-size:48px; margin-bottom:16px;'>🌿</div>
            <h2 style='color:#333;'>Welcome to Milo AI</h2>
            <p>Your safe space for mental health support.<br/>
            I'm here to listen, understand, and help you navigate your feelings.</p>
        </div>
        \"\"\", unsafe_allow_html=True)
    else:
        # Display messages
        for msg in st.session_state.messages:
            if msg[\"role\"] == \"user\":
                with st.chat_message(\"user\", avatar=\"👤\"):
                    st.markdown(msg[\"content\"])
            else:
                with st.chat_message(\"assistant\", avatar=\"🌿\"):
                    st.markdown(msg[\"content\"])


def handle_user_input() -> None:
    \"\"\"Handle user message input and AI response\"\"\"
    if prompt := st.chat_input(\"Share your thoughts...\"):
        try:
            # Add user message to session
            st.session_state.messages.append({
                \"role\": \"user\",
                \"content\": prompt
            })
            
            # Analyze sentiment
            try:
                risk_level, confidence, scores = predict_sentiment(prompt)
                sentiment_metadata = {
                    \"risk_level\": risk_level,
                    \"confidence\": float(confidence),
                    \"scores\": scores,
                    \"timestamp\": datetime.utcnow().isoformat()
                }
            except Exception as e:
                logger.warning(f\"Sentiment analysis failed: {str(e)}\")
                sentiment_metadata = {}
            
            # Create chat if not created yet
            if not st.session_state.chat_created:
                create_new_chat(
                    st.session_state.user,
                    st.session_state.chat_id,
                    prompt[:100]
                )
                st.session_state.chat_created = True
            
            # Save user message
            save_chat_message(
                st.session_state.user,
                st.session_state.chat_id,
                \"user\",
                prompt,
                metadata=sentiment_metadata
            )
            
            # Get AI response
            st.session_state.thinking = True
            st.rerun()
            
        except Exception as e:
            logger.error(f\"Error handling user input: {str(e)}\")
            st.error(\"Failed to process your message. Please try again.\")
    
    # Generate AI response if thinking
    if st.session_state.thinking:
        try:
            with st.spinner(\"🌿 Milo is thinking...\"):
                response = get_ai_response(st.session_state.messages)
            
            st.session_state.messages.append({
                \"role\": \"assistant\",
                \"content\": response
            })
            
            # Save assistant message
            save_chat_message(
                st.session_state.user,
                st.session_state.chat_id,
                \"assistant\",
                response
            )
            
            st.session_state.thinking = False
            st.rerun()
            
        except Exception as e:
            logger.error(f\"AI response error: {str(e)}\")
            error_msg = \"I'm having trouble responding right now. Please try again in a moment.\"
            st.session_state.messages.append({
                \"role\": \"assistant\",
                \"content\": error_msg
            })
            st.session_state.thinking = False
            st.rerun()


def show_chat_interface() -> None:
    \"\"\"Render the main chat interface\"\"\"
    render_chat_header()
    render_sidebar()
    
    # Main chat area
    st.markdown(\"<div style='height:20px'></div>\", unsafe_allow_html=True)
    
    render_messages()
    handle_user_input()


# ===================== MAIN APPLICATION =====================

def main() -> None:
    \"\"\"Main application entry point\"\"\"
    try:
        # Initialize session
        initialize_session_state()
        
        # Load appropriate CSS
        if st.session_state.user:
            ui_styles.load_chat_css()
        else:
            ui_styles.load_auth_css()
        
        # Handle auto-login
        handle_auto_login()
        
        # Initialize services
        try:
            Database.connect()
            AIService.initialize()
            SentimentModel.load()
        except Exception as e:
            logger.error(f\"Service initialization error: {str(e)}\")
            if st.session_state.user:
                st.error(\"⚠️ Failed to initialize services. Please refresh the page.\")
                return
        
        # Render appropriate page
        if st.session_state.user is None:
            show_auth_pages()
            st.stop()
        
        show_chat_interface()
        
    except MiloException as e:
        logger.error(f\"Milo exception: {str(e)}\")
        st.error(f\"⚠️ Error: {str(e)}\")
    except Exception as e:
        logger.error(f\"Unexpected error: {str(e)}\")
        st.error(f\"⚠️ An unexpected error occurred. Please refresh the page.\")


if __name__ == \"__main__\":
    main()
