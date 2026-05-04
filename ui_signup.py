"""
Signup UI module for Milo AI.
Handles user registration interface.
"""

import random
import streamlit as st
from auth_service import signup_user
from validators import calculate_password_strength
from exceptions import UserAlreadyExistsError, ValidationError, DatabaseError
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
    
    st.session_state["su_captcha_question"] = f"{a} {op} {b} = ?"
    st.session_state["su_captcha_answer"] = answer


def _validate_captcha(user_answer: str) -> bool:
    """Validate captcha answer"""
    try:
        return int(user_answer) == st.session_state.get("su_captcha_answer", -1)
    except ValueError:
        return False


def _validate_signup_form(
    email: str,
    password: str,
    confirm_password: str,
    captcha_answer: str
) -> tuple[bool, str]:
    """
    Validate signup form.
    
    Returns:
        tuple of (is_valid: bool, error_message: str)
    """
    if not email or not password or not confirm_password:
        return False, "All fields are required"
    
    if password != confirm_password:
        return False, "Passwords do not match"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not _validate_captcha(captcha_answer):
        return False, "Captcha answer is incorrect"
    
    return True, ""


def _handle_signup(
    email: str,
    password: str,
    confirm_password: str,
    captcha_answer: str
) -> bool:
    """
    Handle signup logic.
    
    Returns:
        bool: True if signup successful
    """
    # Validate form
    is_valid, error_msg = _validate_signup_form(
        email, password, confirm_password, captcha_answer
    )
    
    if not is_valid:
        st.error(f"❌ {error_msg}")
        _init_captcha()
        return False
    
    # Attempt signup
    try:
        user = signup_user(email, password)
        
        logger.info(f"New user registered: {email}")
        
        st.success("✅ Account created successfully!")
        st.info("You can now sign in with your credentials.")
        
        # Switch to login after brief delay
        import time
        time.sleep(1)
        st.session_state.page = "login"
        st.rerun()
        return True
        
    except UserAlreadyExistsError as e:
        st.error(f"❌ {str(e)}")
        logger.warning(f"Signup attempt with existing email: {email}")
        return False
    except ValidationError as e:
        st.error(f"❌ {str(e)}")
        return False
    except DatabaseError as e:
        st.error(f"❌ Database error: {str(e)}")
        logger.error(f"Database error during signup: {str(e)}")
        return False
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        logger.error(f"Unexpected error during signup: {str(e)}")
        return False


# ===================== UI RENDERING =====================

def show_signup() -> None:
    \"\"\"Render enhanced signup page\"\"\"
    
    # Initialize captcha on first load
    if \"su_captcha_answer\" not in st.session_state:
        _init_captcha()
    
    st.markdown(\"<div style='height:4vh'></div>\", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.4, 1])
    
    with col:
        # ========== BRANDING ==========
        st.markdown(\"\"\"
        <div class=\"auth-container\">
            <div class=\"auth-logo\">🌿</div>
            <div class=\"auth-appname\">Milo AI</div>
            <div class=\"auth-heading\">You're not alone</div>
            <div class=\"auth-subheading\">
                Create your space. Milo is here to listen, reflect, and support you.
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)
        
        st.markdown(\"<div style='height:8px'></div>\", unsafe_allow_html=True)
        
        # ========== EMAIL INPUT ==========
        st.markdown(
            '<div class=\"field-label\">📧 Email Address</div>',
            unsafe_allow_html=True
        )
        email = st.text_input(
            \"email\",
            label_visibility=\"collapsed\",
            placeholder=\"you@example.com\",
            key=\"signup_email\"
        )
        
        st.markdown(\"<div style='height:4px'></div>\", unsafe_allow_html=True)
        
        # ========== PASSWORD INPUT ==========
        st.markdown(
            '<div class=\"field-label\">🔒 Password</div>',
            unsafe_allow_html=True
        )
        password = st.text_input(
            \"password\",
            label_visibility=\"collapsed\",
            type=\"password\",
            placeholder=\"Min. 8 characters\",
            key=\"signup_password\"
        )
        
        # ========== PASSWORD STRENGTH METER ==========
        if password:
            score, label, color = calculate_password_strength(password)
            percentage = int((score / 4) * 100)
            
            st.markdown(f\"\"\"
            <div style=\"margin: 8px 0;\">
                <div class=\"strength-bar-wrap\">
                    <div class=\"strength-bar\" style=\"width:{percentage}%; background:{color}; transition: width 0.3s ease;\"></div>
                </div>
                <div class=\"strength-label\" style=\"color:{color}; margin-top: 4px;\">{label}</div>
            </div>
            \"\"\", unsafe_allow_html=True)
        
        st.markdown(\"<div style='height:4px'></div>\", unsafe_allow_html=True)
        
        # ========== CONFIRM PASSWORD ==========
        st.markdown(
            '<div class=\"field-label\">🔑 Confirm Password</div>',
            unsafe_allow_html=True
        )
        confirm_password = st.text_input(
            \"confirm\",
            label_visibility=\"collapsed\",
            type=\"password\",
            placeholder=\"Repeat your password\",
            key=\"signup_confirm\"
        )
        
        # ========== PASSWORD MATCH INDICATOR ==========
        if confirm_password and password:
            if password == confirm_password:
                st.markdown(
                    '<div class=\"strength-label\" style=\"color:#5db87a; margin-top: 4px;\">✓ Passwords match</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class=\"strength-label\" style=\"color:#e07070; margin-top: 4px;\">✗ Passwords do not match</div>',
                    unsafe_allow_html=True
                )
        
        st.markdown(\"<div style='height:12px'></div>\", unsafe_allow_html=True)
        
        # ========== CAPTCHA ==========
        st.markdown(
            '<div class=\"field-label\">🔢 Verify the Captcha</div>',
            unsafe_allow_html=True
        )
        st.markdown(f\"\"\"
        <div class=\"captcha-box\">
            <span class=\"captcha-question\">
                {st.session_state[\"su_captcha_question\"]}
            </span>
        </div>
        \"\"\", unsafe_allow_html=True)
        
        captcha_input = st.text_input(
            \"captcha\",
            label_visibility=\"collapsed\",
            placeholder=\"Type the answer here\",
            key=\"signup_captcha\"
        )
        
        # ========== SIGNUP BUTTON ==========
        st.markdown(\"<div style='height:16px'></div>\", unsafe_allow_html=True)
        
        if st.button(\"Create Account\", use_container_width=True, type=\"primary\"):
            _handle_signup(email, password, confirm_password, captcha_input)
        
        # ========== LOGIN LINK ==========
        st.markdown(\"<div style='height:20px'></div>\", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.8, 1])
        with col2:
            st.markdown(
                \"<div style='text-align:center; color:#8aa089; font-size:13px;'>"
                \"Already have an account? \",
                unsafe_allow_html=True
            )
            
            if st.button(\"Sign in\", key=\"login_link\", use_container_width=False):
                st.session_state.page = \"login\"
                st.rerun()
            
            st.markdown(\"</div>\", unsafe_allow_html=True)
