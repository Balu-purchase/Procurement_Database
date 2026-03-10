import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Corporate Approval Portal", layout="wide")

# Prevent AttributeError: Initialize session keys if they don't exist
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "NONBOM"

# Website-only database storage
if "bom_db" not in st.session_state:
    st.session_state.bom_db = []
if "non_bom_db" not in st.session_state:
    st.session_state.non_bom_db = []

# --- 2. LOGIN SYSTEM ---
if not st.session_state.auth:
    st.title("🏭 Factory Management Login")
    with st.container(border=True):
        uid = st.text_input("Username")
        upw = st.text_input("Password", type="password")
        if st.button("LOG IN", use_container_width=True):
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun()
            else:
                st.error("Invalid Username or Password.")
    st.stop()

# Safe access to role after login check
role = st.session_state.role

# Sidebar Logout
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.session_state.role = None
    st.rerun()

# --- 3. NON-BOM TEAM INTERFACE ---
if role == "NONBOMTEAM":
    st.header("📋 Non-BOM Daily Activity Log")
    with st.form("nonbom_form", clear_on_submit=True):
        activity = st.text_area("Daily Activity / Purchase Requested")
        qty = st.number_input("Total Quantity", min_value=0)
        if st.form_submit_button("Submit to HOD"):
            entry = {
                "Date": datetime.now().strftime("%d-%m
