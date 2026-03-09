import streamlit as st
import pandas as pd
import time

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Purchase NonBOM Tracking", layout="wide")

# --- 2. SESSION MEMORY ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 3. LIVE DATABASE LINK ---
SID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
URL = f"https://docs.google.com/spreadsheets/d/{SID}/export?format=csv"

# --- 4. STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    h1, h2, h3, p, span, label, .stMetric { 
        color: white !important; 
        font-weight: bold !important;
        text-shadow: 2px 2px 5px black;
    }
    .stDataFrame { 
        background-color: rgba(0,0,0,0.8) !important; 
        border: 2px solid #38bdf8 !important; 
    }
    .summary-box {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #38bdf8;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ACCESS KEYS ---
KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

if not st.session_state.logged_in:
    # --- LOGIN SCREEN ---
    st.markdown("<h1>🔐 SECURITY ACCESS</h1>", unsafe_allow_html=True)
    role = st.selectbox("OPERATIONAL ROLE", list(KEYS.keys()))
    pwd = st.text_input("SECURITY PASSKEY", type="password")
    if st.button("AUTHORIZE"):
        if pwd == KEYS.get(role):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Passkey")
else:
    # --- AUTHORIZED DASHBOARD ---
    with st.sidebar:
        st.write("🛰️ SYSTEM LIVE")
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    try:
        # Load fresh Data
        df = pd.read_csv(URL)
        
        # --- NEW HEADING ---
        st.markdown("<h1 style='text-align: center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
        
        # --- SUMMARY TABLE SECTION ---
        st.markdown("### 📊 Summary Report (Plant-wise)")
        
        # Group data by Plant and sum the specific
