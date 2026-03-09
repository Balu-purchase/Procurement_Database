import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="BOM Price", layout="wide")

# 2. USER DATABASE (STRICT ACCESS)
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
        "desig": "BOM Executive"
    }
}

# 3. INITIALIZE SESSION
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u_info" not in st.session_state:
    st.session_state.u_info = {}

# 4. LOGIN GUARD (BLOCKS NON-BOM USERS)
if not st.session_state.auth:
    st.sidebar.title("🔐 BOM ACCESS ONLY")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN"):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[u_id]
            st.rerun()
        else:
            st.sidebar.error("ACCESS DENIED: NOT A BOM USER")
    st.stop()

# 5. STYLING
css = """<style>
    .audit-card { background: white; padding: 15px; 
    border-left: 8px solid #1e40af; margin-bottom: 10px; 
    border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .sig { font-family: 'Brush Script MT', cursive; 
    font-size: 24px; color: #1e40af; }
</style>"""
st.markdown(css, unsafe_allow_html=True)

# 6. DATA LOADING (GID 466678125)
@st.cache_data(ttl=5)
def load_data():
    s_id = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    g_id = "466678125"
    base = "https://docs.google.com/spreadsheets/d/"
    url = base + s_id + "/export?format=csv&gid=" + g_id
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

# 8. PRICE APPROVALS (HOD ONLY ACTION)
if menu == "🏠 APPROVALS":
    st.header("🏭 PRICE APPROVALS FOR BOM ITEMS")
    
    if not df.empty:
        # ONLY Bixapathi (HOD) can see the comment/approval section
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
                        txt = st.text_input("Comment", key="c"+str(i))
                        if st.button("SUBMIT", key="b"+str(i)):
                            if txt.upper() == "APPROVED":
                                st.success("Verified by Bixapathi")
            else:
                st.info("HOD APPROVAL column missing in sheet.")
        
        # BOM LOGINS see the full list but NO comment boxes
        else:
            st.info("BOM TEAM VIEW: Approvals Pending HOD Review.")

        st.divider()
        st.dataframe(df, use_container_width=True)

# 9. AUDIT LOG (RESTRICTED TO APPROVED ITEMS)
else:
    st.header("📜 OFFICIAL AUDIT LOG")
    col = "HOD APPROVAL"
    if not df.empty and col in df.columns:
        mask = df[col].astype(str).str.upper() == "APPROVED"
        appr = df[mask]
        for _, r in appr.iterrows():
            v_name = str(r.get('VENDOR NAME'))
            ts = datetime.now().strftime('%Y-%m-%d %H:%M')
            u_name = "Bixapathi" # Signature belongs to HOD
            u_dsg =
