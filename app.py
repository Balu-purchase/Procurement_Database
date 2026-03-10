import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Corporate Approval Portal", layout="wide")

# This prevents the AttributeError by ensuring keys exist on startup
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "NONBOM" # Default view for HOD

# Internal Databases (Website-only storage)
if "bom_db" not in st.session_state:
    st.session_state.bom_db = []
if "non_bom_db" not in st.session_state:
    st.session_state.non_bom_db = []

# --- 2. LOGIN INTERFACE ---
if not st.session_state.auth:
    st.title("🏭 Factory Management Portal")
    with st.container(border=True):
        uid = st.text_input("Username")
        upw = st.text_input("Password", type="password")
        if st.button("LOG IN", use_container_width=True):
            # Login Credentials
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    st.stop()

# --- 3. SESSION VARIABLES ---
role = st.session_state.role

# Sidebar Navigation
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.session_state.role = None
    st.rerun()

# --- 4. NONBOM TEAM: ACTIVITY ENTRY ---
if role == "NONBOMTEAM":
    st.header("📋 Non-BOM Daily Activity Log")
    with st.form("nonbom_entry
