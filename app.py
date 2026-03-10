import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Persistent lists ensure previous data is not lost
if "master_data" not in st.session_state: st.session_state.master_data = []
if "daily_tracker" not in st.session_state: st.session_state.daily_tracker = []
if "advance_payments" not in st.session_state: st.session_state.advance_payments = []
if "mis_data" not in st.session_state: st.session_state.mis_data = []

# App state
if "auth" not in st.session_state: st.session_state.auth = False
if "role" not in st.session_state: st.session_state.role = None

# --- Helper Functions ---
def get_signature():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"SIGNED BY {st.session_state.role} @ {now}"

def style_status(val):
    if val == "SUCCESSFULLY APPROVED": return 'background-color: #d4edda; color: #155724; font-weight: bold'
    if "PENDING AT GM" in val: return 'background-color: #cce5ff; color: #004085;'
    if "REJECTED" in val: return 'background-color: #f8d7da; color: #721c24;'
    return 'background-color: #fff3cd; color: #856404;'

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        st.markdown("<h2 style='text-align: center;'>PRICE APPROVALS FOR BOM ITEMS</h2>", unsafe_allow_html=True)
        uid = st.text_input("Username").strip().upper() 
        upw = st.text_input("Password", type="password")
        if st.button("ENTER SYSTEM", use_container_width=True):
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789", "GM_OFFICE": "GM2026"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun() 
            else: st.error("Invalid Credentials.")

# --- 3. DASHBOARD PAGE ---
else:
    st.sidebar.title(f"👤 {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("NAVIGATE", ["PENDING APPROVALS", "NON-BOM REVIEW", "AUDIT LOGS"])
    else:
        menu = "MAIN"

    st.title("PRICE APPROVALS FOR BOM ITEMS")
    st.divider()

    # --- 🔵 BOM TEAM MODULE ---
    if st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team: New Price Request")
        with st.form("bom_entry", clear_on_submit=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            p_proj, p_num, p_desc, p_qps = r1c1.text_input("PROJECT"), r1c2.text_input("PART NUMBER"), r1c3.text_input("DESCRIPTION"), r1c4.text_input("QPS")
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            p_uom, p_supp, p_price, p_rem = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Ltr"]), r2c2.text_input("SUPPLIER NAME"), r2c3.text_input("PRICE"), r2c4.text_input("REMARKS")
            if st.form_submit_button("SUBMIT FOR APPROVAL"):
                st.session_state.master_data.append({
                    "VENDOR NAME": p_supp, "PART NUMBER": p_num, "MATERIAL DESCRIPTION": p_desc, 
                    "PRICE": p_price, "QPS": p_qps, "UOM": p_uom, "REMARKS": p_rem,
                    "HOD_SIGN": "", "GM_SIGN": "", "STATUS": "PENDING AT HOD"
                })
                st.rerun()
        
        st.subheader("📋 Submission Status")
        if st.session_state.master_data:
            df_bom = pd.DataFrame(st.session_state.master_data)
            st.dataframe(df_bom.style.applymap(style_status, subset=['STATUS']), use_container_width=True)

    # --- 🟠 HOD & GM APPROVAL (WATERFALL LOGIC) ---
    elif menu == "PENDING APPROVALS":
        st.header(f"🖊️ {st.session_state.role} Approval Queue")
        has_pending = False
        for i, row in enumerate(st.session_state.master_data):
            # FIXED SYNTAX ERROR HERE
            show = (st.session_state.role == "HOD" and row["STATUS"] == "PENDING AT HOD") or (st.session_state.role == "GM_OFFICE" and row["STATUS"] == "PENDING AT GM")
            
            if show:
                has_pending = True
                with st.container(border=True):
                    st.write(f"**VENDOR:** {row['VENDOR NAME']} | **PART:** {row['PART NUMBER']} | **PRICE:** {row['PRICE']}")
                    st.write(f"**QPS:** {row['QPS']} | **REMARKS:** {row['REMARKS']}")
                    c1, c2 = st.columns(2)
                    if c1.button(f"✅ DIGITALLY SIGN AS {st.session_state.role}", key=f"s_{i
