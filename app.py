import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

if "master_data" not in st.session_state: 
    st.session_state.master_data = []
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
    if "SUCCESSFULLY APPROVED" in val_upper or "SIGNED BY" in val_upper: 
        return 'background-color: green; color: white; font-weight: bold'
    elif "PENDING" in val_upper: 
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    elif "REJECTED" in val_upper: 
        return 'background-color: red; color: white; font-weight: bold'
    return ''

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    login_col, img_col = st.columns([1, 2])
    with login_col:
        st.markdown("# 🏗️ Resolute \n### Procurement Portal")
        uid = st.text_input("Username", key="l_user").strip().upper() 
        upw = st.text_input("Password", type="password", key="l_pass")
        if st.button("ENTER SYSTEM", use_container_width=True):
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789", "GM_OFFICE": "GM2026"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun() 
            else: st.error("Invalid Credentials.")
    with img_col:
        st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1200", use_container_width=True)
    st.stop()

# --- 3. DASHBOARD ---
else:
    st.sidebar.title(f"👤 {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("NAVIGATE", ["PENDING APPROVALS", "AUDIT LOGS"])
    else:
        menu = "MAIN"

    st.title("PRICE APPROVALS FOR BOM ITEMS")
    
    if st.session_state.role in ["BOMTEAM", "NONBOMTEAM"]:
        st.header(f"🛠️ {st.session_state.role}: New Request")
        with st.form("entry_form", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns(4)
            p_proj, p_num, p_desc, p_qps = c1.text_input("PROJECT"), c2.text_input("PART NO"), c3.text_input("DESC"), c4.text_input("QPS")
            c5, c6, c7, c8 = st.columns(4)
            p_uom = c5.selectbox("UOM", ["Nos", "KG", "Mtr"])
            p_supp, p_price, p_rem = c6.text_input("SUPPLIER"), c7.text_
