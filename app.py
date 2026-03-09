import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. PAGE CONFIG (Must be first) ---
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide", initial_sidebar_state="expanded")

# --- 2. GOOGLE SHEETS CONFIG ---
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
LIVE_DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- 3. AUTO-REFRESH SCRIPT (30 SECONDS) ---
components.html(
    """
    <script>
    setTimeout(function(){
        window.parent.location.reload();
    }, 30000);
    </script>
    """,
    height=0,
)

# --- 4. DATA LOADING ---
@st.cache_data(ttl=20)
def load_live_data(url):
    try:
        return pd.read_csv(url)
    except Exception:
        return None

# --- 5. VISIBILITY & STYLE FIX ---
st.markdown("""
    <style>
    /* Animated Blue Background */
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
    
    /* Make all text BOLD and WHITE with a black shadow for visibility */
    h1, h2, h3, p, span, label, .stMetric, .stMarkdown {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 8px #000000 !important;
    }
    
    /* Darken the data table for readability */
    .stDataFrame {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 10px;
    }

    /* Sidebar cards */
    .status-card {
        background: rgba(0, 0, 0, 0.8);
        border-left: 5px solid #38bdf8;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 6. SESSION STATE ---
if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
if "role" not in st.session_state:
    st.session_state.role = None

ACCESS_KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 7. APP LOGIC ---
if not st.session_state.secure_access:
    # LOGIN SCREEN
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br><div style='background:rgba(0,0,0,0.8);padding:30px;border-radius:15px;border:2px solid #38bdf8;text-
