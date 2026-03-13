import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Persistent lists ensure data is kept during the session
if "master_data" not in st.session_state: 
    st.session_state.master_data = []

# App state management
if "auth" not in st.session_state: 
    st.session_state.auth = False
if "role" not in st.session_state: 
    st.session_state.role = None

# --- Helper Functions ---
def get_signature():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"SIGNED BY {st.session_state.role} @ {now}"

def style_status(val):
    val_upper = str(val).upper()
    # Approved Successfully - FULLY GREEN COLOR ENTIRE CELL WITH BOLD TEXT 
    if "SUCCESSFULLY APPROVED" in val_upper or "SIGNED BY" in val_upper or val_upper == "APPROVED": 
        return 'background-color: green; color: white; font-weight: bold'
    # PENDING - LIGHT ORENGE COLOUR ENTIRE CELL WITH BOLD TEXT
    elif "PENDING" in val_upper: 
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    # REJECTED - RED COLOUR ENITER CELL WITH BOLD TEXT 
    elif "REJECTED" in val_upper: 
        return 'background-color: red; color: white; font-weight: bold'
    return ''

# --- 2. LOGIN PAGE (Split Screen Design) ---
if not st.session_state.auth:
    login_col, img_col = st.columns([1, 2])
    
    with login_col:
        st.markdown("# 🏗️ Resolute \n### Procurement Portal")
        st.divider()
        uid = st.text_input("Username").strip().upper() 
        upw = st.text_input("Password", type="password")
        
        if st.button("ENTER SYSTEM", use_container_width=True):
            creds = {
                "BOMTEAM": "BOM123", 
                "NONBOMTEAM": "NONBOM123", 
                "HOD": "HOD789", 
                "GM_OFFICE": "GM2026"
            }
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun() 
            else: 
                st.error("Invalid Credentials.")
    
    with img_col:
        # High-
