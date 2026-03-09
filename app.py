import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Procurement Audit System", layout="wide")

# 2. USER DATABASE (Recognized Users & Signatures)
USER_DB = {
    "hod_office": {
        "pass": "HOD789", 
        "role": "HOD", 
        "name": "Bixapathi", 
        "desig": "Head of Department (HOD)"
    },
    "bom_team": {"pass": "BOM2026", "role": "BOM", "name": "BOM Executive", "desig": "Data Entry"}
}

# 3. STYLING (Clean Industrial Management Look)
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .report-card {
        background-color: white; padding: 25px; border-radius: 12px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px; border-left: 8px solid #1e40af;
    }
    .sig-style { font-family: 'Brush Script MT', cursive; font-size: 28px; color: #1e40af; }
    .status-approved { color: #10b981; font-weight: bold; font-size: 1.1rem; }
    h1 { color: #0f172a; text-align: center; font-weight: 800; border-bottom: 3px solid #1e40af; display: inline-block; width: 100%; padding-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# 4. AUTHENTICATION
if "auth" not in st.session_state:
    st.session_state.auth = False

st.sidebar.title("🔐 PORTAL ACCESS")
if not st.session_state.auth:
    u = st.sidebar.text_input("USER ID")
    p = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("LOG IN", use_container_width=True):
        if u in USER_DB and USER_DB[u]["pass"] == p:
            st.session_state.auth = True
            st.session_state.user_data = USER_DB[u]
            st.rerun()
    st.stop()

# 5. NAVIGATION (Icons in Sidebar)
st.sidebar.divider()
menu = st.sidebar.radio("NAVIGATE SYSTEM", ["🏠 DASHBOARD", "🏛️ AUDIT & APPROVAL LOG"])

if st.sidebar.button("LOG OUT", use_container_width=True):
    st.session_state.auth = False
    st.rerun()

# --- FAIL-SAFE DATA LOADING ---
def load_bom_data():
    # IMPORTANT: Ensure your Google Sheet is set to "Anyone with the link can view"
    # Replace '2061093150' with the GID of your BOM Team Tab
    url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv&gid=2061093150"
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
        st.error(f"⚠️ Connection Error: Please ensure the Google Sheet is 'Public' and the Link is correct.")
        return pd.
