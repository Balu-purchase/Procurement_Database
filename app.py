import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resolute Admin Portal", layout="wide", page_icon="🚀")

# --- INITIALIZE DATABASE (Session State) ---
if "bom_data" not in st.session_state:
    st.session_state.bom_data = []
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []
if "daily_data" not in st.session_state:
    st.session_state.daily_data = []

# --- HELPER FUNCTIONS ---
def add_audit_log(action, details):
    log = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": "ADMIN_OVERRIDE",
        "Action": action,
        "Details": details
    }
    st.session_state.audit_logs.append(log)

# ---------------- SIDEBAR NAVIGATION ---------------- #
with st.sidebar:
    st.title("Resolute Admin")
    st.markdown("---")
    
    menu = st.radio(
        "SELECT MODULE",
        ["📊 Dashboard", "💻 BOM Team", "📦 Non-BOM Team", "📜 Audit Logs"],
        index=0
    )
    
    st.markdown("---")
    # Export Data Feature
    if st.button("📥 Export Database to CSV"):
        if st.session_state.bom_data:
            df_export = pd.DataFrame(st.session_state.bom_data)
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button("Click to Download", csv, "procurement_data.csv", "text/csv")
        else:
            st.warning("No data to export.")

    if st.button("🔴 System Logout"):
        st.session_state.clear()
        st.rerun()

# ---------------- MODULE 1: DASHBOARD ---------------- #
if menu == "📊 Dashboard":
    st.header("Executive Procurement Dashboard")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total BOMs", len(st.session_state.bom_data))
    col2.metric("Daily Logs", len(st.session_
