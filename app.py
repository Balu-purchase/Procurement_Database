import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- 1. SETTINGS ---
st.set_page_config(page_title="SKYQUAD", layout="wide")

# --- 2. LOGIN MEMORY ---
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None

# --- 3. LIVE DATA ---
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- 4. STYLE ---
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

# --- 5. KEYS ---
KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 6. LOGIC ---
if not st.session_state.auth:
    # LOGIN BOX
    st.markdown("<h1>LOGIN TO SKYQUAD</h1>", unsafe_allow_html=True)
    sel_role = st.selectbox("OPERATIONAL ROLE", list(KEYS.keys()))
    sel_pwd = st.text_input("SECURITY PASSKEY", type="password")
    
    if st.button("AUTHORIZE"):
        if sel_pwd == KEYS.get(sel_role):
            st.session_state.auth = True
            st.session_state.role = sel_role
            st.rerun()
        else:
            st.error("Invalid Key")
else:
    # DASHBOARD
    st.sidebar.write(f"USER: {st.session_state.role}")
    if st.sidebar.button("LOGOUT"):
        st.session_state.auth = False
        st.rerun()

    try:
        # Load fresh data
        df = pd.read_csv(URL)
        st.markdown(f"<h1>{st.session_state.role} CENTER</h1>", unsafe_allow_html=True)
        
        # Simple Metrics
        c1, c2 = st.columns(2)
        c1.metric("Total Items", len(df))
        c2.metric("Sync Time", datetime.now().strftime("%H:%M:%S"))

        # Simple Search
