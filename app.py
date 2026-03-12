import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Setup
st.set_page_config(page_title="Resolute Admin Portal", layout="wide")

# 2. Data Storage
if "bom_data" not in st.session_state:
    st.session_state.bom_data = []
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []
if "daily_data" not in st.session_state:
    st.session_state.daily_data = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 3. Login Page Logic
if not st.session_state.authenticated:
    st.title("🔐 Resolute Admin Login")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # You can change these credentials as needed
        if user == "ADMIN" and password == "RESOLUTE123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")
    st.stop() # Stops the rest of the app from running until logged in

# 4. Global Audit Function
def log_act(action):
    st.session_state.audit_logs.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Action": action
    })

# 5. Sidebar Navigation & Logout
st.sidebar.title("Resolute Admin")
menu = st.sidebar.radio("Menu", ["Dashboard", "BOM", "Non-BOM", "Logs"])

st.sidebar.markdown("---")
# This button clears auth and sends you back to the login page
if st.sidebar.button("🔴 Logout"):
    st.session_state.authenticated = False
    # Optional: Clear data on logout? If not, remove the line below
    # st.session_state.bom_data = [] 
    st.rerun()

# 6. Dashboard Module
if menu == "Dashboard":
    st.header("Admin Dashboard")
    k1, k2, k3 = st.columns(3)
    k1.metric("BOM Count", len(st.session_state.bom_data))
    k2.metric("Daily Logs", len(st.session_state.daily_data))
    k3.metric("Audit Logs", len(st.session_state.audit_logs))
    
    if st.session_state.bom_data:
        df_b = pd.DataFrame(st.session_state.bom_data)
        st.line_chart(df_b['Price'])

# 7. BOM Module
elif menu == "BOM":
    st.header("BOM Entry")
    with st.form("f1", clear_on_submit=True):
        v = st.text_input("Vendor")
        p = st.text_input("Part
