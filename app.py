import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Audit Portal", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "hod_office": {
        "pass": "HOD789", 
        "role": "HOD", 
        "name": "Bixapathi", 
        "desig": "Head of Department (HOD)"
    },
    "bom_team": {
        "pass": "BOM2026", 
        "role": "BOM", 
        "name": "BOM Team", 
        "desig": "Executive"
    }
}

# 3. INITIALIZE SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u_info" not in st.session_state:
    st.session_state.u_info = {}

# 4. ACCESS CONTROL
if not st.session_state.auth:
    st.sidebar.title("🔐 LOGIN")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN"):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[u_id]
            st.rerun()
        else:
            st.sidebar.error("Invalid ID or Password")
    st.stop()

# 5. STYLING
st.markdown("""
<style>
    .audit-card { 
        background: white; padding: 20px; border-radius: 10px; 
        border-left: 8px solid #1e40af; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        margin-bottom: 15px;
    }
    .sig-font { font-family: 'Brush Script MT', cursive; font-size: 26px; color: #1e40af; }
    h1 { text-align: center; color: #1e40af; }
</style>
""", unsafe_allow_html=True)

# 6. DATA LOADING (UPDATED WITH GID 466678125)
@st.cache_data(ttl=10)
def load_data():
    SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    GID_SHEET = "466678125" 
    
    # URL Construction for CSV Export
    url = "https://docs.google.com/spreadsheets/d/" + SHEET_ID + "/export?format=csv&gid=" + GID_SHEET
    
    try:
        data = pd.read_csv(url)
        # Standardize column names: remove spaces and make UPPERCASE for matching
        data.columns = data.columns.str.strip().str.upper()
        return data
    except Exception as
