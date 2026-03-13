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
    if "SUCCESSFULLY APPROVED" in val_upper or "SIGNED BY" in val_upper or val_upper == "APPROVED": 
        return 'background-color: green; color: white; font-weight: bold'
    elif "PENDING" in val_upper: 
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    elif "REJECTED" in val_upper: 
        return 'background-color: red; color: white; font-weight: bold'
    return ''

# --- 2. LOGIC GATE: LOGIN VS DASHBOARD ---

if not st.session_state.auth:
    # This block runs ONLY when not logged in
    login_col, img_col = st.columns([1, 2])
    
    with login_col:
        st.markdown("# 🏗️ Resolute \n### Procurement Portal")
        st.divider()
        uid = st.text_input("Username", key="login_user").strip().upper() 
        upw = st.text_input("Password", type="password", key="login_pass")
        
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
        st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1200", 
                 caption="Resolute Factory Management System", use_container_width=True)

else:
    # This block runs ONLY after successful login
    st.sidebar.title(f"👤 {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.session_state.role = None
        st.rerun()

    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("NAVIGATE", ["PENDING APPROVALS", "AUDIT LOGS"])
    else:
        menu = "MAIN"

    st.title("PRICE APPROVALS FOR BOM ITEMS")
    st.divider()

    # --- 🔵 BOM & NON-BOM TEAM MODULE ---
    if st.session_state.role in ["BOMTEAM", "NONBOMTEAM"]:
        st.header(f"🛠️ {st.session_state.role}: New Price Request")
        with st.form("entry_form", clear_on_submit=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            p_proj = r1c1.text_input("PROJECT")
            p_num = r1c2.text_input("PART NUMBER")
            p_desc = r1c3.text_input("DESCRIPTION")
            p_qps = r1c4.text_input("QPS")
            
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            p_uom = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Sets"])
            p_supp = r2c2.text_input("SUPPLIER NAME")
            p_price = r2c3.text_input("PRICE")
            p_rem = r2c4.text_input("REMARKS")
            
            if st.form_submit_button("SUBMIT FOR APPROVAL"):
                st.session_state.master_data.append({
                    "VENDOR NAME": p_supp, "PART NUMBER": p_num, "MATERIAL DESCRIPTION": p_desc, 
                    "PRICE": p_price, "QPS": p_qps, "UOM": p_uom, "REMARKS": p_rem,
                    "HOD_SIGN":
