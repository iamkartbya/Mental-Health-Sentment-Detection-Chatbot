import re
import random
import streamlit as st
import streamlit.components.v1 as components
from auth_service import AuthService
from exceptions import AuthenticationError, ValidationError
from logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def _is_valid_email(email: str) -> bool:
    return bool(re.match(r'^[\w\.\+\-]+@[\w\-]+\.\w{2,}$', email))


def _init_captcha():
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


def show_login() -> None:

    params = st.query_params

    if "user" in params and "user" not in st.session_state:
        st.session_state.user = params["user"]
        st.session_state.page = "chat"
        st.rerun()

    if "captcha_answer" not in st.session_state:
        _init_captcha()

    st.markdown("<div style='height:6vh'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.4, 1])

    with col:

        # ===== BRANDING =====
        st.markdown("""
        <div class="auth-logo">🌿</div>
        <div class="auth-appname">Milo AI</div>
        <div class="auth-heading">Welcome back</div>
        <div class="auth-subheading">
            You're safe here. Sign in and let's take it one step at a time.
        </div>
        """, unsafe_allow_html=True)

        # ===== EMAIL =====
        st.markdown(
            '<div class="field-label">Email address</div>',
            unsafe_allow_html=True
        )

        email = st.text_input(
            "email",
            label_visibility="collapsed",
            placeholder="you@example.com",
            key="login_email"
        )

        # ===== PASSWORD =====
        st.markdown(
            '<div class="field-label">Password</div>',
            unsafe_allow_html=True
        )

        password = st.text_input(
            "password",
            label_visibility="collapsed",
            type="password",
            placeholder="••••••••",
            key="login_password"
        )

        # ===== CAPTCHA =====
        st.markdown(f"""
        <div class="field-label">Verify the captcha</div>
        <div class="captcha-box">
            <span class="captcha-question">
                🔢 {st.session_state["captcha_question"]}
            </span>
        </div>
        """, unsafe_allow_html=True)

        captcha_input = st.text_input(
            "captcha",
            label_visibility="collapsed",
            placeholder="Type the answer here",
            key="login_captcha"
        )

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        # ===== LOGIN BUTTON =====
        login_clicked = st.button(
            "Sign in →",
            key="login_btn",
            use_container_width=True
        )

        msg_placeholder = st.empty()

        if login_clicked:

            if not email or not password or not captcha_input:
                msg_placeholder.error(
                    "Please fill in all fields to continue."
                )

            elif not _is_valid_email(email):
                msg_placeholder.error(
                    "That doesn't look like a valid email."
                )

            else:
                try:
                    user_answer = int(captcha_input.strip())
                except:
                    user_answer = None

                if user_answer != st.session_state["captcha_answer"]:
                    msg_placeholder.error(
                        "❌ Incorrect answer — Try again."
                    )
                    _init_captcha()
                    st.rerun()

                else:
                    msg_placeholder.info("Signing you in…")

                    try:
                        user = AuthService.login(
                            email.strip().lower(),
                            password
                        )
                    except (AuthenticationError, ValidationError) as e:
                        logger.error(f"Login error: {str(e)}")
                        msg_placeholder.error(
                            "⚠️ Authentication failed. Please try again."
                        )
                        st.stop()
                    except Exception as e:
                        logger.error(f"Unexpected error during login: {str(e)}")
                        msg_placeholder.error(
                            "⚠️ Can't reach server now."
                        )
                        st.stop()

                    if user:
                        st.session_state.user = user["username"]
                        st.session_state.page = "chat"
                        st.query_params["user"] = user["username"]
                        _init_captcha()
                        st.rerun()

                    else:
                        msg_placeholder.error(
                            "Incorrect email or password."
                        )
                        _init_captcha()

        # ===== SOCIAL TITLE =====
        st.markdown(
            '<div class="auth-divider">OR CONTINUE WITH</div>',
            unsafe_allow_html=True
        )

        # ===== SOCIAL BUTTONS =====
        components.html("""
        <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

        <style>
        body{
            margin:0;
            background:transparent;
            font-family:Arial;
        }
        .wrap{
            display:flex;
            gap:10px;
            justify-content:center;
            padding-top:4px;
        }
        .btn{
            background:#ffffff;
            padding:10px 14px;
            border-radius:12px;
            font-size:15px;
            font-weight:600;
            border:1px solid #ddd;
            min-width:135px;
            text-align:center;
            cursor:pointer;
        }
        .btn i{
            margin-right:8px;
        }
        </style>

        <div class="wrap">
            <div class="btn">
                <i class="fa-brands fa-google"></i> Google
            </div>

            <div class="btn">
                <i class="fa-brands fa-facebook-f"></i> Facebook
            </div>

            <div class="btn">
                <i class="fa-brands fa-telegram"></i> Telegram
            </div>
        </div>
        """, height=70)

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # ===== SIGNUP BUTTON =====
        if st.button(
            "Don't have an account? Join Milo →",
            key="go_signup",
            use_container_width=True
        ):
            st.session_state.page = "signup"
            st.rerun()

        # ===== FOOTER =====
        st.markdown("""
        <div class="milo-tagline">
            "Every storm runs out of rain."
        </div>
        """, unsafe_allow_html=True)