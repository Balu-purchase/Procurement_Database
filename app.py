import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Use lists for storage to avoid Pandas concat errors
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "NONBOM"
if "bom_list" not in st.session_state:
    st.session_state.bom_list = [] # Storing as a list is safer than an empty DF
if "nonbom_list" not in st.session_state:
    st.session_state.nonbom_list = []

# --- 2. LOGIN ---
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

role = st.session_state.role
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 3. BOM TEAM VIEW ---
if role == "BOMTEAM":
    st.header("📦 BOM TEAM - Data Entry")
    
    with st.expander("➕ Add New Row", expanded=True):
        with st.form("bom_entry_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            vendor = c1.text_input("VENDOR NAME")
            part = c2.text_input("PART NUMBER")
            price = c3.text_input("PRICE")
            bom_val = st.text_input("BOM")
            
            if st.form_submit_button("Add to Table"):
                new_entry = {
                    "S.NO": len(st.session_state.bom_list) + 1,
                    "VENDOR NAME": vendor,
                    "PART NUMBER": part,
                    "PRICE": price,
                    "BOM": bom_val,
                    "HOD APPROVAL": "",
                    "GM APPROVAL": ""
                }
                st.session_state.bom_list.append(new_entry)
                st.success("Row added!")
                st.rerun()

    st.divider()
    st.subheader("Current BOM Table")
    if st.session_
