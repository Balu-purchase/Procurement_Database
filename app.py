import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Persistent lists (In a real app, these would sync to Google Sheets GID 466678125)
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
    if val in ["APPROVED", "CLOSED", "DONE", "RECEIVED"]: 
        return 'background-color: green; color: white; font-weight: bold'
    if val in ["REJECTED", "PENDING"]: 
        return 'background-color: red; color: white; font-weight: bold'
    return ''

def apply_payment_colors(val):
    if val in ["DONE", "RECEIVED", "ACCOUNTED"]: return 'background-color: green; color: white'
    elif val in ["PENDING", "HOLD"]: return 'background-color: yellow; color: black'
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

    # Define menu based on role
    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("NAVIGATE", ["BOM PRICE APPROVALS", "NON-BOM REVIEW", "AUDIT LOGS"])
    else:
        menu = "MAIN"

    st.title("PRICE APPROVALS FOR BOM ITEMS")
    st.divider()

    # --- 🔵 BOM TEAM MODULE ---
    if st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team: Manual Entry")
        with st.form("bom_entry_form", clear_on_submit=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            p_proj, p_num, p_desc, p_qps = r1c1.text_input("PROJECT"), r1c2.text_input("PART NUMBER"), r1c3.text_input("DESCRIPTION"), r1c4.text_input("QPS")
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            p_uom, p_supp, p_price, p_rem = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Ltr"]), r2c2.text_input("SUPPLIER NAME"), r2c3.text_input("PRICE"), r2c4.text_input("REMARKS")
            if st.form_submit_button("SUBMIT BOM REQUEST"):
                st.session_state.master_data.append({
                    "PROJECT": p_proj, "PARTNUMBER": p_num, "DESCRIPTION": p_desc, "QPS": p_qps, 
                    "UOM": p_uom, "SUPPLIER": p_supp, "PRICE": p_price, "REMARKS": p_rem, 
                    "HOD": "", "GM": "", "STATUS": "PENDING"
                })
                st.rerun()
        
        st.write("### Submitted Data (Reflects HOD Changes)")
        if st.session_state.master_data:
            df_bom_view = pd.DataFrame(st.session_state.master_data)
            st.dataframe(df_bom_view.style.applymap(style_status, subset=['STATUS']), use_container_width=True)

    # --- 🟢 NON-BOM TEAM MODULE ---
    elif st.session_state.role == "NONBOMTEAM":
        t1, t2, t3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS TRACKER"])
        
        with t1:
            with st.form("dt_nb"):
                c1, c2, c3, c4 = st.columns(4)
                d_d, d_p = c1.date_input("DATE"), c2.text_input("PLANT")
                d_r, d_o = c3.number_input("PR RECEIPTS", min_value=0), c4.number_input("PO DONE", min_value=0)
                if st.form_submit_button("SUBMIT"):
                    st.session_state.daily_tracker.append({"S.NO": len(st.session_state.daily_tracker)+1, "DATE": str(d_d), "PLANT": d_p, "PR RECEIPTS": d_r, "PO DONE": d_o, "BALANCE PR'S": d_r - d_o, "HOD COMMENTS": ""})
                    st.rerun()
            st.table(pd.DataFrame(st.session_state.daily_tracker))

        with t2:
            st.subheader("Advance Payment - Editable Status")
            df_adv = pd.DataFrame(st.session_state.advance_payments)
            if not df_adv.empty:
                edited_adv = st.data_editor(df_adv, column_config={
                        "PAYMENT STATUS": st.column_config.SelectboxColumn("PAYMENT STATUS", options=["PENDING", "DONE", "HOLD"]),
                        "MATERIAL STATUS": st.column_config.SelectboxColumn("MATERIAL STATUS", options=["PENDING", "RECEIVED", "IN-TRANSIT"])
                    }, use_container_width=True, key="exec_adv_edit")
                if st.button("SAVE STATUS UPDATES"):
                    st.session_state.advance_payments = edited_adv.to_dict('records')
                    st.rerun()
                st.dataframe(edited_adv.style.applymap(apply_payment_colors, subset=['PAYMENT STATUS', 'MATERIAL STATUS']), use_container_width=True)

    # --- 🟠 HOD / GM MODULE (FULL EDITING AUTHORIZED) ---
    elif st.session_state.role in ["HOD", "GM_OFFICE"]:
        if menu == "BOM PRICE APPROVALS":
            st.header("📋 Master BOM Editor & Approvals")
            st.info("HOD Note: You can edit any cell below. Changes will reflect for the BOM Team.")
            
            if st.session_state.master_data:
                df_bom_master = pd.DataFrame(st.session_state.master_data)
                # Full editing enabled for HOD
                edited_bom = st.data_editor(
                    df_bom_master,
                    column_config={
                        "HOD": st.column_config.SelectboxColumn("HOD", options=["", "APPROVED", "REJECTED"]),
                        "GM": st.column_config.SelectboxColumn("GM", options=["", "APPROVED", "REJECTED"]),
                        "STATUS": st.column_config.SelectboxColumn("STATUS", options=["PENDING", "APPROVED", "REJECTED"])
                    },
                    use_container_width=True, key="hod_bom_editor"
                )
                if st.button("SAVE ALL BOM CHANGES"):
                    st.session_state.master_data = edited_bom.to_dict('records')
                    st.success("All changes synced to BOM Team!"); st.rerun()
            else:
                st.warning("No BOM requests to display.")

        elif menu == "NON-BOM REVIEW":
            c1, c2, c3 = st.columns(3)
            if c1.button("📅 DAILY TRACKER", use_container_width=True): st.session_state.nb_choice = "DAILY"
            if c2.button("💳 ADVANCE PAYMENTS", use_container_width=True): st.session_state.nb_choice = "ADV"
            if c3.button("📊 MIS TRACKER", use_container_width=True): st.session_state.nb_choice = "MIS"
            
            st.divider()
            
            if st.session_state.nb_choice == "DAILY" and st.session_state.daily_tracker:
                df_dt_hod = pd.DataFrame(st.session_state.daily_tracker)
                edited_dt = st.data_editor(df_dt_hod, use_container_width=True, key="hod_dt_edit")
                if st.button("SAVE TRACKER CHANGES"):
                    st.session_state.daily_tracker = edited_dt.to_dict('records')
                    st.rerun()

            elif st.session_state.nb_choice == "ADV" and st.session_state.advance_payments:
                df_adv_hod = pd.DataFrame(st.session_state.advance_payments)
                edited_adv_hod = st.data_editor(df_adv_hod, use_container_width=True, key="hod_adv_edit")
                if st.button("SAVE ADVANCE CHANGES"):
                    st.session_state.advance_payments = edited_adv_hod.to_dict('records')
                    st.rerun()

        elif menu == "AUDIT LOGS":
            st.subheader("BOM Master Audit Trail")
            if st.session_state.master_data:
                st.dataframe(pd.DataFrame(st.session_state.master_data).style.applymap(style_status, subset=['STATUS']), use_container_width=True)
