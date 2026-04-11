import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURATION & INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Database File Paths
DB_BOM = "resolute_db.csv"
DB_DAILY = "daily_tracker.csv"
DB_ADVANCE = "advance_payments.csv"
DB_MIS = "mis_tracker.csv"

# Unified User Credentials
USERS = {
    "BOMTEAM": "BOM123",
    "NONBOMTEAM": "NONBOM123",
    "HOD": "HOD789",
    "GM": "GM123"
}

# Initialize CSV files if they don't exist
def init_csv(file_path, columns):
    if not os.path.exists(file_path):
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

init_csv(DB_BOM, ["Request ID", "Project", "Part Number", "Description", "BOM", "UOM", "Supplier", "Price", "Remarks", "HOD Approval", "HOD Comments", "GM Approval", "GM Comments", "Status", "Timestamp", "Raised By"])
init_csv(DB_DAILY, ["DATE", "PLANT", "PR RECEIPTS", "PO DONE", "BALANCE PR'S", "HOD COMMENTS"])
init_csv(DB_ADVANCE, ["SUBMIT DATE", "VENDOR NAME", "TYPE", "PI/INVOICE NO", "INVOICE DATE", "PO NO", "PO DATE", "AMOUNT", "REMARKS", "PAYMENT STATUS", "MATERIAL STATUS", "GRN No", "ACCOUNTING STATUS"])
init_csv(DB_MIS, ["SUPPLIER NAME", "PO NO", "PO DATE", "PART NO", "MATERIAL DESCRIPTION", "QUANTITY", "UOM", "Act Unit price", "Act Basic Amt", "RECEIVED QTY", "PENDING QTY", "GRN NO", "PAYMENT STATUS", "ACCOUNTING STATUS"])

# Persistent session state for Auth
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = None

# --- STYLING FUNCTION (Updated to map compatibility) ---
def style_status(val):
    val_upper = str(val).upper()
    if any(x in val_upper for x in ["APPROVED SUCCESSFULLY", "APPROVED", "CLOSED", "DONE", "RECEIVED", "ACCOUNTED"]):
        return 'background-color: green; color: white; font-weight: bold'
    elif any(x in val_upper for x in ["PENDING", "INCOMPLETE"]):
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    elif any(x in val_upper for x in ["REJECTED"]):
        return 'background-color: red; color: white; font-weight: bold'
    elif any(x in val_upper for x in ["OPEN", "INPROCESS"]):
        return 'background-color: orange; color: black; font-weight: bold'
    return ''

# --- 2. LOGIN UI ---
if not st.session_state.auth:
    login_col, img_col = st.columns([1, 2])
    with login_col:
        st.markdown("# 🏗️ Procurement \n### Approval Portal")
        st.divider()
        user_select = st.selectbox("Select Role", list(USERS.keys()))
        pass_input = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if pass_input == USERS[user_select]:
                st.session_state.auth = True
                st.session_state.user = user_select
                st.rerun()
            else:
                st.error("Invalid Password")
    with img_col:
        st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1200", use_container_width=True)
    st.stop()

# --- 3. NAVIGATION ---
st.sidebar.title(f"👤 {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False; st.session_state.user = None; st.rerun()

role = st.session_state.user
if role == "BOMTEAM":
    menu = st.sidebar.radio("Menu", ["Data Entry", "Status Board"])
elif role == "NONBOMTEAM":
    menu = "NonBOM Activity"
else: # HOD or GM
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "NonBOM Activity", "Status Board"])

# --- 4. BOM TEAM MODULE ---
if menu == "Data Entry":
    st.header(f"New Price Request")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            proj, part = st.text_input("Project"), st.text_input("Part Number")
            desc = st.text_area("Description")
        with col2:
            bom = st.number_input("BOM/Qty", min_value=0)
            uom = st.selectbox("UOM", ["Nos", "Sets", "Mtrs", "Kgs"])
            supp, price = st.text_input("Supplier"), st.number_input("Price", min_value=0.0)
        rem = st.text_input("Remarks")
        
        if st.form_submit_button("Submit Request"):
            df = pd.read_csv(DB_BOM)
            req_id = f"REQ-{datetime.now().strftime('%y%m%d%H%M%S')}"
            new_row = pd.DataFrame([{
                "Request ID": req_id, "Project": proj, "Part Number": part, "Description": desc, 
                "BOM": bom, "UOM": uom, "Supplier": supp, "Price": price, "Remarks": rem, 
                "HOD Approval": "Pending", "HOD Comments": "-", "GM Approval": "Pending", 
                "GM Comments": "-", "Status": "Pending HOD", "Timestamp": datetime.now(), "Raised By": role
            }])
            pd.concat([df, new_row], ignore_index=True).to_csv(DB_BOM, index=False)
            st.success(f"Request {req_id} submitted!")

