import streamlit as st

# ================= AUTH CSS =================
def load_auth_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=DM+Sans:wght@300;400;500;600&display=swap');

    .stApp{
        background: radial-gradient(circle at top left,#102117,#060d07 60%);
        color:#ddeae0;
        font-family:'DM Sans',sans-serif;
    }

    #MainMenu, footer{visibility:hidden;}

    header{
        background:transparent !important;
    }

    .block-container{
        max-width:100% !important;
        padding:0 !important;
    }

    .auth-logo{
        font-size:42px;
        text-align:center;
        margin-bottom:4px;
    }

    .auth-appname{
        text-align:center;
        color:#7aab8a;
        letter-spacing:.22em;
        font-size:13px;
        margin-bottom:18px;
    }

    .auth-heading{
        text-align:center;
        font-size:28px;
        color:#f0ead8;
        font-family:'Lora',serif;
        margin-bottom:6px;
    }

    .auth-subheading{
        text-align:center;
        color:#6a8f74;
        font-size:14px;
        line-height:1.7;
        margin-bottom:24px;
    }

    .stTextInput input{
        background:#111c14 !important;
        color:#fff !important;
        border:1px solid rgba(122,171,138,.18) !important;
        border-radius:12px !important;
    }

    .stButton button{
        width:100%;
        border:none !important;
        border-radius:12px !important;
        background:linear-gradient(135deg,#7aab8a,#4d8a62) !important;
        color:#071009 !important;
        font-weight:700 !important;
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
        background:#ffffff !important;
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
        background:#ffffff !important;
        border-bottom:1px solid #ececec;
        height:3rem !important;
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
        background:#f7f7f7 !important;
        border-right:1px solid #e6e6e6;
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
    }

    section[data-testid="stSidebar"] .stButton button{
        width:100%;
        background:#fff !important;
        color:#111 !important;
        border:1px solid #e5e5e5 !important;
        border-radius:12px !important;
        padding:10px 14px !important;
        margin-bottom:8px !important;
        text-align:left !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover{
        background:#f1f1f1 !important;
    }

    .account-email{
        background:#fff;
        border:1px solid #e5e5e5;
        border-radius:12px;
        padding:12px;
        font-size:13px;
        color:#111;
        margin-top:12px;
        margin-bottom:10px;
        word-break:break-word;
    }

    /* HEADER */
    .milo-header{
        margin-top:3rem;
        padding:18px 28px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        border-bottom:1px solid #ececec;
        background:#fff;
    }

    .milo-header-left{
        display:flex;
        align-items:center;
        gap:12px;
    }

    .milo-header-logo{
        font-size:30px;
        font-weight:700;
        color:#111;
    }

    .milo-header-badge{
        background:#f2f2f2;
        color:#444;
        font-size:11px;
        padding:4px 10px;
        border-radius:999px;
        font-weight:700;
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
    }

    .empty-state-icon{
        font-size:52px;
    }

    .empty-state-title{
        font-size:28px;
        font-weight:700;
        margin-top:10px;
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
    }

    /* user right */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){
        justify-content:flex-end;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown{
        background:#111;
        color:#fff;
        padding:14px 16px;
        border-radius:18px 18px 6px 18px;
        max-width:75%;
        margin-left:auto;
    }

    /* bot left */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown{
        background:#f4f4f4;
        color:#111;
        padding:14px 16px;
        border-radius:18px 18px 18px 6px;
        max-width:75%;
    }

    /* INPUT */
    [data-testid="stBottom"],
    [data-testid="stBottom"]>div{
        background:#fff !important;
        border-top:1px solid #ececec;
    }

    [data-testid="stChatInput"]{
        max-width:900px;
        margin:auto;
        padding:14px 18px !important;
    }

    [data-testid="stChatInput"] textarea{
        background:#f7f7f7 !important;
        color:#111 !important;
        border:1px solid #ddd !important;
        border-radius:18px !important;
        min-height:56px !important;
    }

    [data-testid="stChatInput"] button{
        background:#111 !important;
        color:#fff !important;
        border:none !important;
        border-radius:12px !important;
        width:44px !important;
        height:44px !important;
    }
    </style>
    """, unsafe_allow_html=True)