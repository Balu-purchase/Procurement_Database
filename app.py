import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.parse  # For formatting the WhatsApp message

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Resolute Approval System", layout="wide")
DB_FILE = "resolute_db.csv"

# WhatsApp Numbers (Must include Country Code, e.g., 91 for India)
WHATSAPP_NUMBERS = {
    "HOD": "91XXXXXXXXXX",       # Replace with HOD's Phone Number
    "GM": "91XXXXXXXXXX",        # Replace with GM's Phone Number
    "BOMTEAM": "91XXXXXXXXXX"    # Replace with BOM Team Phone Number
}

USERS = {
    "BOMTEAM": "BOM123",
    "NONBOMTEAM": "NONBOM123",
    "HOD": "HOD789",
    "GM": "GM123"
}

# Database Init
if not os.path.exists(DB_FILE):
    cols = ["Request ID", "Project", "Part Number", "Description", "BOM", "UOM", 
            "Supplier", "Price", "Remarks", "HOD Approval", "HOD Comments", 
            "GM Approval", "GM Comments", "Status", "Timestamp", "Raised By"]
    pd.DataFrame(columns=cols).to_csv(DB_FILE, index=False)

# Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None

# --- 2. LOGIN PAGE (LEFT SIDE DESIGN) ---
if not st.session_state.auth:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("RESOLUTE LOGIN")
        u_sel = st.selectbox("Select Role", list(USERS.keys()))
        p_sel = st.text_input("Password", type="password")
        if st.button("SIGN IN", use_container_width=True):
            if p_sel == USERS[u_sel]:
                st.session_state.auth = True
                st.session_state.user = u_sel
                st.rerun()
            else:
                st.error("Incorrect Password")
    with col2:
        st.info("### Price Approval Management System\nWelcome to the official Resolute Electronics Procurement Portal.")
    st.stop()

# --- 3. WHATSAPP HELPER ---
def open_whatsapp(phone, message):
    # This creates a link that opens WhatsApp with a pre-filled message
    encoded_msg = urllib.parse.quote(message)
    link = f"https://wa.me/{phone}?text={encoded_msg}"
    # This displays a link that the user clicks to send the notification
    st.markdown(f"""<a href="{link}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">📲 Send WhatsApp Notification</a>""", unsafe_allow_html=True)

# --- 4. DATA HELPERS ---
def get_data(): return pd.read_csv(DB_FILE)
def save_data(df): df.to_csv(DB_FILE, index=False)

st.sidebar.title(f"👤 {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

menu_options = {
    "BOMTEAM": ["Data Entry", "Status Board"],
    "NONBOMTEAM": ["Data Entry", "Status Board"],
    "HOD": ["BOM Team Requests", "Dashboard", "Audit Logs"],
    "GM": ["BOM Team Requests", "Dashboard", "Audit Logs"]
}
menu = st.sidebar.radio("Navigate", menu_options[st.session_state.user])

# --- 5. DATA ENTRY ---
if menu == "Data Entry":
    st.header("Price Approval Request Form")
    with st.form("entry_form"):
        c1, c2 = st.columns(2)
        with c1:
            proj = st.text_input("Project Name")
            part = st.text_input("Part Number")
        with c2:
            supp = st.text_input("Supplier")
            price = st.number_input("Unit Price", min_value=0.0)
        
        if st.form_submit_button("Save to Database"):
            req_id = f"REQ-{datetime.now().strftime('%y%m%d%H%M')}"
            new_row = {
                "Request ID": req_id, "Project": proj, "Part Number": part, "Description": "-",
                "BOM": 1, "UOM": "Nos", "Supplier": supp, "Price": price, "Remarks": "-",
                "HOD Approval": "Pending", "HOD Comments": "-", "GM Approval": "Pending",
                "GM Comments": "-", "Status": "Pending HOD", "Timestamp": datetime.now(),
                "Raised By": st.session_state.user
            }
            df = get_data()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success(f"Request {req_id} saved!")

    # WHATSAPP TRIGGER BUTTON (Outside form to allow link generation)
    st.subheader("Step 2: Notify HOD")
    last_req = get_data().iloc[-1]
    msg = f"*Price Approval Needed*\n*ID:* {last_req['Request ID']}\n*Project:* {last_req['Project']}\n*Price:* {last_req['Price']}\n*Link:* https://resolute-app.streamlit.app"
    open_whatsapp(WHATSAPP_NUMBERS["HOD"], msg)

# --- 6. HOD / GM APPROVAL (SIMILAR LOGIC) ---
elif menu == "BOM Team Requests":
    st.header("Approval Panel")
    df = get_data()
    # Logic for filtering based on HOD or GM roles
    target_status = "Pending HOD" if st.session_state.user == "HOD" else "Pending GM"
    pending = df[df["Status"] == target_status]
    
    for i, row in pending.iterrows():
        with st.expander(f"Review {row['Request ID']}"):
            dec = st.selectbox("Action", ["Pending", "Approved", "Rejected"], key=f"d{i}")
            if st.button("Save Decision", key=f"b{i}"):
                df.at[i, "Status"] = "Pending GM" if dec == "Approved" and st.session_state.user == "HOD" else "Finalized"
                save_data(df)
                st.success("Decision Saved! Use the button below to notify the next person.")
                
                # Dynamic WhatsApp Link
                next_person = "GM" if st.session_state.user == "HOD" else "BOMTEAM"
                next_msg = f"*Update on {row['Request ID']}*\n*Decision:* {dec}\n*By:* {st.session_state.user}"
                open_whatsapp(WHATSAPP_NUMBERS[next_person], next_msg)

elif menu in ["Audit Logs", "Dashboard", "Status Board"]:
    st.dataframe(get_data())
