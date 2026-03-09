import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="BOM Price", layout="wide")

# 2. CONFIG (SHORT NAMES TO PREVENT CUT-OFF)
H_NAME = "Bixapathi"
H_DSG = "Head of Department (HOD)"
B_DSG = "BOM Executive"
T_COL = "HOD APPROVAL"

# 3. USER DATABASE
USER_DB = {
    "hod_office": {"pass": "HOD789", "role": "HOD", "name": H_NAME, "dsg": H_DSG},
    "bom_team": {"pass": "BOM2026", "role": "BOM", "name": "BOM Team", "dsg": B_DSG}
}

# 4. SESSION INITIALIZE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u_info" not in st.session_state:
    st.session_state.u_info = {}

# 5. ACCESS CONTROL
if not st.session_state.auth:
    st.sidebar.title("🔐 BOM LOGIN ONLY")
    uid = st.sidebar.text_input("USER ID")
    upw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN"):
        if uid in USER_DB and USER_DB[uid]["pass"] == upw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[uid]
            st.rerun()
        else:
            st.sidebar.error("DENIED: NOT BOM")
    st.stop()

# 6. STYLE
st.markdown("<style>.audit-card { background: white; padding: 15px; border-left: 8px solid #1e40af; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); } .sig { font-family: 'Brush Script MT', cursive; font-size: 24px; color: #1e40af; }</style>", unsafe_allow_html=True)

# 7. DATA (GID 466678125)
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

# 8. NAVIGATION
menu = st.sidebar.radio("NAV", ["🏠 APPROVALS", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 9. DASHBOARD
if menu == "🏠 APPROVALS":
    st.header("🏭 PRICE APPROVALS FOR BOM ITEMS")
    if not df.empty:
        if u["role"] == "HOD":
            st.subheader("📝 PENDING HOD REVIEW")
            if T_COL in df.columns:
                pend = df[df[T_COL].isna()]
                for i, r in pend.iterrows():
                    v = str(r.get('VENDOR NAME', 'N/A'))
                    with st.expander("Review: " + v):
                        st.write("Price: " + str(r.get('PRICE', '0')))
                        txt = st.text_input("Comment", key="c"+str(i))
                        if st.button("SUBMIT", key="b"+str(i)):
                            if txt.upper() == "APPROVED":
                                st.success("Signed by " + H_NAME)
        else:
            st.info("BOM VIEW: Waiting for HOD.")
        st.divider()
        st.dataframe(df, use_container_width=True)

# 10. AUDIT LOG (BI
