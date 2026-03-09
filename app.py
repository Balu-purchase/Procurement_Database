import streamlit as st
import pandas as pd
from datetime import datetime
import time

# 1. PAGE SETUP
st.set_page_config(page_title="SKYQUAD", layout="wide")

# 2. SESSION MEMORY (Prevents Logout)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 3. LIVE DATA LINK
# This links directly to your spreadsheet ID
SID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
URL = f"https://docs.google.com/spreadsheets/d/{SID}/export?format=csv"

# 4. HIGH-CONTRAST STYLE
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
        border: 2px solid #38bdf8; 
    }
    </style>
    """, unsafe_allow_html=True)

# 5. ACCESS KEYS
KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# 6. APP LOGIC
if not st.session_state.logged_in:
    # --- LOGIN SCREEN ---
    st.markdown("<h1>🔐 SKYQUAD SECURITY ACCESS</h1>", unsafe_allow_html=True)
    
    role = st.selectbox("OPERATIONAL ROLE", list(KEYS.keys()))
    pwd = st.text_input("SECURITY PASSKEY", type="password")
    
    if st.button("AUTHORIZE"):
        if pwd == KEYS.get(role):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Key")

else:
    # --- AUTHORIZED DASHBOARD ---
    # Refresh logic only runs here so you stay logged in
    
    with st.sidebar
