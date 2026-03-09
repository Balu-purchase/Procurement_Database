import streamlit as st
import pandas as pd
from datetime import datetime
import time

# 1. INITIAL CONFIG
st.set_page_config(page_title="SKYQUAD", layout="wide")

# 2. SESSION MEMORY (Prevents Logout on Refresh)
if "auth_status" not in st.session_state:
    st.session_state.auth_status = False

# 3. GOOGLE SHEETS LINK
# Your specific Sheet ID
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 4. STYLING (High Contrast for Visibility)
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    h1, h2, h3, p, span, label, .stMetric { 
        color: #ffffff !important; 
        font-weight: bold !important;
        text-shadow: 2px 2px 4px #000000;
    }
    .stDataFrame { 
        background-color: rgba(0,0,0,0.6); 
        border: 1px solid #38bdf8; 
    }
    </style>
    """, unsafe_allow_html=True)

# 5. ACCESS KEYS
USER_KEYS = {
    "BOM Team": "BOM2026",
    "Non-BOM Team": "NBOM2026",
    "GM Management": "GM789"
}

# 6. APP LOGIC
if not st.session_state.auth_status:
    # --- LOGIN SCREEN ---
    st.markdown("<h1>🔐 SKYQUAD LOGIN</h1>", unsafe_allow_html=True)
    
    role = st.selectbox("OPERATIONAL ROLE", list(USER_KEYS.keys()))
    pwd = st.text_input("SECURITY PASSKEY", type="password")
    
    if st.button("AUTHORIZE ACCESS"):
        if pwd == USER_KEYS.get(role):
            st.session_state.auth_status = True
            st.rerun()
        else:
            st.error("Invalid Passkey")

else:
    # --- AUTHORIZED DASHBOARD ---
    # Refresh logic only runs here to prevent kicking user to login
    
    with st.sidebar:
        st.markdown("### SYSTEM STATUS")
        st.write("🟢 LIVE SYNC ACTIVE")
        if st.button("LOGOUT / RESET"):
            st.session_state.auth_status = False
            st.rerun()

    # THE DATA BLOCK (Correctly aligned try/except)
    try:
        # Pull fresh data from Google Sheets
        df = pd.read_csv(SHEET_URL)
        
        st.markdown("<h1>🚀 SKYQUAD COMMAND CENTER</h1>", unsafe_allow_html=True)
        
        # Display Metrics
        col1, col2 = st.columns(2)
        col1.metric("Total Records", len(df))
        
        # Create Time String separately to avoid syntax errors
        current_time = datetime.now().strftime("%H:%M
