import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. INITIAL SETUP ---
st.set_page_config(page_title="Resolute Approval System", layout="wide")
DB_FILE = "approval_database.csv"

# Define User Credentials
USERS = {
    "BOMTEAM": "BOM123",
    "NONBOM TEAM": "NON123",
    "HOD": "HOD123",
    "GM": "GM123"
}

# Initialize Database
if not os.path.exists(DB_FILE):
    columns = [
        "Request ID", "Project", "Part Number", "Description", "BOM", "UOM", 
        "Supplier", "Price", "Remarks", "HOD Approval", "HOD Comments", 
        "GM Approval", "GM Comments", "Status", "Timestamp"
    ]
    pd.DataFrame(columns=columns).to_csv(DB_FILE, index=False)

# Session State for Login
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    st.title("🔐 Resolute Management Login")
    user_select = st.selectbox("Select User Role", list(USERS.keys()))
    pass_input = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        if pass_input == USERS[user_select]:
            st.session_state.auth = True
            st.session_state.user = user_select
            st.rerun()
        else:
            st.error("❌ Incorrect Password")
    st.stop()

# --- 3. GLOBAL DATA HELPER ---
def get_data(): return pd.read_csv(DB_FILE)
def save_data(df): df.to_csv(DB_FILE, index=False)

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title(f"User: {st.session_state.user}")
if st.session_state.user == "BOMTEAM":
    menu = st.sidebar.radio("Navigation", ["BOM Entry", "Status Table"])
elif st.session_state.user == "HOD":
    menu = st.sidebar.radio("Navigation", ["BOM Team Requests", "NonBOM Team", "Dashboard", "Audit Logs"])
elif st.session_state.user == "GM":
    menu = st.sidebar.radio("Navigation", ["BOM Team Requests", "Dashboard", "Audit Logs"])
else: # NONBOM
    menu = st.sidebar.radio("Navigation", ["NonBOM Entry"])

if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 5. BOMTEAM PAGE ---
if st.session_state.user == "BOMTEAM":
    if menu == "BOM Entry":
        st.header("Create Price Approval Request")
        with st.form("bom_form"):
            c1, c2 = st.columns(2)
            with c1:
                proj = st.text_input("Project")
                part = st.text_input("Part Number")
                desc = st.text_area("Description")
            with c2:
                bom = st.number_input("BOM Quantity", min_value=0)
                uom = st.selectbox("UOM", ["Nos", "Mtrs", "Sets", "Kgs"])
                supp = st.text_input("Supplier")
                price = st.number_input("Price", min_value=0.0)
                rem = st.text_input("Remarks")
            
            if st.form_submit_button("Submit to HOD"):
                req_id = f"REQ-{datetime.now().strftime('%y%m%d%H%M%S')}"
                new_row = {
                    "Request ID": req_id, "Project": proj, "Part Number": part,
                    "Description": desc, "BOM": bom, "UOM": uom, "Supplier": supp,
                    "Price": price, "Remarks": rem, "HOD Approval": "Pending",
                    "HOD Comments": "", "GM Approval": "Pending", "GM Comments": "",
                    "Status": "Pending at HOD", "Timestamp": datetime.now()
                }
                df = get_data()
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success(f"Request {req_id} Submitted!")
                st.info(f"📧 Notification sent to HOD. Subject: Price approval request received - {req_id}")

    # Visual Table below for BOMTEAM
    st.subheader("BOM Request History")
    st.dataframe(get_data())

# --- 6. HOD PAGE ---
elif st.session_state.user == "HOD":
    if menu == "BOM Team Requests":
        st.header("Pending BOM Approvals")
        df = get_data()
        pending = df[df["Status"] == "Pending at HOD"]
        
        if pending.empty:
            st.info("No pending requests.")
        else:
            for i, row in pending.iterrows():
                with st.expander(f"Request: {row['Request ID']} - {row['Project']}"):
                    st.write(row)
                    decision = st.selectbox("Decision", ["Pending", "Approved", "Rejected"], key=f"d_{i}")
                    comm = st.text_input("HOD Comments", key=f"c_{i}")
                    if st.button("Submit Decision", key=f"b_{i}"):
                        df.at[i, "HOD Approval"] = decision
                        df.at[i, "HOD Comments"] = comm
                        if decision == "Approved":
                            df.at[i, "Status"] = "Pending at GM"
                            st.info(f"📧 Mail sent to GM for Request {row['Request ID']}")
                        else:
                            df.at[i, "Status"] = f"Rejected by HOD ({comm})"
                        save_data(df)
                        st.rerun()
    elif menu == "Audit Logs":
        st.header("Decision History")
        st.table(get_data())

# --- 7. GM PAGE ---
elif st.session_state.user == "GM":
    if menu == "BOM Team Requests":
        st.header("GM Final Approval")
        df = get_data()
        pending = df[df["Status"] == "Pending at GM"]
        
        if pending.empty:
            st.info("No requests pending GM approval.")
        else:
            for i, row in pending.iterrows():
                with st.expander(f"Request: {row['Request ID']} (HOD Approved)"):
                    st.write(f"HOD Comments: {row['HOD Comments']}")
                    st.write(row)
                    decision = st.selectbox("Final Decision", ["Pending", "Approved", "Rejected"], key=f"gm_d_{i}")
                    comm = st.text_input("GM Comments", key=f"gm_c_{i}")
                    if st.button("Confirm Final Approval", key=f"gm_b_{i}"):
                        df.at[i, "GM Approval"] = decision
                        df.at[i, "GM Comments"] = comm
                        if decision == "Approved":
                            df.at[i, "Status"] = "Approved Successfully"
                            st.success("📧 All parties notified: Price Approved!")
                        else:
                            df.at[i, "Status"] = f"Rejected by GM ({comm})"
                        save_data(df)
                        st.rerun()
    elif menu == "Audit Logs":
        st.table(get_data())
