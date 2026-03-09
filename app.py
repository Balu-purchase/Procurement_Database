import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Audit Portal", layout="wide")

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

# 3. PROFESSIONAL STYLING
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .audit-card { 
        background: white; padding: 25px; border-radius: 12px; 
        border-left: 10px solid #1e40af; box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        margin-bottom: 20px;
    }
    .sig-font { font-family: 'Brush Script MT', cursive; font-size: 28px; color: #1e40af; }
    h1 { text-align: center; color: #0f172a; font-weight: 800; border-bottom: 2px solid #1e40af; }
</style>
""", unsafe_allow_html=True)

# 4. INITIALIZE SESSION STATE (Prevents AttributeError)
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = None

# 5. SIDEBAR LOGIN
st.sidebar.title("🔐 ACCESS CONTROL")

if not st.session_state.auth:
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN", use_container_width=True):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.user = USER_DB[u_id]
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid ID or Password")
    st.warning("Please log in to access the system.")
    st.stop() # Force stop here so code below doesn't run without a user

# 6. NAVIGATION & LOGOUT (Only reachable if auth is True)
menu = st.sidebar.radio("NAVIGATE", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.session_state.user = None
    st.rerun()

# 7. DATA LOADING
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv&gid=2061093150"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

# 8. DASHBOARD VIEW
if menu == "🏠 DASHBOARD":
    # Safe access to session_state.user
    role = st.session_state.user['role']
    st.markdown(
