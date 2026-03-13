import streamlit as st
import pandas as pd
from datetime import datetime

# Optional: Plotly for charts
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Persistent state management
state_keys = {
    "auth": False, "role": None, "master_data": [], 
    "daily_tracker": [], "advance_payments": [], 
    "mis_data": [], "nb_choice": "DAILY" 
}
for key, default in state_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Helper Functions for Styling ---
def style_status(val):
    if val in ["APPROVED", "CLOSED", "DONE", "RECEIVED"]: 
        return 'background-color: green; color: white; font-weight: bold'
    if val in ["REJECTED", "PENDING"]: 
        return 'background-color: red; color: white; font-weight: bold'
    if val == "OPEN": 
        return 'background-color: orange; color: black; font-weight: bold'
    return ''

def apply_payment_colors(val):
    if val in ["DONE", "RECEIVED", "ACCOUNTED"]: 
        return 'background-color: green; color: white'
    elif val == "PENDING": 
        return 'background-color: yellow; color: black'
    return ''

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
    
    # Navigation logic
    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("GO TO", ["BOM", "NONBOM", "AUDIT LOGS"])
    else:
        # Default menu for Team roles so the page isn't blank
        menu = "MAIN"

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.title("Factory Procurement Dashboard")
    st.divider()

    # --- 🟢 NON-BOM TEAM MODULE (FIXED) ---
    if st.session_state.role == "NONBOMTEAM":
        st.header("📦 Non-BOM Activity Management")
        tab1, tab2, tab3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS TRACKER"])
        
        with tab1:
            st.subheader("Daily PR to PO Tracker")
            with st.form("dt_form", clear_on_submit=True):
                c1, c2, c3, c4 = st.columns(4)
                d_date = c1.date_input("DATE")
                d_plant = c2.text_input("PLANT")
                d_pr = c3.number_input("PR RECEIPTS", min_value=0)
                d_po = c4.number_input("PO DONE", min_value=0)
                if st.form_submit_button("SUBMIT ENTRY"):
                    st.session_state.daily_tracker.append({
                        "S.NO": len(st.session_state.daily_tracker)+1, "DATE": str(d_date), 
                        "PLANT": d_plant, "PR RECEIPTS": d_pr, "PO DONE": d_po, 
                        "BALANCE PR'S": d_pr - d_po, "HOD COMMENTS": ""
                    })
                    st.rerun()
