import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Setup
st.set_page_config(page_title="Resolute Admin", layout="wide")

# 2. Data Storage
if "bom_data" not in st.session_state:
    st.session_state.bom_data = []
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []
if "daily_data" not in st.session_state:
    st.session_state.daily_data = []

# 3. Sidebar Navigation & Logout
st.sidebar.title("Resolute Admin")
menu = st.sidebar.radio("Menu", ["Dashboard", "BOM", "Non-BOM", "Logs"])

st.sidebar.markdown("---")
if st.sidebar.button("Logout / Reset Session"):
    st.session_state.clear()
    st.rerun()

# 4. Global Audit Function
def log_act(action):
    st.session_state.audit_logs.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Action": action
    })

# 5. Dashboard Module
if menu == "Dashboard":
    st.header("Admin Dashboard")
    k1, k2, k3 = st.columns(3)
    k1.metric("BOM Count", len(st.session_state.bom_data))
    k2.metric("Daily Logs", len(st.session_state.daily_data))
    k3.metric("Audit Logs", len(st.session_state.audit_logs))
    
    if st.session_state.bom_data:
        df_b = pd.DataFrame(st.session_state.bom_data)
        st.line_chart(df_b['Price'])

# 6. BOM Module
elif menu == "BOM":
    st.header("BOM Entry")
    with st.form("f1", clear_on_submit=True):
        v = st.text_input("Vendor")
        p = st.text_input("Part")
        pr = st.number_input("Price", min_value=0.0)
        if st.form_submit_button("Submit"):
            st.session_state.bom_data.append({"Vendor":v, "Part":p, "Price":pr})
            log_act(f"Added BOM: {p}")
            st.rerun()
    if st.session_state.bom_data:
        st.write(pd.DataFrame(st.session_state.bom_data))

# 7. Non-BOM Module
elif menu == "Non-BOM":
    st.header("Non-BOM Tracker")
    with st.form("f2"):
        pl = st.text_input("Plant")
        qty = st.number_input("Qty", step=1)
        if st.form_submit_button("Save"):
            st.session_state.daily_data.append({"Plant":pl, "Qty":qty})
            log_act(f"Non-BOM: {pl}")
            st.rerun()
    if st.session_state.daily_data:
        st.write(pd.DataFrame(st.session_state.daily_data))

# 8. Audit Logs
elif menu == "Logs":
    st.header("System Logs")
    if st.session_state.audit_logs:
        st.write(pd.DataFrame(st.session_state.audit_logs)[::-1])
    else:
        st.info("No logs.")
