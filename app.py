import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Safe initialization of session state
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "BOM" # Default view
if "bom_list" not in st.session_state:
    st.session_state.bom_list = []
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

# Role-based Navigation
role = st.session_state.role
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 3. BOM TEAM VIEW ---
if role == "BOMTEAM":
    st.header("📦 BOM TEAM - Price Approval Entry")
    
    # Form to add data manually
    with st.expander("➕ Add New Entry", expanded=True):
        with st.form("bom_input_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            v_name = c1.text_input("VENDOR NAME")
            p_num = c2.text_input("PART NUMBER")
            
            c3, c4 = st.columns(2)
            price = c3.text_input("PRICE")
            bom_val = c4.text_input("BOM")
            
            if st.form_submit_button("Add to Table"):
                new_entry = {
                    "S.NO": len(st.session_state.bom_list) + 1,
                    "VENDOR NAME": v_name,
                    "PART NUMBER": p_num,
                    "PRICE": price,
                    "BOM": bom_val,
                    "HOD APPROVAL": "", # Empty for HOD to fill
                    "GM APPROVAL": ""   # Empty for GM to fill
                }
                st.session_state.bom_list.append(new
