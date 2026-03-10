import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION (Retains previous data) ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Ensure all data lists exist in the session so data is not lost
if "master_data" not in st.session_state: st.session_state.master_data = []
if "daily_tracker" not in st.session_state: st.session_state.daily_tracker = []
if "advance_payments" not in st.session_state: st.session_state.advance_payments = []
if "mis_data" not in st.session_state: st.session_state.mis_data = []

# App authentication state
if "auth" not in st.session_state: st.session_state.auth = False
if "role" not in st.session_state: st.session_state.role = None

# --- Helper Functions for Auditor Proof ---
def get_digital_signature():
    """Captures Name and Timestamp for audit logs."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"APPROVED BY {st.session_state.role} @ {now}"

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
            # Credentials for BOM, NON-BOM, HOD, and GM
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

    # Sidebar Navigation for HOD/GM
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
        
        st.subheader("📋 Submission Status Table")
        if st.session_state.master_data:
            st.dataframe(pd.DataFrame(st.session_state.master_data).style.applymap(style_status, subset=['STATUS']), use_container_width=True)

    # --- 🟢 NON-BOM TEAM MODULE (Fixed: Shows Previous Data) ---
    elif st.session_state.role == "NONBOMTEAM":
        st.header("📦 Non-BOM Activity Management")
        t1, t2, t3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS TRACKER"])
        
        with t1:
            with st.form("dt_form"):
                c1, c2, c3, c4 = st.columns(4)
                d_d, d_p = c1.date_input("DATE"), c2.text_input("PLANT")
                d_r, d_o = c3.number_input("PR RECEIPTS", min_value=0), c4.number_input("PO DONE", min_value=0)
                if st.form_submit_button("SUBMIT"):
                    st.session_state.daily_tracker.append({"S.NO": len(st.session_state.daily_tracker)+1, "DATE": str(d_d), "PLANT": d_p, "PR RECEIPTS": d_r, "PO DONE": d_o, "BALANCE PR'S": d_r - d_o, "HOD COMMENTS": ""})
                    st.rerun()
            st.write("### Previous Daily Records")
            if st.session_state.daily_tracker:
                st.table(pd.DataFrame(st.session_state.daily_tracker))

        with t2:
            st.subheader("Advance Payment Status")
            if st.session_state.advance_payments:
                df_adv = pd.DataFrame(st.session_state.advance_payments)
                edited = st.data_editor(df_adv, use_container_width=True, key="adv_edit")
                if st.button("SAVE CHANGES"): st.session_state.advance_payments = edited.to_dict('records'); st.rerun()
            
            with st.expander("Add New Advance Request"):
                with st.form("adv_new"):
                    c1, v_n = st.columns(2); s_d, v_name = c1.date_input("SUBMIT DATE"), v_n.text_input("VENDOR")
                    if st.form_submit_button("SUBMIT NEW REQUEST"):
                        st.session_state.advance_payments.append({"SUBMIT DATE": str(s_d), "VENDOR NAME": v_name, "PAYMENT STATUS": "PENDING"})
                        st.rerun()

    # --- 🟠 HOD & GM SEQUENTIAL APPROVAL (Waterfall) ---
    elif menu == "PENDING APPROVALS":
        st.header(f"🖊️ {st.session_state.role} Approval Workspace")
        found = False
        for i, row in enumerate(st.session_state.master_data):
            # Waterfall: GM only sees after HOD signs
            show = (st.session_state.role ==
