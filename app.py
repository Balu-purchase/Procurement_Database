import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide", initial_sidebar_state="expanded")

# --- 2. GOOGLE SHEETS CONFIG ---
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
LIVE_DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- 3. AUTO-REFRESH LOGIC (Every 30 Seconds) ---
# This JavaScript snippet forces the browser to refresh without user input
components.html(
    """
    <script>
    window.parent.document.querySelector('section.main').scrollTo(0, 0);
    setTimeout(function(){
        window.parent.location.reload();
    }, 30000); // 30000ms = 30 seconds
    </script>
    """,
    height=0,
)

# --- 4. DATA LOADING ---
@st.cache_data(ttl=20) # Cache expires slightly before the auto-refresh
def load_live_data(url):
    try:
        return pd.read_csv(url)
    except Exception:
        return None

# --- 5. ENHANCED UI STYLING (High Visibility) ---
st.markdown("""
    <style>
    /* Animated Background */
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
    
    /* High Contrast Text & Containers */
    h1, h2, h3, p, span, label {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    /* Dataframe Visibility Fix */
    .stDataFrame {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #38bdf8;
    }

    /* Status Cards */
    .status-card {
        background: rgba(0, 0, 0, 0.6);
        border-left: 5px solid #38bdf8;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow:
