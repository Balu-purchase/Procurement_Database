import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="SKYQUAD | SECURE PORTAL", layout="wide")

# --- CUSTOM CSS (Animated Background & Restricted UI) ---
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
        opacity: 0.25;
        font-size: 1rem;
        color: #38bdf8;
        font-weight: 800;
        letter-spacing: 5px;
        z-index: 9999;
        pointer-events: none;
        text-transform: uppercase;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 5px 15px;
        border-radius: 50px;
    }
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3, p { color: #f8fafc !important; }
    </style>
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- ACCESS CONTROL ---
if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
    st.session_state.role = None

# --- LOGIN GATE ---
if not st.session_state.secure_access:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
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
                st.error("Invalid Passkey")

# --- SECURE DASHBOARD AREA ---
else:
    st.sidebar.title("System Status")
    st.sidebar.info(f"Access Level: {st.session_state.role}")
    if st.sidebar.button("TERMINATE SESSION"):
        st.session_state.secure_access = False
        st.session_state.role = None
        st.rerun()

    # --- GM MANAGEMENT VIEW ---
    if st.session_state.role == "GM Management":
        st.markdown("<h1 style='text-align: center;'>📊 GM MASTER COMMAND CENTER</h1>", unsafe_allow_html=True)
        
        col_bom, col_nbom = st.columns(2)
        
        with col_bom:
            st.subheader("📦 BOM Team Stream")
            file_bom = st.file_uploader("Upload BOM CSV", type=["csv"], key="bom_uploader")
            if file_bom:
                df_bom = pd.
