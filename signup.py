import re
import random
import streamlit as st
from auth_service import AuthService
from exceptions import UserAlreadyExistsError, ValidationError, AuthenticationError
from logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def _is_valid_email(email: str) -> bool:
    return bool(re.match(r'^[\w\.\+\-]+@[\w\-]+\.\w{2,}$', email))


def _password_strength(password: str) -> tuple[int, str, str]:
    if len(password) == 0:
        return 0, "", "#243328"
    if len(password) < 8:
        return 1, "Too short", "#e07070"
    score = 0
    if re.search(r'[A-Z]', password):         score += 1
    if re.search(r'[0-9]', password):         score += 1
    if re.search(r'[^A-Za-z0-9]', password):  score += 1
    if len(password) >= 12:                   score += 1
    score = max(1, min(score, 4))
    labels  = {1: "Weak", 2: "Fair", 3: "Good", 4: "Strong"}
    colours = {1: "#e07070", 2: "#c9a84c", 3: "#7aab8a", 4: "#5db87a"}
    return score, labels[score], colours[score]


def _init_captcha():
    """Generate a fresh math CAPTCHA and store in session state."""
    a  = random.randint(2, 15)
    b  = random.randint(2, 15)
    op = random.choice(["+", "-", "×"])
    if op == "+":
        answer = a + b
    elif op == "-":
        a, b   = max(a, b), min(a, b)
        answer = a - b
    else:
        a      = random.randint(2, 9)
        b      = random.randint(2, 9)
        answer = a * b

    st.session_state["su_captcha_question"] = f"{a} {op} {b} = ?"
    st.session_state["su_captcha_answer"]   = answer


def show_signup() -> None:
    # ── Init CAPTCHA once ──
    if "su_captcha_answer" not in st.session_state:
        _init_captcha()

    st.markdown("<div style='height:4vh'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        # ── Branding ──
        st.markdown("""
        <div class="auth-logo">🌿</div>
        <div class="auth-appname">Milo AI</div>
        <div class="auth-heading">You're not alone</div>
        <div class="auth-subheading">
            Create your space. Milo is here to listen, reflect, and support you.
        </div>
        """, unsafe_allow_html=True)

        # ── Email ──
        st.markdown('<div class="field-label">Email address</div>', unsafe_allow_html=True)
        email = st.text_input(
            "email", label_visibility="collapsed",
            placeholder="you@example.com", key="signup_email"
        )

        # ── Password ──
        st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
        password = st.text_input(
            "password", label_visibility="collapsed",
            type="password", placeholder="Min. 8 characters", key="signup_password"
        )

        # ── Live strength meter ──
        if password:
            score, label, colour = _password_strength(password)
            pct = int((score / 4) * 100)
            st.markdown(f"""
            <div class="strength-bar-wrap">
              <div class="strength-bar" style="width:{pct}%; background:{colour};"></div>
            </div>
            <div class="strength-label" style="color:{colour};">{label}</div>
            """, unsafe_allow_html=True)

        # ── Confirm password ──
        st.markdown('<div class="field-label">Confirm password</div>', unsafe_allow_html=True)
        confirm = st.text_input(
            "confirm", label_visibility="collapsed",
            type="password", placeholder="Repeat your password", key="signup_confirm"
        )

        # ── Inline match hint ──
        if confirm and password:
            if password == confirm:
                st.markdown('<div class="strength-label" style="color:#5db87a;">✓ Passwords match</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="strength-label" style="color:#e07070;">✗ Passwords don\'t match</div>', unsafe_allow_html=True)

        # ── CAPTCHA ──
        st.markdown(f"""
        <div class="field-label">Verify you're human</div>
        <div class="captcha-box">
            <span class="captcha-question">🔢 {st.session_state["su_captcha_question"]}</span>
        </div>
        """, unsafe_allow_html=True)

        captcha_input = st.text_input(
            "captcha", label_visibility="collapsed",
            placeholder="Type the answer here", key="signup_captcha"
        )

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        signup_clicked  = st.button("Create my account  →", key="signup_btn", use_container_width=True)
        msg_placeholder = st.empty()

        if signup_clicked:
            error = None

            if not email or not password or not confirm or not captcha_input:
                error = "Please fill in all fields to get started."
            elif not _is_valid_email(email):
                error = "That doesn't look like a valid email. Please double-check."
            elif len(password) < 8:
                error = "Your password needs to be at least 8 characters."
            elif password != confirm:
                error = "Passwords don't match — please try again."

            if error:
                msg_placeholder.error(error)

            else:
                # ── Validate CAPTCHA ──
                try:
                    user_answer = int(captcha_input.strip())
                except ValueError:
                    user_answer = None

                if user_answer != st.session_state["su_captcha_answer"]:
                    msg_placeholder.error("❌ Wrong answer — please try the math question again.")
                    _init_captcha()
                    st.rerun()

                else:
                    # ── Attempt signup ──
                    try:
                        result = AuthService.signup(email.strip().lower(), password)
                        
                        msg_placeholder.success("Welcome to Milo 🌿 Redirecting you now…")
                        _init_captcha()
                        st.session_state.page = "login"
                        st.rerun()
                        
                    except UserAlreadyExistsError:
                        msg_placeholder.error("An account with this email already exists.")
                        _init_captcha()
                    except ValidationError as e:
                        msg_placeholder.error(f"Validation error: {str(e)}")
                        _init_captcha()
                    except Exception as e:
                        logger.error(f"Signup error: {str(e)}")
                        msg_placeholder.error("Could not create account. Please try again.")
                        _init_captcha()

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("Already have an account? Sign in →", key="go_login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

        st.markdown("""
        <div class="milo-tagline">"Healing is not linear — and that's okay."</div>
        """, unsafe_allow_html=True)