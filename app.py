import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- 1. SETTINGS ---
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide")

# --- 2. LOGIN MEMORY (SESSION STATE) ---
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None

# --- 3. DATABASE LINK ---
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- 4. HIGH-VISIBILITY STYLE ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; }
    h1, h2, h3, p, span, label, .stMetric { 
        color: white !important; 
        font-weight: bold !important;
        text-shadow: 2px 2px 4px #000000;
    }
    .stDataFrame { background: rgba(0,0,0,0.5); border: 1px solid #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ACCESS KEYS ---
KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 6. MAIN LOGIC FLOW ---
if not st.session_state.auth:
    # --- LOGIN SCREEN ---
    st.markdown("<h1>🔐 SKYQUAD LOGIN</h1>", unsafe_allow_html=True)
    role_choice = st.selectbox("OPERATIONAL ROLE", list(KEYS.keys()))
    pwd_input = st.text_input("SECURITY PASSKEY", type="password")
    
    if st.button("AUTHORIZE"):
        if pwd_input == KEYS.get(role_choice):
            st.session_state.auth = True
            st.session_state.role = role_choice
            st.rerun()
        else:
            st.error("Invalid Key")
else:
    # --- AUTHORIZED DASHBOARD ---
    st.sidebar.markdown(f"### 👤 {st.session_state.role}")
    if st.sidebar.button("LOGOUT"):
        st.session_state.auth = False
        st.rerun()

    # THE DATA LOOP (Wrapped correctly in try/except)
    try:
        # Load fresh data from Google Sheet
        df = pd.read_csv(URL)
        
        st.markdown(f"<h1>🚀 {st.session_state.role} CENTER</h1>", unsafe_allow_html=True)
        
        # Dashboard Metrics
        c1, c2 = st.columns(2)
        c1.metric("Live Records", len(df))
        c2.metric("Last Sync", datetime.now().strftime("%
