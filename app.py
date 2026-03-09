import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Audit Portal", layout="wide")

# 2. USER DB & STYLING
USER_DB = {
    "hod_office": {"pass": "HOD789", "role": "HOD", "name": "Bixapathi", "desig": "Head of Department (HOD)"},
    "bom_team": {"pass": "BOM2026", "role": "BOM", "name": "BOM Executive", "desig": "Data Entry"}
}

st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .report-card { 
        background: white; padding: 20px; border-radius: 10px; 
        border-left: 8px solid #1e40af; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px;
    }
    .sig { font-family: 'cursive'; font-size: 22px; color: #1e40af; font-weight: bold; }
    h1 { text-align: center; color: #0f172a; border-bottom: 2px solid #1e40af; }
</style>
""", unsafe_allow_html=True)

# 3. AUTHENTICATION
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.sidebar.title("🔐 LOGIN")
    u, p = st.sidebar.text_input("ID"), st.sidebar.text_input("PASS", type="password")
    if st.sidebar.button("SIGN IN"):
        if u in USER_DB and USER_DB[u]["pass"] == p:
            st.session_state.auth, st.session_state.user = True, USER_DB[u]
            st.rerun()
    st.stop()

# 4. NAVIGATION
menu = st.sidebar.radio("MENU", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 5. DATA LOADING (Fail-Safe)
def load_data():
    # Ensure Google Sheet is "Public - Anyone with link can view"
    url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv&gid=2061093150"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        st.error("Sheet Connection Error")
        return pd.DataFrame()

# 6. APP LOGIC
df = load_data()

if menu == "🏠 DASHBOARD":
    st.markdown(f"<h1>🏭 {st.session_state.user['role']} VIEW</h1>", unsafe_allow_html=True)
    if not df.empty:
        if st.session_state.user['
