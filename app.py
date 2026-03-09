import streamlit as st
import pandas as pd

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SKYQUAD | SECURE PORTAL", layout="wide")

# --- 2. VISUALS & WATERMARK ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #000000);
        background-size: 400% 400%;
        animation: skyquadGradient 20s ease infinite;
    }
    @keyframes skyquadGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .watermark {
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0.4;
        font-size: 1.2rem;
        color: #38bdf8;
        font-weight: 800;
        letter-spacing: 5px;
        z-index: 9999;
        pointer-events: none;
        text-transform: uppercase;
        border: 2px solid rgba(56, 189, 248, 0.3);
        padding: 8px 20px;
        border-radius: 50px;
        background: rgba(0,0,0,0.3);
    }
    h1, h2, h3, p, label { color: white !important; font-family: 'sans-serif'; }
    .login-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    </style>
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- 3. SESSION INITIALIZATION ---
if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
if "role" not in st.session_state:
    st.session_state.role = None

# --- 4. THE LOGIN GATE ---
if not st.session_state.secure_access:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.5, 1])
    
    with col_login:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🔐 SKYQUAD SHIELD</h1>", unsafe_allow_html=True)
        
        role_select = st.selectbox("Identify Your Team", ["BOM Team", "Non-BOM Team", "GM Management"])
        pwd_input = st.text_input("Security Passkey", type="password")
        
        if st.button("VERIFY IDENTITY", use_container_width=True):
            creds = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}
            if pwd_input == creds.get(role_select):
                st.session_state.secure_access = True
                st.session_state.role = role_select
                st.rerun()
            else:
                st.error("❌ Access Denied: Invalid Passkey")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. THE MAIN DASHBOARD ---
else:
    # Sidebar
    st.sidebar.title("Skyquad System")
    st.sidebar
