import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Resolute Approval System", layout="wide")
DB_FILE = "resolute_db.csv"

# User Credentials
USERS = {
    "BOMTEAM": "BOM123",
    "NONBOMTEAM": "NONBOM123",
    "HOD": "HOD789",
    "GM": "GM123"
}

# Database Initialization
if not os.path.exists(DB_FILE):
    cols = [
        "Request ID", "Project", "Part Number", "Description", "BOM", "UOM", 
        "Supplier", "Price", "Remarks", "HOD Approval", "HOD Comments", 
        "GM Approval", "GM Comments", "Status", "Timestamp", "Raised By"
    ]
    pd.DataFrame(columns=cols).to_csv(DB_FILE, index=False)

# Session Management
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None

# --- 2. LOGIN / LOGOUT UI ---
if not st.session_state.auth:
    st.title("🏗️ Resolute Approval Portal")
    user_select = st.selectbox("Select Role", list(USERS.keys()))
    pass_input = st.text_input("Password", type="password")
    if st.button("Login"):
        if pass_input == USERS[user_select]:
            st.session_state.auth = True
            st.session_state.user = user_select
            st.rerun()
        else:
            st.error("Invalid Password")
    st.stop()

# Logout Button in Sidebar
st.sidebar.title(f"Logged in: {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.session_state.user = None
    st.rerun()

# --- 3. DATA PERSISTENCE HELPERS ---
def get_data(): 
    return pd.read_csv(DB_FILE)

def save_data(df): 
    df.to_csv(DB_FILE, index=False)

# --- 4. NAVIGATION LOGIC ---
if st.session_state.user in ["BOMTEAM", "NONBOMTEAM"]:
    menu = st.sidebar.radio("Menu", ["Data Entry", "Status Board"])
elif st.session_state.user == "HOD":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "NonBOM Team", "Dashboard", "Audit Logs"])
elif st.session_state.user == "GM":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "Dashboard", "Audit Logs"])

# --- 5. DATA ENTRY (BOM & NON-BOM) ---
if menu in ["Data Entry", "BOM Entry"]:
    st.header(f"New Price Request - {st.session_state.user}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            proj = st.text_input("Project")
            part = st.text_input("Part Number")
            desc = st.text_area("Description")
        with col2:
            bom = st.number_input("BOM/Qty", min_value=0)
            uom = st.selectbox("UOM", ["Nos", "Sets", "Mtrs", "Kgs"])
            supp = st.text_input("Supplier")
            price = st.number_input("Price", min_value=0.0)
        rem = st.text_input("Remarks")
        
        if st.form_submit_button("Submit Request"):
            req_id = f"REQ-{datetime.now().strftime('%y%m%d%H%M%S')}"
            new_row = {
                "Request ID": req_id, "Project": proj, "Part Number": part,
                "Description": desc, "BOM": bom, "UOM": uom, "Supplier": supp,
                "Price": price, "Remarks": rem, "HOD Approval": "Pending",
                "HOD Comments": "-", "GM Approval": "Pending", "GM Comments": "-",
                "Status": "Pending HOD", "Timestamp": datetime.now(), 
                "Raised By": st.session_state.user
            }
            df = get_data()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success(f"Request {req_id} submitted!")
            st.info(f"📧 Notification sent to HOD - Subject: Price approval request received - {req_id}")

    st.subheader("Your Submission Table")
    st.dataframe(get_data())

# --- 6. HOD APPROVAL SECTION ---
elif menu == "BOM Team Requests" and st.session_state.user == "HOD":
    st.header("HOD Approval Panel")
    df = get_data()
    pending_hod = df[df["Status"] == "Pending HOD"]
    
    if pending_hod.empty:
        st.info("No requests pending for HOD.")
    else:
        for i, row in pending_hod.iterrows():
            with st.expander(f"ID: {row['Request ID']} | Project: {row['Project']}"):
                st.write(row)
                decision = st.selectbox("Decision", ["Pending", "Approved", "Rejected"], key=f"h_{i}")
                h_comm = st.text_input("HOD Comments", key=f"hc_{i}")
                if st.button("Submit HOD Decision", key=f"hb_{i}"):
                    df.at[i, "HOD Approval"] = decision
                    df.at[i, "HOD Comments"] = h_comm
                    if decision == "Approved":
                        df.at[i, "Status"] = "Pending GM"
                    elif decision == "Rejected":
                        df.at[i, "Status"] = f"Rejected by HOD: {h_comm}"
                    save_data(df)
                    st.rerun()

# ---
