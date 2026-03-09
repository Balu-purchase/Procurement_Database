import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="BOM Price Approval", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "hod_office": {
        "pass": "HOD789", "role": "HOD", 
        "name": "Bixapathi", "desig": "Head of Department (HOD)"
    },
    "bom_team": {
        "pass": "BOM2026", "role": "BOM", 
        "name": "BOM Team", "desig": "Executive"
    }
}

# 3. INITIALIZE SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u_info" not in st.session_state:
    st.session_state.u_info = {}

# 4. ACCESS CONTROL
if not st.session_state.auth:
    st.sidebar.title("🔐 LOGIN")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN"):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[u_id]
            st.rerun()
        else:
            st.sidebar.error("Invalid ID/Password")
    st.stop()

# 5. STYLING
st.markdown("<style>.audit-card { background: white; padding: 20px; border-radius: 10px; border-left: 8px solid #1e40af; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; } .sig-font { font-family: 'Brush Script MT', cursive; font-size: 26px; color: #1e40af; } h1 { text-align: center; color: #1e40af; font-weight: bold; }</style>", unsafe_allow_html=True)

# 6. DATA LOADING (GID 466678125)
@st.cache_data(ttl=5)
def load_data():
    sid = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    gid = "466678125" 
    url = "https://docs.google.com/spreadsheets/d/" + sid + "/export?format=csv&gid=" + gid
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip().str.upper()
        return data
    except:
        return pd.DataFrame()

df = load_data()
u = st.session_state.u_info

# 7. NAVIGATION
menu = st.sidebar.radio("NAVIGATE", ["🏠 APPROVALS", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 8. PRICE APPROVALS FOR BOM ITEMS
if menu == "🏠 APPROVALS":
    st.markdown("<h1>🏭 PRICE APPROVALS FOR BOM ITEMS</h1>", unsafe_allow_html=True)
    
    if not df.empty:
        role = u.get('role')
        if role == "HOD":
            st.subheader("📝 PENDING HOD REVIEW")
            col = "HOD APPROVAL"
            if col in df.columns:
                # Filter for rows where HOD column is empty
                mask = df[col].isna() | (df[col].astype(str).str.strip() == "")
                pending = df[mask]
                
                if pending.empty:
                    st.success("🎉 All items have been reviewed!")
                else:
                    for i, r in pending.iterrows():
                        v_name = str(r.get('VENDOR NAME', 'N/A'))
                        with st.expander("Review: " + v_name):
                            st.write("**Price:** " + str(r.get('PRICE', '0')))
                            comment = st.text_input("HOD Comment", key="c_"+str(i))
                            if st.button("SUBMIT", key="b_"+str(i)):
                                if comment.upper() == "APPROVED":
                                    st.success("Record signed by Bixapathi.")
                                else:
                                    st.info("Comment noted: " + comment)
            else:
                st.warning("Column 'HOD APPROVAL' not found in Sheet.")
        
        st.divider()
        st.write("### CURRENT BOM DATABASE")
        st.dataframe(df, use_container_width=True, hide_
