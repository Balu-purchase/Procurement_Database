import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Persistent lists for all modules
if "master_data" not in st.session_state: st.session_state.master_data = []
if "daily_tracker" not in st.session_state: st.session_state.daily_tracker = []
if "advance_payments" not in st.session_state: st.session_state.advance_payments = []
if "mis_data" not in st.session_state: st.session_state.mis_data = []

# App state
if "auth" not in st.session_state: st.session_state.auth = False
if "role" not in st.session_state: st.session_state.role = None
if "nb_choice" not in st.session_state: st.session_state.nb_choice = "DAILY"

# --- Helper Functions for Styling ---
def style_status(val):
    if val in ["APPROVED", "CLOSED", "DONE"]: return 'background-color: green; color: white; font-weight: bold'
    if val in ["REJECTED", "PENDING"]: return 'background-color: red; color: white; font-weight: bold'
    if val == "OPEN": return 'background-color: orange; color: black; font-weight: bold'
    return ''

def apply_payment_colors(val):
    if val in ["DONE", "RECEIVED", "ACCOUNTED"]: return 'background-color: green; color: white'
    elif val == "PENDING": return 'background-color: yellow; color: black'
    return ''

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        st.markdown("<h2 style='text-align: center;'>SYSTEM LOGIN</h2>", unsafe_allow_html=True)
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

    st.title("Factory Procurement Dashboard")
    st.divider()

    # --- 🔵 BOM TEAM MODULE (FULLY RESTORED) ---
    if st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team: Manual Entry")
        with st.container(border=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            p_proj = r1c1.text_input("PROJECT")
            p_num = r1c2.text_input("PART NUMBER")
            p_desc = r1c3.text_input("DESCRIPTION")
            p_qps = r1c4.text_input("QPS")
            
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            p_uom = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Ltr"])
            p_supp = r2c2.text_input("SUPPLIER NAME")
            p_price = r2c3.text_input("PRICE")
            p_opt = r2c4.text_input("OPTIONAL SUPPLIER")
            
            if st.button("SUBMIT BOM REQUEST", type="primary"):
                st.session_state.master_data.append({
                    "PROJECT": p_proj, "PARTNUMBER": p_num, "DESCRIPTION": p_desc, 
                    "QPS": p_qps, "UOM": p_uom, "SUPPLIER": p_supp, "PRICE": p_price, 
                    "OPT_SUPP": p_opt, "HOD APPROVAL": "", "GM APPROVAL": "", "STATUS": "PENDING"
                })
                st.success("BOM Entry Submitted Successfully!")
                st.rerun()
        
        st.subheader("📋 My Submitted BOM Requests")
        if st.session_state.master_data:
            df_bom = pd.DataFrame(st.session_state.master_data)
            st.dataframe(df_bom.style.applymap(style_status, subset=['STATUS']), use_container_width=True)

    # --- 🟢 NON-BOM TEAM MODULE (WITH FIXED TABLES) ---
    elif st.session_state.role == "NONBOMTEAM":
        st.header("📦 Non-BOM Activity Management")
        nb_tab1, nb_tab2, nb_tab3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS TRACKER"])
        
        with nb_tab1:
            st.subheader("PR to PO Daily Entry")
            with st.form("dt_form_nb", clear_on_submit=True):
                c1, c2, c3, c4 = st.columns(4)
                d_date = c1.date_input("DATE")
                d_plant = c2.text_input("PLANT")
                d_pr = c3.number_input("PR RECEIPTS", min_value=0)
                d_po = c4.number_input("PO DONE", min_value=0)
                if st.form_submit_button("SUBMIT RECORD"):
                    st.session_state.daily_tracker.append({
                        "S.NO": len(st.session_state.daily_tracker)+1, "DATE": str(d_date), 
                        "PLANT": d_plant, "PR RECEIPTS": d_pr, "PO DONE": d_po, 
                        "BALANCE PR'S": d_pr - d_po, "HOD COMMENTS": ""
                    })
                    st.rerun()
            st.write("### Current Daily Records")
            if st.session_state.daily_tracker:
                st.table(pd.DataFrame(st.session_state.daily_tracker))

        with nb_tab2:
            st.subheader("Advance Payment Entry")
            with st.form("adv_form_nb", clear_on_submit=True):
                c1, c2, c3 = st.columns(3); s_d, v_n, v_t = c1.date_input("SUBMIT DATE"), c2.text_input("VENDOR NAME"), c3.selectbox("TYPE", ["BOM", "NONBOM"])
                c4, c5, c6 = st.columns(3); pi_n, pi_d, po_n = c4.text_input("PI NO"), c5.date_input("PI DATE"), c6.text_input("PO NO")
                c7, c8, c9 = st.columns(3); po_d, p_amt, p_rem = c7.date_input("PO DATE"), c8.number_input("AMOUNT"), c9.text_input("REMARKS")
                if st.form_submit_button("SUBMIT ADVANCE"):
                    st.session_state.advance_payments.append({
                        "SUBMIT DATE": str(s_d), "VENDOR NAME": v_n, "TYPE": v_t, "PI NO": pi_n, 
                        "PI DATE": str(pi_d), "PO NO": po_n, "PO DATE": str(po_d), "AMOUNT": p_amt, 
                        "REMARKS": p_rem, "PAYMENT STATUS": "PENDING", "MATERIAL STATUS": "PENDING"
                    })
                    st.rerun()
            st.write("### Submitted Advance Requests")
            if st.session_state.advance_payments:
                st.dataframe(pd.DataFrame(st.session_state.advance_payments).style.applymap(apply_payment_colors), use_container_width=True)

        with nb_tab3:
            st.subheader("MIS Database")
            df_mis = pd.DataFrame(st.session_state.mis_data, columns=[
                "SUBMIT DATE", "VENDOR NAME", "TYPE", "PART NUMBER", "MATERIAL DESCRIPTION", 
                "TOTAL QTY", "RECEIVED QTY", "PENDING QTY", "STATUS", "HOD COMMENTS"
            ])
            mis_edit = st.data_editor(df_mis, num_rows="dynamic", use_container_width=True)
            if st.button("SAVE MIS UPDATES"): 
                st.session_state.mis_data = mis_edit.to_dict('records')
                st.success("Saved!"); st.rerun()

    # --- 🟠 HOD / GM MODULE ---
    elif st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("NAVIGATE", ["BOM APPROVALS", "NON-BOM REVIEW"])
        
        if menu == "BOM APPROVALS":
            st.header("📋 BOM Price Approvals")
            for i, row in enumerate(st.session_state.master_data):
                if (st.session_state.role == "HOD" and row["STATUS"] == "PENDING") or (st.session_state.role == "GM_OFFICE" and row["HOD APPROVAL"] == "APPROVED" and row["GM APPROVAL"] == ""):
                    with st.container(border=True):
                        st.write(f"**PROJECT:** {row['PROJECT']} | **PART:** {row['PARTNUMBER']} | **PRICE:** {row['PRICE']}")
                        dec = st.selectbox("DECISION", ["PENDING", "APPROVED", "REJECTED"], key=f"h_bom_{i}")
                        if st.button("SAVE DECISION", key=f"h_btn_{i}"):
                            if st.session_state.role == "HOD": st.session_state.master_data[i].update({"HOD APPROVAL": dec, "STATUS": dec})
                            else: st.session_state.master_data[i].update({"GM APPROVAL": dec, "STATUS": dec})
                            st.rerun()

        elif menu == "NON-BOM REVIEW":
            st.header("📋 Non-BOM Data Review")
            c1, c2, c3 = st.columns(3)
            if c1.button("📅 DAILY", use_container_width=True): st.session_state.nb_choice = "DAILY"
            if c2.button("💳 ADVANCE", use_container_width=True): st.session_state.nb_choice = "ADV"
            if c3.button("📊 MIS", use_container_width=True): st.session_state.nb_choice = "MIS"
            
            st.divider()
            if st.session_state.nb_choice == "DAILY" and st.session_state.daily_tracker:
                st.table(pd.DataFrame(st.session_state.daily_tracker))
            elif st.session_state.nb_choice == "ADV" and st.session_state.advance_payments:
                st.dataframe(pd.DataFrame(st.session_state.advance_payments).style.applymap(apply_payment_colors), use_container_width=True)
            elif st.session_state.nb_choice == "MIS" and st.session_state.mis_data:
                st.dataframe(pd.DataFrame(st.session_state.mis_data).style.applymap(style_status, subset=['STATUS']), use_container_width=True)
