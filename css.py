import streamlit as st

# ================= AUTH CSS =================
def load_auth_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .stApp{
        background: linear-gradient(135deg, #0a1410 0%, #1a2e24 50%, #0f1b15 100%);
        color:#ddeae0;
        font-family:'DM Sans',sans-serif;
        min-height: 100vh;
        position: relative;
    }

    /* Animated background elements */
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        right: -50%;
        width: 100vw;
        height: 100vh;
        background: radial-gradient(circle, rgba(122, 171, 138, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: drift 20s linear infinite;
        z-index: -1;
        pointer-events: none;
    }

    @keyframes drift {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }

    #MainMenu, footer{visibility:hidden;}

    header{
        background:transparent !important;
    }

    .block-container{
        max-width:100% !important;
        padding:0 !important;
    }

    /* Auth Container */
    .auth-container {
        animation: slideIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .auth-logo{
        font-size:56px;
        text-align:center;
        margin-bottom:8px;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .auth-appname{
        text-align:center;
        color:#7aab8a;
        letter-spacing:.22em;
        font-size:13px;
        margin-bottom:18px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .auth-heading{
        text-align:center;
        font-size:32px;
        color:#f0ead8;
        font-family:'Playfair Display',serif;
        margin-bottom:8px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .auth-subheading{
        text-align:center;
        color:#8aa089;
        font-size:14px;
        line-height:1.8;
        margin-bottom:32px;
        font-weight: 300;
    }

    /* Field Label */
    .field-label {
        color: #a8d5af;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        display: block;
    }

    /* Input Styling */
    .stTextInput input{
        background: rgba(17, 28, 20, 0.8) !important;
        color:#f0ead8 !important;
        border: 1.5px solid rgba(122, 171, 138, 0.25) !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
    }

    .stTextInput input:hover {
        border-color: rgba(122, 171, 138, 0.45) !important;
        box-shadow: 0 0 20px rgba(122, 171, 138, 0.1) !important;
    }

    .stTextInput input:focus {
        border-color: #7aab8a !important;
        box-shadow: 0 0 30px rgba(122, 171, 138, 0.2) !important;
        background: rgba(17, 28, 20, 0.95) !important;
    }

    /* Input Placeholder */
    .stTextInput input::placeholder {
        color: rgba(166, 189, 166, 0.5) !important;
    }

    /* Button Styling */
    .stButton button {
        width: 100%;
        border: none !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, #7aab8a 0%, #5a9b7a 100%) !important;
        color: #071009 !important;
        font-weight: 700 !important;
        padding: 14px 24px !important;
        font-size: 15px !important;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 8px 24px rgba(122, 171, 138, 0.2) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        cursor: pointer;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #8ac19a 0%, #6aab8a 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 32px rgba(122, 171, 138, 0.3) !important;
    }

    .stButton button:active {
        transform: translateY(0) !important;
        box-shadow: 0 4px 16px rgba(122, 171, 138, 0.2) !important;
    }

    /* Captcha Box */
    .captcha-box {
        background: rgba(122, 171, 138, 0.08);
        border: 1.5px dashed rgba(122, 171, 138, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        text-align: center;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    .captcha-question {
        color: #f0ead8;
        font-weight: 600;
        font-size: 16px;
        font-family: 'Courier New', monospace;
    }

    /* Links */
    a {
        color: #7aab8a !important;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    a:hover {
        color: #a8d5af !important;
        text-decoration: underline;
    }

    /* Loading Animation */
    .stSpinner {
        color: #7aab8a !important;
    }

    /* Error/Success Messages */
    .stAlert {
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .stAlert > div {
        animation: slideInAlert 0.3s ease;
    }

    @keyframes slideInAlert {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(122, 171, 138, 0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(122, 171, 138, 0.3);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(122, 171, 138, 0.5);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .auth-logo {
            font-size: 42px;
        }

        .auth-heading {
            font-size: 24px;
        }

        .auth-subheading {
            font-size: 13px;
        }

        .stButton button {
            padding: 12px 20px !important;
            font-size: 14px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)


# ================= CHAT CSS =================
def load_chat_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    /* GLOBAL */
    .stApp{
        background: linear-gradient(135deg, #f8fafb 0%, #f0f3f6 100%) !important;
        color:#111 !important;
        font-family:'DM Sans',sans-serif;
    }

    #MainMenu, footer{
        visibility:hidden;
    }

    .block-container{
        max-width:100% !important;
        padding:0 !important;
    }

    .main .block-container{
        padding-bottom:110px !important;
    }

    /* KEEP TOOLBAR + SIDEBAR BUTTON */
    header{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafb 100%) !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        height:3rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    header [data-testid="stToolbar"]{
        display:flex !important;
        visibility:visible !important;
    }

    header [data-testid="stSidebarCollapsedControl"]{
        display:flex !important;
        visibility:visible !important;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"]{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafb 100%) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.08);
        width:310px !important;
        min-width:310px !important;
    }

    section[data-testid="stSidebar"] .block-container{
        padding:18px 14px !important;
    }

    .sidebar-title{
        color:#111;
        font-size:12px;
        font-weight:700;
        margin-bottom:14px;
        text-transform:uppercase;
        letter-spacing:.08em;
        color: #7aab8a;
    }

    section[data-testid="stSidebar"] .stButton button{
        width:100%;
        background:#fff !important;
        color:#111 !important;
        border: 1.5px solid #e5e5e5 !important;
        border-radius:12px !important;
        padding:10px 14px !important;
        margin-bottom:8px !important;
        text-align:left !important;
        transition: all 0.3s ease !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover{
        background: linear-gradient(135deg, #f1f1f1 0%, #e8e8e8 100%) !important;
        border-color: #7aab8a !important;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(122, 171, 138, 0.1) !important;
    }

    .account-email{
        background:#fff;
        border: 1.5px solid #e5e5e5;
        border-radius:12px;
        padding:12px;
        font-size:13px;
        color:#111;
        margin-top:12px;
        margin-bottom:10px;
        word-break:break-word;
        transition: all 0.3s ease;
    }

    .account-email:hover {
        border-color: #7aab8a;
        box-shadow: 0 4px 12px rgba(122, 171, 138, 0.08);
    }

    /* HEADER */
    .milo-header{
        margin-top:3rem;
        padding:18px 28px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        background: linear-gradient(135deg, #ffffff 0%, #f8fafb 100%);
    }

    .milo-header-left{
        display:flex;
        align-items:center;
        gap:12px;
    }

    .milo-header-logo{
        font-size:30px;
        font-weight:700;
        color: #7aab8a;
        animation: subtle-glow 3s ease-in-out infinite;
    }

    @keyframes subtle-glow {
        0%, 100% { text-shadow: 0 0 0 rgba(122, 171, 138, 0); }
        50% { text-shadow: 0 0 8px rgba(122, 171, 138, 0.2); }
    }

    .milo-header-badge{
        background: linear-gradient(135deg, #7aab8a20 0%, #7aab8a10 100%);
        color: #7aab8a;
        font-size:11px;
        padding:4px 10px;
        border-radius:999px;
        font-weight:700;
        border: 1px solid rgba(122, 171, 138, 0.3);
    }

    .milo-header-right{
        font-size:14px;
        color:#666;
    }

    /* EMPTY STATE */
    .empty-state{
        max-width:900px;
        margin:60px auto 0 auto;
        text-align:center;
        padding:20px;
        animation: fadeIn 0.6s ease-out;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .empty-state-icon{
        font-size:52px;
        animation: float 3s ease-in-out infinite;
    }

    .empty-state-title{
        font-size:28px;
        font-weight:700;
        margin-top:10px;
        color: #111;
    }

    .empty-state-sub{
        color:#666;
        line-height:1.8;
        font-size:16px;
        margin-top:12px;
    }

    /* CHAT */
    [data-testid="stChatMessage"]{
        max-width:900px;
        margin:auto;
        padding:8px 24px !important;
        animation: slideInChat 0.3s ease-out;
    }

    @keyframes slideInChat {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* user right */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){
        justify-content:flex-end;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown{
        background: linear-gradient(135deg, #7aab8a 0%, #5a9b7a 100%);
        color:#fff;
        padding:14px 16px;
        border-radius:18px 18px 6px 18px;
        max-width:75%;
        margin-left:auto;
        box-shadow: 0 4px 12px rgba(122, 171, 138, 0.2);
        transition: all 0.3s ease;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown:hover {
        box-shadow: 0 6px 16px rgba(122, 171, 138, 0.3);
        transform: translateY(-2px);
    }

    /* bot left */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown{
        background: linear-gradient(135deg, #f4f4f4 0%, #efefef 100%);
        color:#111;
        padding:14px 16px;
        border-radius:18px 18px 18px 6px;
        max-width:75%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    /* INPUT */
    [data-testid="stBottom"],
    [data-testid="stBottom"]>div{
        background: linear-gradient(135deg, #ffffff 0%, #f8fafb 100%) !important;
        border-top: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.04);
    }

    [data-testid="stChatInput"]{
        max-width:900px;
        margin:auto;
        padding:14px 18px !important;
    }

    [data-testid="stChatInput"] textarea{
        background:#fff !important;
        color:#111 !important;
        border: 1.5px solid #ddd !important;
        border-radius:18px !important;
        min-height:56px !important;
        transition: all 0.3s ease !important;
        font-size: 14px !important;
    }

    [data-testid="stChatInput"] textarea:hover {
        border-color: rgba(122, 171, 138, 0.3) !important;
        box-shadow: 0 4px 12px rgba(122, 171, 138, 0.08) !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        border-color: #7aab8a !important;
        box-shadow: 0 4px 16px rgba(122, 171, 138, 0.15) !important;
    }

    [data-testid="stChatInput"] button{
        background: linear-gradient(135deg, #7aab8a 0%, #5a9b7a 100%) !important;
        color:#fff !important;
        border:none !important;
        border-radius:12px !important;
        width:44px !important;
        height:44px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(122, 171, 138, 0.2) !important;
    }

    [data-testid="stChatInput"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(122, 171, 138, 0.3) !important;
    }

    [data-testid="stChatInput"] button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(122, 171, 138, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)