elif menu == "BOM Team Requests":
    st.header(f"{role} Approval Panel")
    df = pd.read_csv(DB_BOM)
    status_to_check = "Pending HOD" if role == "HOD" else "Pending GM"
    pending = df[df["Status"] == status_to_check]
    
    if pending.empty:
        st.info(f"No requests pending for {role}.")
    else:
        for i, row in pending.iterrows():
            with st.expander(f"ID: {row['Request ID']} | Project: {row['Project']}"):
                st.write(row)
                decision = st.selectbox("Decision", ["Pending", "Approved", "Rejected"], key=f"d_{i}")
                comm = st.text_input("Comments", key=f"c_{i}")
                if st.button("Submit Decision", key=f"b_{i}"):
                    df.at[i, f"{role} Approval"] = decision
                    df.at[i, f"{role} Comments"] = comm
                    if decision == "Approved":
                        df.at[i, "Status"] = "Pending GM" if role == "HOD" else "Approved Successfully"
                    elif decision == "Rejected":
                        df.at[i, "Status"] = f"Rejected by {role}"
                    df.to_csv(DB_BOM, index=False)
                    st.rerun()

# --- 5. NON-BOM TEAM MODULE ---
elif menu == "NonBOM Activity":
    st.header("📦 Non-BOM Activity Management")
    tab1, tab2, tab3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS TRACKER"])

    with tab1:
        df_dt = pd.read_csv(DB_DAILY)
        if role == "NONBOMTEAM":
            with st.form("dt_form", clear_on_submit=True):
                c1, c2, c3, c4 = st.columns(4)
                d_date, d_plant = c1.date_input("DATE"), c2.text_input("PLANT")
                d_pr, d_po = c3.number_input("PR RECEIPTS", min_value=0), c4.number_input("PO DONE", min_value=0)
                if st.form_submit_button("ADD ENTRY"):
                    new_dt = pd.DataFrame([{"DATE": str(d_date), "PLANT": d_plant, "PR RECEIPTS": d_pr, "PO DONE": d_po, "BALANCE PR'S": d_pr-d_po, "HOD COMMENTS": ""}])
                    pd.concat([df_dt, new_dt], ignore_index=True).to_csv(DB_DAILY, index=False)
                    st.rerun()
        
        edited_dt = st.data_editor(df_dt, use_container_width=True, key="dt_edit", disabled=(role != "NONBOMTEAM" and role != "HOD"))
        if st.button("Save Tracker Changes"):
            edited_dt.to_csv(DB_DAILY, index=False)
            st.success("Daily Tracker Updated!")

    with tab2:
        df_adv = pd.read_csv(DB_ADVANCE)
        if role == "NONBOMTEAM":
            with st.form("adv_form", clear_on_submit=True):
                r1c1, r1c2, r1c3 = st.columns(3); v_name, v_type, v_pi = r1c1.text_input("VENDOR"), r1c2.selectbox("TYPE", ["Advance", "Partial", "Full"]), r1c3.text_input("PI NO")
                r2c1, r2c2, r2c3 = st.columns(3); v_po, v_amt, v_rem = r2c1.text_input("PO NO"), r2c2.number_input("AMOUNT"), r2c3.text_input("REMARKS")
                if st.form_submit_button("SUBMIT ADVANCE"):
                    new_adv = pd.DataFrame([{"SUBMIT DATE": str(datetime.now().date()), "VENDOR NAME": v_name, "TYPE": v_type, "PI/INVOICE NO": v_pi, "AMOUNT": v_amt, "PAYMENT STATUS": "PENDING", "ACCOUNTING STATUS": "PENDING"}])
                    pd.concat([df_adv, new_adv], ignore_index=True).to_csv(DB_ADVANCE, index=False)
                    st.rerun()
        
        # Fixed: Use .map() instead of .applymap()
        st.dataframe(df_adv.style.map(style_status, subset=["PAYMENT STATUS", "ACCOUNTING STATUS"]), use_container_width=True)

    with tab3:
        df_mis = pd.read_csv(DB_MIS)
        if role == "NONBOMTEAM":
            with st.form("mis_form", clear_on_submit=True):
                m1, m2, m3 = st.columns(3); m_supp, m_po, m_qty = m1.text_input("SUPPLIER"), m2.text_input("PO NO"), m3.number_input("QTY", min_value=0)
                if st.form_submit_button("SUBMIT MIS"):
                    new_mis = pd.DataFrame([{"SUPPLIER NAME": m_supp, "PO NO": m_po, "QUANTITY": m_qty, "PAYMENT STATUS": "INCOMPLETE", "ACCOUNTING STATUS": "PENDING"}])
                    pd.concat([df_mis, new_mis], ignore_index=True).to_csv(DB_MIS, index=False)
                    st.rerun()
        
        # Fixed: Use .map() instead of .applymap()
        st.dataframe(df_mis.style.map(style_status, subset=["PAYMENT STATUS", "ACCOUNTING STATUS"]), use_container_width=True)

# --- 6. STATUS BOARD ---
elif menu == "Status Board":
    st.header("📊 Transaction Audit History (BOM)")
    df = pd.read_csv(DB_BOM)
    # Fixed: Use .map() instead of .applymap()
    styled_df = df.style.map(style_status, subset=['HOD Approval', 'GM Approval', 'Status'])
    st.dataframe(styled_df, use_container_width=True, height=600)
