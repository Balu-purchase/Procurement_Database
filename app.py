import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Factory Approval System", layout="wide")

# --- 2. INTERNAL STORAGE (The "Website Database") ---
# This initializes empty lists to store data if they don't exist yet
if "bom_db" not in st.session_state:
    st.session_state.bom_db = []
if "non_bom_db" not in st.session_state:
    st.session_state.non_bom_db = []

# --- 3. LOGIN SYSTEM ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Factory Portal Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("LOG IN"):
        # Login Credentials
        db = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
        if user in db and db[user] == pw:
            st.session_state.auth = True
            st.session_state.role = user
            st.rerun()
        else:
            st.error("Invalid Username or Password")
    st.stop()

# --- 4. NAVIGATION & LOGOUT ---
role = st.session_state.role
st.sidebar.title(f"Welcome, {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 5. NONBOM TEAM LOGIN ---
if role == "NONBOMTEAM":
    st.header("📋 NON-BOM Daily Activity")
    with st.form("nb_form", clear_on_submit=True):
        activity = st.text_area("Daily Activity Description")
        requested = st.number_input("Items Purchased/Requested Today", min_value=0)
        if st.form_submit_button("Submit Entry"):
            entry = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Activity": activity,
                "Qty": requested,
                "HOD_Comment": "Waiting..."
            }
            st.session_state.non_bom_db.append(entry)
            st.success("Activity submitted to HOD.")

# --- 6. BOM TEAM LOGIN ---
elif role == "BOMTEAM":
    st.header("📦 BOM Price Approval Request")
    with st.form("bom_form", clear_on_submit=True):
        part = st.text_input("Part Number / Item Name")
        vendor = st.text_input("Vendor Name")
        price = st.text_input("Quoted Price")
        if st.form_submit_button("Request Approval"):
            entry = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Part": part,
                "Vendor": vendor,
                "Price": price,
                "Status": "PENDING",
                "HOD_Remarks": ""
            }
            st.session_state.bom_db.append(entry)
            st.success("Price request sent to HOD.")

# --- 7. HOD LOGIN (THE COMMAND CENTER) ---
elif role == "HOD":
    st.title("👨‍💼 HOD CONTROL PANEL")
    
    # Navigation Icons
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("📊 NON-BOM ACTIVITY", use_container_width=True):
            st.session_state.hod_view = "NONBOM"
    with c2:
        if st.button("📦 BOM APPROVALS", use_container_width=True):
            st.session_state.hod_view = "BOM"
    with c3:
        if st.button("📜 AUDIT LOGS", use_container_width=True):
            st.session_state.hod_view = "AUDIT"

    # HOD VIEW LOGIC
    view = st.session_state.get("hod_view", "NONBOM")

    if view == "NONBOM":
        st.subheader("Daily Activity Reports")
        if not st.session_state.non_bom_db:
            st.info("No reports yet.")
        else:
            for i, item in enumerate(st.session_state.non_bom_db):
                with st.expander(f"Report: {item['Date']}"):
                    st.write(f"**Activity:** {item['Activity']}")
                    st.write(f"**Qty:** {item['Qty']}")
                    new_com = st.text_input("HOD Comment", key=f"nb_{i}")
                    if st.button("Save Comment", key=f"btn_nb_{i}"):
                        st.session_state.non_bom_db[i]['HOD_Comment'] = new_com
                        st.rerun()

    elif view == "BOM":
        st.subheader("Pending Price Approvals")
        # Show only items that are PENDING
        pending_bom = [i for i in st.session_state.bom_db if i['Status'] == "PENDING"]
        if not pending_bom:
            st.success("All prices approved!")
        else:
            for i, item in enumerate(st.session_state.bom_db):
                if item['Status'] == "PENDING":
                    with st.container(border=True):
                        st.write(f"**Part:** {item['Part']} | **Price:** {item['Price']} | **Vendor:** {item['Vendor']}")
                        rem = st.text_input("Remarks", key=f"rem_{i}")
                        col_a, col_r = st.columns(2)
                        if col_a.button("✅ APPROVE", key=f"app_{i}"):
                            st.session_state.bom_db[i]['Status'] = "APPROVED"
                            st.session_state.bom_db[i]['HOD_Remarks'] = rem
                            st.rerun()
                        if col_r.button("❌ REJECT", key=f"rej_{i}"):
                            st.session_state.bom_db[i]['Status'] = "REJECTED"
                            st.session_state.bom_db[i]['HOD_Remarks'] = rem
                            st.rerun()

    elif view == "AUDIT":
        st.subheader("📜 Price Approval Audit Logs")
        st.write("Record of all Approved and Rejected BOM prices.")
        # Show only items that are NOT pending
        audit_data = [i for i in st.session_state.bom_db if i['Status'] != "PENDING"]
        if audit_data:
            st.table(pd.DataFrame(audit_data))
        else:
            st.warning("No audit records found yet.")
