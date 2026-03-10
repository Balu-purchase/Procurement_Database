import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Ensure session state lists exist
if "master_data" not in st.session_state: st.session_state.master_data = []
if "daily_tracker" not in st.session_state: st.session_state.daily_tracker = []
if "advance_payments" not in st.session_state: st.session_state.advance_payments = []
if "mis_data" not in st.session_state: st.session_state.mis_data = []
if "auth" not in st.session_state: st.session_state.auth = False
if "role" not in st.session_state: st.session_state.role = None
if "nb_choice" not in st.session_state: st.session_state.nb_choice = "DAILY"

# --- Helper Functions for Styling ---
def apply_payment_colors(val):
    if val in ["DONE", "RECEIVED", "ACCOUNTED"]: 
        return 'background-color: green; color: white'
    elif val == "PENDING": 
        return 'background-color: yellow; color: black'
    return ''

def style_status(val):
    if val in ["APPROVED", "CLOSED", "DONE"]: return 'background-color: green; color: white'
    if val in ["REJECTED", "PENDING"]: return 'background-color: red; color: white'
    if val == "OPEN": return 'background-color: orange; color: black'
    return ''

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        st.write("### SYSTEM LOGIN")
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

    # --- 🟢 NON-BOM TEAM LOGIC ---
    if st.session_state.role == "NONBOMTEAM":
        st.header("📦 Non-BOM Activity Management")
        tab1, tab2, tab3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS TRACKER"])
        
        with tab1:
            st.subheader("Daily PR to PO Entry")
            with st.form("dt_form", clear_on_submit=True):
                c1, c2, c3, c4 = st.columns(4)
                d_date = c1.date_input("DATE")
                d_plant = c2.text_input("PLANT")
                d_pr = c3.number_input("PR RECEIPTS", min_value=0)
                d_po = c4.number_input("PO DONE", min_value=0)
                if st.form_submit_button("SUBMIT ENTRY"):
                    st.session_state.daily_tracker.append({
                        "S.NO": len(st.session_state.daily_tracker)+1, "DATE": str(d_date), 
                        "PLANT": d_plant, "PR RECEIPTS": d_pr, "PO DONE": d_po, 
                        "BALANCE PR'S": d_pr - d_po, "HOD COMMENTS": ""
                    })
                    st.rerun()
            
            # TABLE MOVED OUTSIDE FORM TO ENSURE VISIBILITY
            st.write("### PR to PO Record List")
            if st.session_state.daily_tracker:
                st.table(pd.DataFrame(st.session_state.daily_tracker))
            else:
                st.info("No entries found in Daily Tracker.")

        with tab2:
            st.subheader("Advance Payment Request Entry")
            with st.form("adv_form", clear_on_submit=True):
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
            
            st.write("### Advance Payment Records")
            if st.session_state.advance_payments:
                df_p = pd.DataFrame(st.session_state.advance_payments)
                st.dataframe(df_p.style.applymap(apply_payment_colors), use_container_width=True)
            else:
                st.info("No Advance Payment requests found.")

        with tab3:
            st.subheader("MIS Tracker Management")
            # We use data_editor to allow manual updates to the MIS list
            df_mis_current = pd.DataFrame(st.session_state.mis_data, columns=[
                "SUBMIT DATE", "VENDOR NAME", "TYPE", "PART NUMBER", "MATERIAL DESCRIPTION", 
                "TOTAL QTY", "RECEIVED QTY", "PENDING QTY", "STATUS", "HOD COMMENTS"
            ])
            
            mis_edit = st.data_editor(df_mis_current, num_rows="dynamic", use_container_width=True, key="mis_editor")
            
            if st.button("SAVE MIS DATABASE"): 
                st.session_state.mis_data = mis_edit.to_dict('records')
                st.success("Database Saved Successfully!")
                st.rerun()

    # --- 🔵 BOM TEAM LOGIC (PRESERVED) ---
    elif st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team: Manual Entry")
        with st.form("bom_form", clear_on_submit=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            p_proj, p_num, p_desc, p_qps = r1c1.text_input("PROJECT"), r1c2.text_input("PART NUMBER"), r1c3.text_input("DESCRIPTION"), r1c4.text_input("QPS")
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            p_uom, p_supp, p_price, p_opt = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Ltr"]), r2c2.text_input("SUPPLIER NAME"), r2c3.text_input("PRICE"), r2c4.text_input("OPTIONAL SUPPLIER")
            if st.form_submit_button("SUBMIT BOM REQUEST"):
                st.session_state.master_data.append({"PROJECT": p_proj, "PARTNUMBER": p_num, "DESCRIPTION": p_desc, "QPS": p_qps, "UOM": p_uom, "SUPPLIER": p_supp, "PRICE": p_price, "OPT_SUPP": p_opt, "HOD APPROVAL": "", "GM APPROVAL": "", "STATUS": "PENDING", "REMARKS": ""})
                st.success("Submitted!"); st.rerun()
        
        st.write("### BOM Submission Status")
        if st.session_state.master_data:
            st.dataframe(pd.DataFrame(st.session_state.master_data).style.applymap(style_status, subset=['STATUS']), use_container_width=True)

    # --- 🟠 HOD / GM LOGIC ---
    elif st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("NAVIGATE", ["BOM APPROVALS", "NON-BOM REVIEW"])
        
        if menu == "NON-BOM REVIEW":
            ic1, ic2, ic3 = st.columns(3)
            if ic1.button("📅 DAILY TRACKER", use_container_width=True): st.session_state.nb_choice = "DAILY"
            if ic2.button("💳 ADVANCE", use_container_width=True): st.session_state.nb_choice = "ADV"
            if ic3.button("📊 MIS", use_container_width=True): st.session_state.nb_choice = "MIS"
            
            st.divider()
            if st.session_state.nb_choice == "DAILY":
                st.write("### Daily Tracker Review")
                if st.session_state.daily_tracker:
                    st.table(pd.DataFrame(st.session_state.daily_tracker))
            elif st.session_state.nb_choice == "ADV":
                st.write("### Advance Payment Review")
                if st.session_state.advance_payments:
                    st.dataframe(pd.DataFrame(st.session_state.advance_payments).style.applymap(apply_payment_colors), use_container_width=True)
            elif st.session_state.nb_choice == "MIS":
                st.write("### MIS Tracker Review")
                if st.session_state.mis_data:
                    st.dataframe(pd.DataFrame(st.session_state.mis_data).style.applymap(style_status, subset=['STATUS']), use_container_width=True)
