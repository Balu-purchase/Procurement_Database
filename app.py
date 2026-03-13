import streamlit as st
import pandas as pd
from datetime import datetime
import os
import smtplib  # Added for real email
from email.mime.text import MIMEText

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

# --- EMAIL FUNCTION ---
# Note: You need a Gmail App Password to make this work for real.
def send_notification(subject, body, to_email="hod_email@example.com"):
    # This is a placeholder. To enable real emails, uncomment the lines below 
    # and provide your credentials.
    st.info(f"📧 Notification Triggered: {subject}")
    # try:
    #     msg = MIMEText(body)
    #     msg['Subject'] = subject
    #     msg['From'] = "your_email@gmail.com"
    #     msg['To'] = to_email
    #     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    #         server.login("your_email@gmail.com", "your_app_password")
    #         server.send_message(msg)
    # except Exception as e:
    #     st.error(f"Email failed: {e}")

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
# Standardized menu names to prevent logic errors
if st.session_state.user in ["BOMTEAM", "NONBOMTEAM"]:
    menu = st.sidebar.radio("Menu", ["Data Entry", "Status Board"])
elif st.session_state.user == "HOD":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "NonBOM Team", "Dashboard", "Audit Logs"])
elif st.session_state.user == "GM":
    # FIXED: Added BOM Team Requests here so it matches the IF statement below
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "Dashboard", "Audit Logs"])

# --- 5. DATA ENTRY (BOM & NON-BOM) ---
if menu == "Data Entry":
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
            
            # TRIGGER EMAIL TO HOD
            send_notification(f"Price approval request received - {req_id}", f"New request {req_id} from BOM Team is pending.")
            
            st.success(f"Request {req_id} submitted!")
            st.rerun()

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
                        # TRIGGER EMAIL TO GM
                        send_notification(f"Price approval request received - {row['Request ID']}", "HOD has approved. Final GM approval needed.")
                    elif decision == "Rejected":
                        df.at[i, "Status"] = f"Rejected by HOD: {h_comm}"
                    save_data(df)
                    st.rerun()

# --- 7. GM APPROVAL SECTION ---
elif menu == "BOM Team Requests" and st.session_state.user == "GM":
    st.header("GM Final Approval Panel")
    df = get_data()
    # FIXED: The GM logic now correctly looks for "Pending GM" status
    pending_gm = df[df["Status"] == "Pending GM"]
    
    if pending_gm.empty:
        st.info("No requests pending for GM.")
    else:
        for i, row in pending_gm.iterrows():
            with st.expander(f"ID: {row['Request ID']} (Approved by HOD)"):
                st.write(f"HOD Comments: {row['HOD Comments']}")
                st.write(row)
                decision = st.selectbox("Final Decision", ["Pending", "Approved", "Rejected"], key=f"g_{i}")
                g_comm = st.text_input("GM Comments", key=f"gc_{i}")
                if st.button("Confirm Final Approval", key=f"gb_{i}"):
                    df.at[i, "GM Approval"] = decision
                    df.at[i, "GM Comments"] = g_comm
                    if decision == "Approved":
                        df.at[i, "Status"] = "Approved Successfully"
                        send_notification("Price Approval Success", f"Request {row['Request ID']} has been fully approved.")
                    elif decision == "Rejected":
                        df.at[i, "Status"] = f"Rejected by GM: {g_comm}"
                    save_data(df)
                    st.rerun()

# --- 8. AUDIT LOGS / DASHBOARD ---
elif menu in ["Audit Logs", "Dashboard", "Status Board"]:
    st.header("Transaction Audit History")
    st.dataframe(get_data())
