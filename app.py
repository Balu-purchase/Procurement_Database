import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="BOM Price", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "hod_office": {
        "pass": "HOD789", 
        "role": "HOD", 
        "name": "Bixapathi", 
        "desig": "Head of Department (HOD)"
    },
    "bom_team": {
        "pass": "BOM2026", 
        "role": "BOM", 
        "name": "BOM Team", 
        "desig": "Executive"
    }
}

# 3. INITIALIZE SESSION
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u_info" not in st.session_state:
    st.session_state.u_info = {}

# 4. LOGIN GUARD
if not st.session_state.auth:
    st.sidebar.title("🔐 LOGIN")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN"):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[u_id]
            st.rerun()
    st.stop()

# 5. STYLING
st.markdown("""
<style>
    .audit-card { 
        background: white; padding: 15px; 
        border-left: 8px solid #1e40af; 
        margin-bottom: 10px; border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sig { 
        font-family: 'Brush Script MT', cursive; 
        font-size: 24px; color: #1e40af; 
    }
</style>
""", unsafe_allow_html=True)

# 6. DATA LOADING (GID 466678125)
@st.cache_data(ttl=5)
def load_data():
    s = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    g = "466678125"
    url = "https://docs.google.com/spreadsheets/d/"
    url += s + "/export?format=csv&gid=" + g
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip().str.upper()
        return data
    except:
        return pd.DataFrame()

df = load_data()
u = st.session_state.u_info

# 7. NAVIGATION
nav = ["🏠 APPROVALS", "🏛️ AUDIT LOG"]
menu = st.sidebar.radio("NAVIGATE", nav)
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 8. PRICE APPROVALS FOR BOM ITEMS
if menu == "🏠 APPROVALS":
    st.header("🏭 PRICE APPROVALS FOR BOM ITEMS")
    if not df.empty:
        if u.get('role') == "HOD":
            st.subheader("📝 PENDING HOD REVIEW")
            col = "HOD APPROVAL"
            if col in df.columns:
                mask = df[col].isna()
                pend = df[mask]
                for i, r in pend.iterrows():
                    v = str(r.get('VENDOR NAME', 'N/A'))
                    with st.expander("Review: " + v):
                        st.write("Price: " + str(r.get('PRICE', '0')))
                        c_key = "c" + str(i)
                        b_key = "b" + str(i)
                        txt = st.text_input("Comment", key=c_key)
                        if st.button("SUBMIT", key=b_key):
                            if txt.upper() == "APPROVED":
                                st.success("Signed by Bixapathi")
            else:
                st.info("HOD APPRO
