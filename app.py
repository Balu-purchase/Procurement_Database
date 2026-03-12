import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resolute Admin Portal", layout="wide")

# --- INITIALIZE SESSION STATE ---
if "bom_data" not in st.session_state:
    st.session_state.bom_data = []
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []
if "daily_data" not in st.session_state:
    st.session_state.daily_data = []

# --- AUDIT LOG FUNCTION ---
def add_audit_log(action, details):
    log = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": "ADMIN",
        "Action": action,
        "Details": details
    }
    st.session_state.audit_logs.append(log)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Resolute Admin")
    menu = st.radio("SELECT MODULE", ["Dashboard", "BOM Team", "Non-BOM Team", "Audit Logs"])
    st.markdown("---")
    if st.button("Clear All Data"):
        st.session_state.clear()
        st.rerun()

# --- DASHBOARD ---
if menu == "Dashboard":
    st.header("Executive Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("BOM Requests", len(st.session_state.bom_data))
    c2.metric("Daily Logs", len(st.session_state.daily_data))
    c3.metric("Audit Actions", len(st.session_state.audit_logs))
    
    if st.session_state.bom_data:
        df = pd.DataFrame(st.session_state.bom_data)
        st.subheader("Price Overview")
        st.line_chart(df['Price'])

# --- BOM TEAM ---
elif menu == "BOM Team":
    st.
