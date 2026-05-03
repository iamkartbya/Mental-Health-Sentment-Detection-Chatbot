"""
Login UI module for Milo AI.
Handles user authentication interface.
"""

import random
import streamlit as st
from auth_service import login_user
from exceptions import AuthenticationError, ValidationError, DatabaseError
from logger import setup_logger


logger = setup_logger(__name__)


# ===================== HELPER FUNCTIONS =====================

def _init_captcha() -> None:
    """Initialize captcha challenge and store in session state"""
    a = random.randint(2, 15)
    b = random.randint(2, 15)
    op = random.choice(["+", "-", "×"])
    
    if op == "+":
        answer = a + b
    elif op == "-":
        a, b = max(a, b), min(a, b)
        answer = a - b
    else:
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        answer = a * b
    
    st.session_state["captcha_question"] = f"{a} {op} {b} = ?"
    st.session_state["captcha_answer"] = answer


def _validate_captcha(user_answer: str) -> bool:
    \"\"\"
    Validate captcha answer.
    
    Args:
        user_answer: User's captcha answer
        
    Returns:
        bool: True if correct
    \"\"\"
    try:
        return int(user_answer) == st.session_state.get("captcha_answer", -1)
    except ValueError:
        return False


def _handle_login(email: str, password: str, captcha_answer: str) -> bool:
    \"\"\"
    Handle login logic.
    
    Args:
        email: User email
        password: User password
        captcha_answer: Captcha answer
        
    Returns:
        bool: True if login successful
    \"\"\"
    # Validate captcha first (fastest check)
    if not _validate_captcha(captcha_answer):
        st.error("❌ Captcha answer is incorrect. Please try again.")
        _init_captcha()
        return False
    
    # Validate inputs
    if not email or not password:
        st.error("❌ Please enter email and password")
        return False
    
    # Attempt login
    try:
        user = login_user(email, password)
        
        # Update session state
        st.session_state.user = email
        st.session_state.page = "chat"
        
        logger.info(f"User logged in: {email}")
        st.success("✅ Login successful! Redirecting...")
        st.rerun()
        return True
        
    except AuthenticationError as e:
        st.error(f\"❌ {str(e)}\")
        logger.warning(f\"Login failed for {email}: {str(e)}\")
        return False
    except ValidationError as e:
        st.error(f\"❌ Invalid input: {str(e)}\")
        return False
    except DatabaseError as e:
        st.error(f\"❌ Database error: {str(e)}\")
        logger.error(f\"Database error during login: {str(e)}\")
        return False
    except Exception as e:
        st.error(f\"❌ An unexpected error occurred: {str(e)}\")
        logger.error(f\"Unexpected error during login: {str(e)}\")
        return False


# ===================== UI RENDERING =====================

def show_login() -> None:
    \"\"\"Render login page\"\"\"
    
    # Initialize captcha on first load
    if \"captcha_answer\" not in st.session_state:
        _init_captcha()
    
    # Handle auto-login from query params
    if \"user\" in st.query_params and st.session_state.user is None:
        st.session_state.user = st.query_params[\"user\"]
        st.session_state.page = \"chat\"
        st.rerun()
    
    # Layout
    st.markdown(\"<div style='height:6vh'></div>\", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.4, 1])
    
    with col:
        # ========== BRANDING ==========
        st.markdown(\"\"\"
        <div class=\"auth-logo\">🌿</div>
        <div class=\"auth-appname\">Milo AI</div>
        <div class=\"auth-heading\">Welcome back</div>
        <div class=\"auth-subheading\">
            You're safe here. Sign in and let's take it one step at a time.
        </div>
        \"\"\", unsafe_allow_html=True)
        
        # ========== EMAIL INPUT ==========
        st.markdown(
            '<div class=\"field-label\">Email address</div>',
            unsafe_allow_html=True
        )
        email = st.text_input(
            \"email\",
            label_visibility=\"collapsed\",
            placeholder=\"you@example.com\",
            key=\"login_email\"
        )
        
        # ========== PASSWORD INPUT ==========
        st.markdown(
            '<div class=\"field-label\">Password</div>',
            unsafe_allow_html=True
        )
        password = st.text_input(
            \"password\",
            label_visibility=\"collapsed\",
            type=\"password\",
            placeholder=\"••••••••\",
            key=\"login_password\"
        )
        
        # ========== CAPTCHA ==========
        st.markdown(f\"\"\"
        <div class=\"field-label\">Verify the captcha</div>
        <div class=\"captcha-box\">
            <span class=\"captcha-question\">
                🔢 {st.session_state[\"captcha_question\"]}
            </span>
        </div>
        \"\"\", unsafe_allow_html=True)
        
        captcha_input = st.text_input(
            \"captcha\",
            label_visibility=\"collapsed\",
            placeholder=\"Type the answer here\",
            key=\"login_captcha\"
        )
        
        # ========== LOGIN BUTTON ==========
        st.markdown(\"<div style='height:12px'></div>\", unsafe_allow_html=True)
        
        if st.button(\"Sign In\", use_container_width=True, type=\"primary\"):
            _handle_login(email, password, captcha_input)
        
        # ========== SIGNUP LINK ==========
        st.markdown(\"<div style='height:16px'></div>\", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.8, 1])
        with col2:
            st.markdown(
                \"<div style='text-align:center; color:#7aab8a; font-size:13px;'>"
                \"Don't have an account? \",
                unsafe_allow_html=True
            )
            
            if st.button(\"Create one\", key=\"signup_link\", use_container_width=False):
                st.session_state.page = \"signup\"
                st.rerun()
            
            st.markdown(\"</div>\", unsafe_allow_html=True)
