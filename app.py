import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Persistent storage for all modules
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "master_data" not in st.session_state:
    st.session_state.master_data = []
if "daily_tracker" not in st.session_state:
    st.session_state.daily_tracker = []
if "advance_payments" not in st.session_state:
    st.session_state.advance_payments = []
if "mis_data" not in st.session_state:
    st.session_state.mis_data = []
if "nb_choice" not in st.session_state:
    st.session_state.nb_choice = "DAILY"

# --- Helper Functions for Styling ---
def style_status(val):
    if val in ["APPROVED", "CLOSED", "DONE", "RECEIVED"]: 
        return 'background-color: green; color: white; font-weight: bold'
    if val in ["REJECTED", "PENDING"]: 
        return 'background-color: red; color: white; font-weight: bold'
    if val == "OPEN": 
        return 'background-color: orange; color: black; font-weight: bold'
    return ''

def style_payment_table(df):
    """Applies specific colors for Advance Payment Tracker"""
    def apply_colors(x):
        color = ''
        if x in ["DONE", "RECEIVED", "ACCOUNTED"]: color = 'background-color: green; color: white'
        elif x == "PENDING": color = 'background-color: yellow; color: black'
        return color
    return df.style.applymap(apply_colors)

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://t3.ftcdn.net/jpg/09/94/98/98/360_F_994989868_JVms41RbTVCoI1wmY7JOwTGG3CsGQ8wr.webp");
        background-size: cover; background-position: center;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.9); border-radius: 10px; padding: 20px;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    _, col_login = st.columns([1.8, 1])
    with col_login:
        st.write("###")
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #333;'>SYSTEM LOGIN</h2>", unsafe_allow_html=True)
            uid = st.text_input("Username").strip().upper() 
            upw = st.text_input("Password", type="password")
            if st.button("ENTER SYSTEM", use_container_width=True):
                creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789", "GM_OFFICE": "GM2026"}
                if uid in creds and creds[uid] == upw:
                    st.session_state.auth = True
                    st.session_state.role = uid
                    st.rerun() 
                else: st.error("Invalid Credentials.")

# --- 3. DASHBOARD PAGE ---
else:
    st.sidebar.title(f"👤 {st.session_state.role}")
    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("GO TO", ["BOM", "NONBOM", "AUDIT LOGS"])
    else: menu = "MAIN"

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.title("Factory Procurement Dashboard")
    st.divider()

    # --- BOM TEAM MODULE
