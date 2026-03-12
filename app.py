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

# 3. Sidebar Navigation
st.sidebar.title("Resolute Admin")
menu = st.sidebar.radio("Menu", ["Dashboard", "BOM", "Non-BOM", "Logs"])

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
            st.session_state
