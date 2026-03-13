import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURATION & INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")
DB_FILE = "resolute_db.csv"

# Unified User Credentials
USERS = {
    "BOMTEAM": "BOM123",
    "NONBOMTEAM": "NONBOM123",
    "HOD": "HOD789",
    "GM": "GM123"
}

# Persistent state management for Non-BOM Modules
state_keys = {
    "auth": False, 
    "user": None, 
    "daily_tracker": [], 
    "advance_payments": [], 
    "mis_data": []
}
for key, default in state_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- STYLING FUNCTION (Merged Logic) ---
def style_status(val):
    val_upper = str(val).upper()
    # Success/Approved States
    if any(x in val_upper for x in ["APPROVED SUCCESSFULLY", "APPROVED", "CLOSED", "DONE", "RECEIVED", "ACCOUNTED"]):
        return 'background-color: green; color: white; font-weight: bold'
    # Pending/Incomplete States
    elif any(x in val_upper for x in ["PENDING", "INCOMPLETE"]):
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    # Rejected States
    elif any(x in val_upper for x in ["REJECTED"]):
        return 'background-color: red; color: white; font-weight: bold'
    # In Process States
    elif any(x in val_upper for x in ["OPEN", "INPROCESS"]):
        return 'background-color: orange; color: black; font-weight: bold'
    return ''

# BOM Database Initialization
if not os.path.exists(DB_FILE):
    cols = ["Request ID", "Project", "Part Number", "Description", "BOM", "UOM", "Supplier", "Price", "Remarks", "HOD Approval", "HOD Comments", "GM Approval", "GM Comments", "Status", "Timestamp", "Raised By"]
    pd.DataFrame(columns=cols).to_csv(DB_FILE, index=False)

def get_data(): return pd.read_csv(DB_FILE)
def save_data(df): df.to_csv(DB_FILE, index=False)

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
        st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1200", 
                 caption="Resolute Procurement Management", use_container_width=True)
    st.stop()

# --- 3. NAVIGATION ---
st.sidebar.title(f"👤 {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False ; st.session_state.user = None ; st.rerun()

# Define Menus based on Role
if st.session_state.user == "BOMTEAM":
    menu = st.sidebar.radio("Menu", ["Data Entry", "Status Board"])
elif st.session_state.user == "NONBOMTEAM":
    menu = "NonBOM Activity" # Force to NonBOM Module
elif st.session_state.user == "HOD":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "NonBOM Activity", "Dashboard", "Audit Logs"])
elif st.session_state.user == "GM":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "NonBOM Activity", "Dashboard", "Audit Logs"])

# --- 4. BOM TEAM MODULE ---
if menu == "Data Entry":
    st.header(f"New Price Request - {st.session_state.user}")
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
            req_id = f"REQ-{datetime.now().strftime('%y%m%d%H%M%S')}"
            new_row = {
                "Request ID": req_id, "Project": proj, "Part Number": part, "Description": desc, 
                "BOM": bom, "UOM": uom, "Supplier": supp, "Price": price, "Remarks": rem, 
                "HOD Approval": "Pending", "HOD Comments": "-", "GM Approval": "Pending", 
                "GM Comments": "-", "Status": "Pending HOD", "Timestamp": datetime.now(), "Raised By": st.session_state.user
            }
            df = get_data()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success(f"Request {req_id} submitted!")
            st.rerun()

elif menu == "BOM Team Requests":
    role = st.session_state.user
    st.header(f"{role} Approval Panel")
    df = get_data()
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
                    save_data(df)
                    st.rerun()

