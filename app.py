import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Persistent data storage using session_state
if "master_data" not in st.session_state: st.session_state.master_data = []

# App state
if "auth" not in st.session_state: st.session_state.auth = False
if "role" not in st.session_state: st.session_state.role = None

# --- Helper Functions ---
def get_signature():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"SIGNED BY {st.session_state.role} @ {now}"

def style_status(val):
    val_upper = str(val).upper()
    # FULL GREEN COLOR ENTIRE CELL WITH BOLD TEXT
    if "SUCCESSFULLY APPROVED" in val_upper or "SIGNED BY" in val_upper or val_upper == "APPROVED":
        return 'background-color: green; color: white; font-weight: bold'
    # LIGHT ORANGE COLOUR ENTIRE CELL WITH BOLD TEXT
    elif "PENDING" in val_upper:
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    # RED COLOUR ENTIRE CELL WITH BOLD TEXT
    elif "REJECTED" in val_upper:
        return 'background-color: red; color: white; font-weight: bold'
    return ''

# --- 2. LOGIN PAGE (Split Screen) ---
if not st.session_state.auth:
    login_col, img_col = st.columns([1, 2])
    
    with login_col:
        st.markdown("# 🏗️ Procurement \n### Approval Portal")
        st.divider()
        uid = st.text_input("Username").strip().upper() 
        upw = st.text_input("Password", type="password")
        if st.button("ENTER SYSTEM", use_container_width=True):
            creds = {
                "BOMTEAM": "BOM123", 
                "NONBOMTEAM": "NONBOM123", 
                "HOD": "HOD789", 
                "GM_OFFICE": "GM
