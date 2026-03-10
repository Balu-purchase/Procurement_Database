import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Safe initialization to prevent AttributeErrors
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "BOM"
if "bom_list" not in st.session_state:
    st.session_state.bom_list = []

# --- 2. LOGIN SYSTEM ---
if not st.session_state.auth:
    st.title("🏭 Factory Management Login")
    with st.container(border=True):
        uid = st.text_input("Username")
        upw = st.text_input("Password", type="password")
        if st.button("LOG IN", use_container_width=True):
            # Credentials for BOMTEAM, NONBOMTEAM, and HOD
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun()
            else:
                st.error("Invalid Username or Password.")
    st.stop()

# Role Setup
role = st.session_state.role
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 3. BOM TEAM VIEW ---
if role == "BOMTEAM":
    st.header("📦 BOM TEAM - Price Approval Entry")
    
    # Input Form
    with st.expander("➕ Click to Add New Row", expanded=True):
        with st.form("bom_entry_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            v_name = c1.text_input("
