import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- 1. SETTINGS ---
st.set_page_config(page_title="SKYQUAD", layout="wide")

# --- 2. LOGIN MEMORY ---
if "auth" not in st.session_state:
    st.session_state.auth = False

# --- 3. DATABASE LINK ---
# Direct link to your spreadsheet
SID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
URL = f"https://docs.google.com/spreadsheets/d/{SID}/export?format=csv"

# --- 4. STYLE ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; }
    h1, h2, h3, p, span, label, .stMetric { 
        color: white !important; 
        font-weight: bold !important;
    }
    .stDataFrame { background: rgba(0,0,0,0.5); border: 1px solid #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. KEYS ---
KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 6. MAIN LOGIC ---
if not st.session_state.auth:
    # --- LOGIN SCREEN ---
    st.markdown("<h1>🔐 SKYQUAD LOGIN</h1>", unsafe_allow_html=True)
    role_choice = st.selectbox("ROLE", list(KEYS.keys()))
    pwd_input = st.text_input("PASSWORD", type="password")
    
    if st.button("AUTHORIZE"):
        if pwd_input == KEYS.get(role_choice):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid Key")
else:
    # --- DASHBOARD ---
    if st.sidebar.button("LOGOUT"):
        st.session_state.auth = False
        st.rerun()

    try:
        # Load fresh data
        df = pd.read_csv(URL)
        
        st.markdown("<h1>🚀 SKYQUAD COMMAND CENTER</h1>", unsafe_allow_html=True)
        
        # Metrics
        c1, c2 = st.columns(2)
        c1.metric("Total Records", len(df))
        
        # Simplified time string to prevent syntax errors
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        c2.metric
