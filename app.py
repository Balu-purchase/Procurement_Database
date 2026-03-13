import streamlit as st
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Procurement System", layout="wide")
DB_FILE = "resolute_db.csv"

USERS = {
    "BOMTEAM": "BOM123",
    "NONBOMTEAM": "NONBOM123",
    "HOD": "HOD789",
    "GM": "GM123"
}

# --- STYLING FUNCTION (Bold + Full Cell Color) ---
def style_status(val):
    val_upper = str(val).upper()
    # Green for Approved
    if "APPROVED SUCCESSFULLY" in val_upper or val_upper == "APPROVED":
        return 'background-color: green; color: white; font-weight: bold'
    # Light Orange for Pending
    elif "PENDING" in val_upper:
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    # Red for Rejected
    elif "REJECTED" in val_upper:
        return 'background-color: red; color: white; font-weight: bold'
    return ''

# --- EMAIL FUNCTION ---
def send_notification(subject, body, to_email="hod_email@example.com"):
    st.info(f"📧 Notification Triggered: {subject}")

# Database Initialization
if not os.path.exists(DB_FILE):
    cols = ["Request ID", "Project", "Part Number", "Description", "BOM", "UOM", "Supplier", "Price", "Remarks", "HOD Approval", "HOD Comments", "GM Approval", "GM Comments", "Status", "Timestamp", "Raised By"]
    pd.DataFrame(columns=cols).to_csv(DB_FILE, index=False)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None

# --- 2. ENHANCED LOGIN UI (Left: Login, Right: Office Image) ---
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

# --- 3. NAVIGATION & SIDEBAR ---
st.sidebar.title(f"👤 {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False ; st.session_state.user = None ; st.rerun()

def get_data(): return pd.read_csv(DB_FILE)
def save_data(df): df.to_csv(DB_FILE, index=False)

if st.session_state.user in ["BOMTEAM", "NONBOMTEAM"]:
    menu = st.sidebar.radio("Menu", ["Data Entry", "Status Board"])
elif st.session_state.user == "HOD":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "NonBOM Team", "Dashboard", "Audit Logs"])
elif st.session_state.user == "GM":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "Dashboard", "Audit Logs"])

# --- 4. DATA ENTRY ---
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

# --- 5. HOD/GM APPROVAL PANEL ---
elif menu == "BOM Team Requests" and st.session_state.user in ["HOD", "GM"]:
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

# --- 6. DASHBOARD WITH MULTI-COLUMN COLORING ---
elif menu in ["Audit Logs", "Dashboard", "Status Board"]:
    st.header("📊 Transaction Audit History")
    df = get_data()
    
    # APPLY COLORS TO ALL THREE COLUMNS: HOD Approval, GM Approval, and Status
    styled_df = df.style.applymap(
        style_status, 
        subset=['HOD Approval', 'GM Approval', 'Status']
    )
    
    st.dataframe(styled_df, use_container_width=True, height=600)