# --- 5. NON-BOM TEAM MODULE (NEW INTEGRATION) ---
elif menu == "NonBOM Activity":
    st.header("📦 Non-BOM Activity Management")
    tab1, tab2, tab3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS TRACKER"])

    with tab1: # DAILY TRACKER
        if st.session_state.user == "NONBOMTEAM":
            st.subheader("Add Daily PR to PO Tracker")
            with st.form("dt_form", clear_on_submit=True):
                c1, c2, c3, c4 = st.columns(4)
                d_date = c1.date_input("DATE")
                d_plant = c2.text_input("PLANT")
                d_pr = c3.number_input("PR RECEIPTS", min_value=0)
                d_po = c4.number_input("PO DONE", min_value=0)
                if st.form_submit_button("SUBMIT ENTRY"):
                    st.session_state.daily_tracker.append({
                        "DATE": str(d_date), "PLANT": d_plant, "PR RECEIPTS": d_pr, 
                        "PO DONE": d_po, "BALANCE PR'S": d_pr - d_po, "HOD COMMENTS": ""
                    })
                    st.rerun()
        
        if st.session_state.daily_tracker:
            df_dt = pd.DataFrame(st.session_state.daily_tracker)
            if st.session_state.user == "NONBOMTEAM":
                edited_dt = st.data_editor(df_dt, use_container_width=True, key="dt_editor", num_rows="dynamic")
                st.session_state.daily_tracker = edited_dt.to_dict('records')
            else:
                st.dataframe(df_dt, use_container_width=True)

    with tab2: # ADVANCE PAYMENT
        if st.session_state.user == "NONBOMTEAM":
            st.subheader("New Advance Payment Entry")
            with st.form("adv_form", clear_on_submit=True):
                r1c1, r1c2, r1c3, r1c4 = st.columns(4)
                v_name = r1c1.text_input("VENDOR NAME")
                v_type = r1c2.selectbox("TYPE", ["Advance", "Partial", "Full"])
                v_pi = r1c3.text_input("PI/INVOICE NO")
                v_idate = r1c4.date_input("INVOICE DATE")
                r2c1, r2c2, r2c3, r2c4 = st.columns(4)
                v_po, v_pdate = r2c1.text_input("PO NO"), r2c2.date_input("PO DATE")
                v_amt, v_rem = r2c3.number_input("AMOUNT", min_value=0.0), r2c4.text_input("REMARKS")
                if st.form_submit_button("SUBMIT REQUEST"):
                    st.session_state.advance_payments.append({
                        "SUBMIT DATE": str(datetime.now().date()), "VENDOR NAME": v_name, "TYPE": v_type, 
                        "PI/INVOICE NO": v_pi, "INVOICE DATE": str(v_idate), "PO NO": v_po, "PO DATE": str(v_pdate), 
                        "AMOUNT": v_amt, "REMARKS": v_rem, "PAYMENT STATUS": "PENDING", "MATERIAL STATUS": "PENDING", 
                        "GRN No": "", "ACCOUNTING STATUS": "PENDING"
                    })
                    st.rerun()
        
        if st.session_state.advance_payments:
            df_adv = pd.DataFrame(st.session_state.advance_payments)
            if st.session_state.user == "NONBOMTEAM":
                edited_adv = st.data_editor(df_adv, use_container_width=True, key="adv_editor", num_rows="dynamic")
                st.session_state.advance_payments = edited_adv.to_dict('records')
            else:
                st.dataframe(df_adv.style.applymap(style_status, subset=["PAYMENT STATUS", "ACCOUNTING STATUS"]), use_container_width=True)

    with tab3: # MIS TRACKER
        if st.session_state.user == "NONBOMTEAM":
            st.subheader("New MIS Data Entry")
            with st.form("mis_form", clear_on_submit=True):
                m1, m2, m3, m4 = st.columns(4)
                m_supp, m_po, m_pdate, m_part = m1.text_input("SUPPLIER NAME"), m2.text_input("PO NO"), m3.date_input("PO DATE"), m4.text_input("PART NO")
                m5, m6, m7, m8 = st.columns(4)
                m_desc, m_qty, m_uom, m_price = m5.text_input("DESCRIPTION"), m6.number_input("QTY", min_value=0), m7.selectbox("UOM", ["Nos", "KG", "Mtr"]), m8.number_input("Unit Price", min_value=0.0)
                if st.form_submit_button("SUBMIT MIS"):
                    st.session_state.mis_data.append({
                        "SUPPLIER NAME": m_supp, "PO NO": m_po, "PO DATE": str(m_pdate), "PART NO": m_part,
                        "MATERIAL DESCRIPTION": m_desc, "QUANTITY": m_qty, "UOM": m_uom,
                        "Act Unit price": m_price, "Act Basic Amt": m_qty * m_price,
                        "RECEIVED QTY": 0, "PENDING QTY": m_qty, "GRN NO": "", "PAYMENT STATUS": "INCOMPLETE", "ACCOUNTING STATUS": "PENDING"
                    })
                    st.rerun()

        if st.session_state.mis_data:
            df_mis = pd.DataFrame(st.session_state.mis_data)
            if st.session_state.user == "NONBOMTEAM":
                edited_mis = st.data_editor(df_mis, use_container_width=True, key="mis_editor", num_rows="dynamic")
                st.session_state.mis_data = edited_mis.to_dict('records')
            else:
                st.dataframe(df_mis.style.applymap(style_status, subset=["PAYMENT STATUS", "ACCOUNTING STATUS"]), use_container_width=True)

# --- 6. AUDIT & DASHBOARD (BOM STATUS BOARD) ---
elif menu in ["Audit Logs", "Dashboard", "Status Board"]:
    st.header("📊 Transaction Audit History (BOM)")
    df = get_data()
    styled_df = df.style.applymap(style_status, subset=['HOD Approval', 'GM Approval', 'Status'])
    st.dataframe(styled_df, use_container_width=True, height=600)
