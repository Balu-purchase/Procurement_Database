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

# 4. STYLING
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

# 5. ACCESS CONTROL
if not st.session_state.auth:
    st.sidebar.title("🔐 ACCESS CONTROL")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN", use_container_width=True):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[u_id]
            st.rerun()
    st.stop()

# 6. NAVIGATION
menu = st.sidebar.radio("NAVIGATE", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 7. DATA LOADING
@st.cache_data(ttl=30)
def load_data():
    base = "https://docs.google.com/spreadsheets/d/"
    key = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    suffix = "/export?format=csv&gid=2061093150"
    try:
        data = pd.read_csv(f"{base}{key}{suffix}")
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame()

df = load_data()
u = st.session_state.u_info

# 8. DASHBOARD VIEW
if menu == "🏠 DASHBOARD":
    st.markdown(f"<h1>🏭 {u.get('role')} CONTROL CENTER</h1>", unsafe_allow_html=True)
    if not df.empty:
        if u.get('role') == "HOD":
            st.subheader("🔔 PENDING HOD APPROVALS")
            # Filter rows where HOD APPROVAL column is empty
            if 'HOD APPROVAL' in df.columns:
                pending = df[df['HOD APPROVAL'].fillna('').eq('')]
                for i, r in pending.iterrows():
                    v_name = r.get('VENDOR NAME', 'N/A')
                    p_num = r.get('PART NUMBER', 'N/A')
                    price_val = r.get('PRICE', '0')
                    with st.expander(f"Review: {v_name} | {p_num}"):
                        st.write(f"**Price:** {price_val}")
                        if st.button(f"APPROVE S.NO {r.get('S.NO')}", key=f"btn_{
