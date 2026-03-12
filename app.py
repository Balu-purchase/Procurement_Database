import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Config
st.set_page_config(page_title="Resolute Admin", layout="wide")

# 2. State
if "bom" not in st.session_state: st.session_state.bom = []
if "log" not in st.session_state: st.session_state.log = []
if "auth" not in st.session_state: st.session_state.auth = False

# 3. Login
if not st.session_state.auth:
    st.title("Login")
    u = st.text_input("User")
    p = st.text_input("Pass", type="password")
    if st.button("Login"):
        if u == "ADMIN" and p == "RE123":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Wrong")
    st.stop()

# 4. Sidebar
st.sidebar.title("Admin")
m = st.sidebar.radio("Go to", ["Dash", "BOM", "Logs"])
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# 5. Dashboard
if m == "Dash":
    st.header("Dashboard")
    st.metric("Total Items", len(st.session_state.bom))
    if st.session_state.bom:
        df = pd.DataFrame(st.session_state.bom)
        st.line_chart(df['Price'])

# 6. BOM Entry
elif m == "BOM":
    st.header("BOM Entry")
    with st.form("f"):
        vend = st.text_input("Vendor")
        part = st.text_input("Part")
        cost = st.number_input("Price", min_value=0.0)
        if st.form_submit_button("Save"):
            st.session_state.bom.append({"Vendor":vend,"Part":part,"Price":cost})
            st.session_state.log.append(f"Added {part}")
            st.success("Saved")
            st.rerun()
    if st.session_state.bom:
        st.write(pd.DataFrame(st.session_state.bom))

# 7. Logs
elif m == "Logs":
    st.header("Logs")
    st.write(st.session_state.log)
