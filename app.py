import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Corporate Approval Portal", layout="wide")

# Prevent AttributeError by initializing keys
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "NONBOM"

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
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.stop()

# Safe access to role after login
role = st.session_state.role

# Sidebar
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.session_state.role = None
    st.rerun()

# --- 3. NONBOM TEAM LOGIN ---
if role == "NONBOMTEAM":
    st.header("📋 Non-BOM Daily Activity Log")
    with st.form("nonbom_entry", clear_on_submit=True):
        activity = st.text_area("Daily Activity / Purchase Requests")
        qty = st.number_input("Total Quantity", min_value=0)
        if st.form_submit_button("Submit to HOD"):
            st.session_state.non_bom_db.append({
                "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "Activity": activity,
                "Qty": qty,
                "HOD_Comment": "PENDING"
            })
            st.success("Activity submitted!")

# --- 4. BOM TEAM LOGIN ---
elif role == "BOMTEAM":
    st.header("💰 BOM Price Approval Request")
    with st.form("bom_entry", clear_on_submit=True):
        part = st.text_input("Part Number / Item Name")
        vendor = st.text_input("Vendor Name")
        price = st.text_input("Quoted Price")
        if st.form_submit_button("Request Price Approval"):
            st.session_state.bom_db.
