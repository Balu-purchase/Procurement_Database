import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide", initial_sidebar_state="expanded")

# --- 🔗 LIVE DATABASE LINK (DIRECT CSV EXPORT) ---
# This link is specifically formatted to pull data from your 'Untitled spreadsheet'
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
LIVE_DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=30)  # Data refreshes every 30 seconds
def load_live_data(url):
    try:
        # Pulling live data: S.NO, ID, DATE, PLANT, ITEM NAME, DEPT, etc.
        data = pd.read_csv(url)
        return data
    except Exception as e:
        return None

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #0369a1);
        background-size: 400% 400%;
        animation: skyquadGradient 15s ease infinite;
    }
    @keyframes skyquadGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .status-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #38bdf8;
        padding: 15px; border-radius: 10px; margin-bottom: 12px;
    }
    .status-label { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; }
    .status-value { color: #f8fafc; font-weight: 700; font-size: 1rem; }
    .pulse-icon {
        display: inline-block; width: 9px; height: 9px;
        background: #22c55e; border-radius: 50%; margin-right: 8px;
        box-shadow: 0 0 10px #22c55e; animation: pulse-animation 2s infinite;
    }
    @keyframes pulse-animation {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }
    </style>
    <div style="position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); opacity: 0.4; color: #38bdf8; font-weight: 800; letter-spacing: 4px; z-index: 9999; pointer-events: none;">NONBOM TEAM - SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- SECURITY GATE ---
ACCESS_KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
    st.session_state.role = None

if not st.session_state.secure_access:
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br><div style='background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);'><h1 style='text-align: center;'>🔐 SKYQUAD SHIELD</h1></div>", unsafe_allow_html=True)
        selected_role =
