import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resolute Admin Portal", layout="wide", page_icon="🚀")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e9ecef; }
    </style>
    """, unsafe_allow_html=True)

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
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/Logo_placeholder.png", width=120)
    st.title("Control Center")
    st.markdown("---")
    
    # Native Streamlit navigation (No extra modules needed)
    menu = st.radio(
        "SELECT MODULE",
        ["📊 Dashboard", "💻 BOM Team", "📦 Non-BOM Team", "📜 Audit Logs"],
        index=0
    )
    
    st.markdown("---")
    if st.button("🔴 System Logout"):
        st.session_state.clear()
        st.rerun()

# ---------------- MODULE 1: DASHBOARD ---------------- #
if menu == "📊 Dashboard":
    st.header("Executive Procurement Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total BOMs", len(st.session_state.bom_data))
    with col2:
        st.metric("Daily Logs", len(st.session_state.daily_data))
    with col3:
        st.metric("System Actions", len(st.session_state.audit_logs))
    with col4:
        st.metric("Access Level", "Full Admin")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("BOM Price Analysis")
        if st.session_state.bom_data:
            df_bom = pd.DataFrame(st.session_state.bom_data)
            st.area_chart(df_bom.set_index('Date')['Price'])
        else:
            st.info("No BOM data to visualize.")
            
    with c2:
        st.subheader("Recent Audit History")
        if st.session_
