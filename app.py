import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Procurement System", layout="wide")
DB_FILE = "resolute_db.csv"

USERS = {
    "BOMTEAM": "BOM123",
    "NONBOMTEAM": "NONBOM123",
    "HOD": "HOD789",
    "GM": "GM123"
}

# --- ENHANCED COLOR LOGIC ---
def apply_color_logic(val):
    val_upper = str(val).upper()
    # FULL GREEN for Approved
    if "APPROVED SUCCESSFULLY" in val_upper or val_upper == "APPROVED":
        return 'background-color: green; color: white; font-weight: bold'
    # LIGHT ORANGE for Pending
    elif "PENDING" in val_upper:
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    # RED for Rejected
    elif "REJECTED" in val_upper:
        return 'background-color: red; color: white; font-weight: bold'
    return ''

# Database Initialization
if not os.path.exists(DB_FILE):
    cols = ["Request ID", "Project", "Part Number", "Description", "BOM", "UOM", "Supplier", "Price", "Remarks", "HOD Approval", "HOD Comments", "GM Approval", "GM Comments", "Status", "Timestamp", "Raised By"]
    pd.DataFrame(columns=cols).to_csv(DB_FILE, index=False)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None

# --- 2. LOGIN UI (Split Screen) ---
if not st.session_state.auth:
    login_col, img_col = st.columns([1, 2])
    with login_col:
        st.markdown("# 🏗️ procurement \n### Approval Portal")
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

# --- 3. HELPER FUNCTIONS ---
def get_data(): return pd.read_csv(DB_FILE)
def save_data(df): df.to_csv(DB_FILE, index=False)

# --- 4. NAVIGATION ---
st.sidebar.title(f"👤 {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False; st.session_state.user = None; st.rerun()

if st.session_state.user in ["BOMTEAM", "NONBOMTEAM"]:
    menu = st.sidebar.radio("Menu", ["Data Entry", "Status Board"])
elif st.session_state.user == "HOD":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "Dashboard", "Audit Logs"])
elif st.session_state.user == "GM":
    menu = st.sidebar.radio("Menu", ["BOM Team Requests", "Dashboard", "Audit Logs"])

# --- 5. DATA ENTRY ---
if menu == "Initiate the Price approval":
    st.header(f"New Price Request - {st.session_state.user}")
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            proj, part = st.text_input("Project"), st.text_input("Part Number")
            desc = st.text_area("Description")
        with c2:
            bom = st.number_input("BOM", min_value=0)
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

# --- 6. APPROVAL PANEL ---
elif menu == "BOM Team-Requests":
    role = st.session_state.user
    st.header(f"{role} Approval Panel")
    df = get_data()
    target_status = "Pending HOD" if role == "HOD" else "Pending GM"
    pending = df[df["Status"] == target_status]
    
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

# --- 7. STYLED DASHBOARD ---
elif menu in ["Audit Logs", "Dashboard", "Status Board"]:
    st.header("📊 Price approved Transaction records/Audit History")
    df = get_data()
    
    # Apply colors to ALL three relevant columns
    styled_df = df.style.applymap(apply_color_logic, subset=['HOD Approval', 'GM Approval', 'Status'])
    
    st.dataframe(styled_df, use_container_width=True, height=600)
