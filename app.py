import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Procurement Audit Portal", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "hod_office": {"pass": "HOD789", "role": "HOD", "name": "Bixapathi", "desig": "Head of Department (HOD)"},
    "bom_team": {"pass": "BOM2026", "role": "BOM", "name": "BOM Team", "desig": "Executive"}
}

# 3. INITIALIZE SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# 4. PROFESSIONAL STYLING
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .audit-card { 
        background: white; padding: 25px; border-radius: 12px; 
        border-left: 10px solid #1e40af; box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        margin-bottom: 20px;
    }
    .sig-font { font-family: 'Brush Script MT', cursive; font-size: 28px; color: #1e40af; }
    h1 { text-align: center; color: #0f172a; font-weight: 800; border-bottom: 2px solid #1e40af; padding-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 5. ACCESS CONTROL GATEKEEPER
if not st.session_state.auth:
    st.sidebar.title("🔐 ACCESS CONTROL")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN", use_container_width=True):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.user_info = USER_DB[u_id]
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid ID or Password")
    
    # Show welcome screen only if not logged in
    st.markdown("<h1>🏭 WELCOME TO THE PROCUREMENT PORTAL</h1>", unsafe_allow_html=True)
    st.info("Please enter your credentials in the sidebar to view the Dashboard and Audit Logs.")
    st.stop() # THIS PREVENTS ANY FURTHER CODE FROM RUNNING

# --- EVERYTHING BELOW THIS LINE ONLY RUNS IF AUTH IS TRUE ---

# 6. NAVIGATION & LOGOUT
st.sidebar.success(f"User: {st.session_state.user_info.get('name')}")
menu = st.sidebar.radio("NAVIGATE", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.session_state.user_info = {}
    st.rerun()

# 7. DATA LOADING
@st.cache_data(ttl=30)
def load_data():
    url =
