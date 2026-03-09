import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide")

# --- 2. THE "MEMORY" (SESSION STATE) ---
# This is the most important part. It keeps you logged in during refreshes.
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# --- 3. DATABASE LINK ---
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
LIVE_DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- 4. STYLE & VISIBILITY ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #0369a1);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    /* High Visibility Text */
    h1, h2, h3, p, span, label, .stMetric {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 8px #000000 !important;
    }
    /* Dark Table for Readability */
    .stDataFrame {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ACCESS KEYS ---
ACCESS_KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 6. MAIN LOGIC FLOW ---
if not st.session_state.authenticated:
    # --- LOGIN INTERFACE ---
    st.markdown("<h1 style='text-align:center;'>🔐 SKYQUAD SHIELD</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div style='background:rgba(0,0,0,0.5); padding:20px; border-radius:10px;'>", unsafe_allow_html=True)
        role = st.selectbox("OPERATIONAL ROLE", list(ACCESS_KEYS.keys()))
        pwd = st.text_input("SECURITY PASSKEY", type="password")
        
        if st.button("AUTHORIZE ACCESS", use_container_width=True):
            if pwd == ACCESS_KEYS.get(role):
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun() # Refresh to enter dashboard
            else:
                st.error("Invalid Passkey")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- AUTHORIZED DASHBOARD ---
    # This section only runs if authenticated is True
    
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user_role}")
        st.write(f"**Sync Time:** {datetime.now().strftime('%H:%M:%S')}")
        if st.button("LOGOUT"):
            st.session_state.authenticated = False
            st.rerun()

    # LOAD DATA
    try:
        # We don't use cache here so it pulls fresh data every time the page reloads
        df = pd.read_csv(LIVE_DATA_URL)
        
        st.markdown(f"<h1>🚀 {st.session_state.user_role} Command Center</h1>", unsafe_allow_html=True)
        
        # Dashboard Metrics
        m1, m2 = st.columns(2)
        m1.metric("Total Line Items", len(df))
        m2.metric("System Status", "LIVE SYNC")

        # Search Bar
        search = st.text_input("🔍
