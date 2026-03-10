import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Initialize all session keys
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
    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("GO TO", ["BOM", "NONBOM", "AUDIT LOGS"])
    else: menu = "MAIN"

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.title("Factory Procurement Dashboard")
    st.divider()

    # --- BOM TEAM MODULE ---
    if st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team: Manual Entry")
        with st.container(border=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            proj, pnum, desc, qps = r1c1.text_input("PROJECT"), r1c2.text_input("PART NUMBER"), r1c3.text_input("DESCRIPTION"), r1c4.text_input("QPS")
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            uom, supp, price, opt_supp = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Ltr"]), r2c2.text_input("SUPPLIER NAME"), r2c3.text_input("PRICE"), r2c4.text_input("OPTIONAL SUPPLIER")
            if st.button("SUBMIT REQUEST", type="primary"):
                st.session_state.master_data.append({"PROJECT": proj, "PARTNUMBER": pnum, "DESCRIPTION": desc, "QPS": qps, "UOM": uom, "SUPPLIER": supp, "PRICE": price, "OPT_SUPP": opt_supp, "HOD APPROVAL": "", "GM APPROVAL": "", "STATUS": "PENDING", "REMARKS": ""})
                st.success("Submitted to HOD!"); st.rerun()

        st.subheader("📋 PRICE APPROVAL REQUEST STATUS")
        if st.session_state.master_data:
            df = pd.DataFrame(st.session_state.master_data)
            st.dataframe(df.style.applymap(style_status, subset=['STATUS']), use_container_width=True)

    # --- NON-BOM TEAM MODULE ---
    elif st.session_state.role == "NONBOMTEAM":
        tab1, tab2, tab3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS"])
        
        with tab1:
            st.subheader("DAILY TRACKER (PR TO PO)")
            with st.form("dt_form", clear_on_submit=True):
                c1, c2, c3, c4 = st.columns(4)
                dt_date, dt_plant = c1.date_input("DATE"), c2.text_input("PLANT")
                dt_pr,
