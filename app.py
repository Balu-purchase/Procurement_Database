import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Audit Portal", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "hod_office": {"pass": "HOD789", "role": "HOD", "name": "Bixapathi", "desig": "Head of Department (HOD)"},
    "bom_team": {"pass": "BOM2026", "role": "BOM", "name": "BOM Team", "desig": "Executive"}
}

# 3. INITIALIZE SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u_info" not in st.session_state:
    st.session_state.u_info = {}

# 4. PROFESSIONAL STYLING
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .audit-card { 
        background: white; padding: 25px; border-radius: 12px; 
        border-left: 10px solid #1e40af; box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        margin-bottom: 20px;
    }
    .sig-font { font-family: 'Brush Script MT', cursive; font-size: 28px; color: #1e40af; }
    h1 { text-align: center; color: #0f172a; font-weight: 800; border-bottom: 2px solid #1e40af; padding-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 5. ACCESS CONTROL GATEKEEPER
if not st.session_state.auth:
    st.sidebar.title("🔐 ACCESS CONTROL")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN", use_container_width=True):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[u_id]
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid ID or Password")
    
    st.markdown("<h1>🏭 PROCUREMENT AUDIT SYSTEM</h1>", unsafe_allow_html=True)
    st.info("Please enter your credentials in the sidebar to access protected files.")
    st.stop()

# --- THE FOLLOWING CODE ONLY RUNS AFTER LOGIN ---

# 6. NAVIGATION & LOGOUT
st.sidebar.success(f"Logged in: {st.session_state.u_info.get('name')}")
menu = st.sidebar.radio("NAVIGATE", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 7. FAIL-SAFE DATA LOADING
@st.cache_data(ttl=30)
def load_data():
    # URL is joined to prevent line-break syntax errors
    base = "https://docs.google.com/spreadsheets/d/"
    key = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    suffix = "/export?format=csv&gid=2061093150"
    sheet_url = f"{base}{key}{suffix}"
    
    try:
        data = pd.read_csv(sheet_url)
        data.columns = data.columns.str.strip()
        return data
    except Exception:
        return pd.DataFrame()

df = load_data()
u = st.session_state.u_info

# 8. DASHBOARD VIEW
if menu == "🏠 DASHBOARD":
    st.markdown(f"<h1>🏭 {u.get('role')} CONTROL CENTER</h1>", unsafe_allow_html=True)
    
    if not df.empty:
        if u.get('role') == "HOD":
            st.subheader("🔔 PENDING HOD APPROVALS")
            # Logic: Show rows where 'HOD APPROVAL' column is empty
            if 'HOD APPROVAL' in df.columns:
                pending = df[df['HOD APPROVAL'].fillna('').eq('')]
                if not pending.empty:
                    for i, r in pending.iterrows():
                        with st.expander(f"Review: {r.get('VENDOR NAME')} | {r.get('PART NUMBER')}"):
                            st.write(f"**Price
