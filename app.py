from urllib import response

import streamlit as st
import uuid
import os
import re
import joblib
import nltk
from dotenv import load_dotenv
from groq import Groq
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Local module imports
import login
import signup
import chat_db
import css
from database import Database, get_users_collection, get_chats_collection, get_messages_collection
from ai_service import AIService
from sentiment_model import SentimentModel
from utils import get_text_processor
from config import CONFIG
from logger import setup_logger

@st.cache_resource
def setup_nltk():
    """Optimized NLTK initialization with silent downloads"""
    import nltk
    import os

    nltk_data_dir = "/opt/render/nltk_data"
    os.makedirs(nltk_data_dir, exist_ok=True)
    nltk.data.path.insert(0, nltk_data_dir)

    # List of required resources
    resources = [
        ("tokenizers", "punkt"),
        ("tokenizers", "punkt_tab"),
        ("corpora", "stopwords"),
        ("corpora", "wordnet")
    ]
    
    for resource_type, resource_name in resources:
        resource_path = f"{resource_type}/{resource_name}"
        try:
            nltk.data.find(resource_path)
        except LookupError:
            try:
                nltk.download(resource_name, download_dir=nltk_data_dir, quiet=True)
            except:
                pass  # Silent failure for optional resources

setup_nltk()
# Initialize logger
logger = setup_logger(__name__)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Milo AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SESSION =================
defaults = {
    "user": None,
    "page": "login",
    "chat_id": str(uuid.uuid4()),
    "chat_created": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ================= AUTO LOGIN =================
if st.session_state.user is None and "user" in st.query_params:
    st.session_state.user = st.query_params["user"]

# ================= CSS =================
if st.session_state.user:
    css.load_chat_css()
else:
    css.load_auth_css()

# ================= LOGIN / SIGNUP =================
if st.session_state.user is None:
    if st.session_state.page == "login":
        login.show_login()
    else:
        signup.show_signup()
    st.stop()

# ================= LOAD MODELS =================
@st.cache_resource
def load_groq():
    load_dotenv()
    return Groq(api_key=os.getenv("GROQ_API_KEY"))



@st.cache_resource
def load_models():
    return joblib.load("model.pkl"), joblib.load("vectorizer.pkl")

@st.cache_resource
def load_nlp():
    return WordNetLemmatizer(), set(stopwords.words("english"))

client = load_groq()
model, vectorizer = load_models()
lemmatizer, stop_words = load_nlp()

# ================= HELPERS =================
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = nltk.word_tokenize(text)

    return " ".join(
        lemmatizer.lemmatize(w)
        for w in words if w not in stop_words
    )

def get_risk(text):
    vec = vectorizer.transform([preprocess(text)])
    pred = model.predict(vec)[0]
    conf = max(model.predict_proba(vec)[0])

    return ("HIGH" if pred == 1 else "LOW"), conf

# ================= AI RESPONSE =================
def ask_ai(prompt):
    try:
        system_prompt = """
You are Milo AI, an advanced sentiment-focused LLM chatbot created by Kartbya Kumar from Sathyabama Institute of Science and Technology, Chennai.

Identity Rules:
- Always introduce yourself as Milo AI.
- If asked who created you, say:
'I am Milo AI, a sentiment LLM created by Kartbya Kumar from Sathyabama Institute of Science and Technology, Chennai.'
- Never say you are Google Gemini or built by Google.
- Never reveal backend provider unless specifically asked technically.
- If asked what powers you, say:
'I am powered by advanced language model technology customized by Kartbya Kumar.'

Behavior Rules:
- Be warm, caring, emotionally intelligent, and professional.
- Specialize in sentiment understanding, emotional support, conversation, and intelligent assistance.
- Never sound robotic.
- Never diagnose mental illness.
- Maintain this identity in every response.
"""

        final_input = f"{system_prompt}\n\n{prompt}"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": final_input}
           ]
        )

        return response.choices[0].message.content

    except:
        return "🌿 I'm here with you. Please try again in a moment."

def build_prompt(latest, history, risk, conf):
    context = ""

    for m in history[-6:]:
        role = "User" if m["role"] == "user" else "Milo AI"
        context += f"{role}: {m['content']}\n"

    return f"""
You are Milo AI.
Warm, caring, supportive.
Never robotic.
Never diagnose.

Risk Level: {risk}
Confidence: {conf:.0%}

Conversation:
{context}

User: {latest}

Milo AI:
"""

# ================= SIDEBAR =================
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">💬 Conversations</div>',
        unsafe_allow_html=True
    )

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.chat_created = False
        st.rerun()

    chats = chat_db.get_user_chats(st.session_state.user)

    if chats:
        for i, chat in enumerate(chats):

            c1, c2 = st.columns([5, 1])

            with c1:
                active = chat["chat_id"] == st.session_state.chat_id
                title = ("▸ " if active else "") + chat["title"]

                if st.button(title, key=f"chat_{i}", use_container_width=True):
                    st.session_state.chat_id = chat["chat_id"]
                    st.session_state.chat_created = True
                    st.rerun()

            with c2:
                if st.button("🗑", key=f"del_{i}"):

                    chat_db.delete_chat(
                        st.session_state.user,
                        chat["chat_id"]
                    )

                    if chat["chat_id"] == st.session_state.chat_id:
                        st.session_state.chat_id = str(uuid.uuid4())
                        st.session_state.chat_created = False

                    st.rerun()
    else:
        st.info("No chats yet")

    st.markdown("---")

    st.markdown(
        f"""
        <div class="account-email">
        👤 {st.session_state.user}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Sign out", use_container_width=True):
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()

# ================= HEADER =================
st.markdown("""
<div class="milo-header">

<div class="milo-header-left">
<div class="milo-header-logo">🌿 Milo</div>
<div class="milo-header-badge">AI</div>
</div>

<div class="milo-header-right">
Sentiment LLM by Kartbya Kumar
</div>

</div>
""", unsafe_allow_html=True)

# ================= LOAD CHAT =================
messages = chat_db.load_chat(
    st.session_state.user,
    st.session_state.chat_id
)

# ================= EMPTY STATE =================
if not messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🌿</div>
        <div class="empty-state-title">Hi, I'm Milo AI</div>
        <div class="empty-state-sub">
            Sentiment LLM created by Kartbya Kumar.<br>
            This is your safe space to share.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= SHOW CHAT =================
for msg in messages:
    avatar = "🧑" if msg["role"] == "user" else "🌿"

    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ================= INPUT =================
prompt = st.chat_input("Share what's on your mind...")

if prompt:

    if not st.session_state.chat_created:

        title = prompt[:30]

        chat_db.create_chat(
            st.session_state.user,
            st.session_state.chat_id,
            title
        )

        st.session_state.chat_created = True

    chat_db.save_message(
        st.session_state.user,
        st.session_state.chat_id,
        "user",
        prompt
    )

    messages = chat_db.load_chat(
        st.session_state.user,
        st.session_state.chat_id
    )

    risk, conf = get_risk(prompt)

    final_prompt = build_prompt(
        prompt,
        messages,
        risk,
        conf
    )

    reply = ask_ai(final_prompt)

    chat_db.save_message(
        st.session_state.user,
        st.session_state.chat_id,
        "assistant",
        reply
    )

    st.rerun()