import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="BOM", layout="wide")

# 2. CONFIG (Short Keys)
H_N = "Bixapathi"
H_D = "Head of Department (HOD)"
T_C = "HOD APPROVAL"
V_C = "VENDOR NAME"
P_C = "PART NUMBER"
R_C = "PRICE"
S_C = "BOM STATUS"

# 3. USERS
DB = {
    "hod_office": {"p": "HOD789", "r": "HOD"},
    "bom_team": {"p": "BOM2026", "r": "BOM"}
}

# 4. SESSION
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u" not in st.session_state:
    st.session_state.u = {}

# 5. LOGIN
if not st.session_state.auth:
    st.sidebar.title("BOM LOGIN")
    uid = st.sidebar.text_input("ID")
    upw = st.sidebar.text_input("PW", type="password")
    if st.sidebar.button("IN"):
        if uid in DB and DB[uid]["p"] == upw:
            st.session_state.auth = True
            st.session_state.u = DB[uid]
            st.rerun()
    st.stop()

# 6. STYLE
st.markdown("<style>.card { background: white; padding: 12px; border-left: 10px solid #1e40af; margin-bottom: 10px; border-radius: 5px; box-shadow: 1px 1px 3px rgba(0,0,0,0.1); } .sig { font-family: 'Brush Script MT', cursive; font-size: 22px; color: #1e40af; }</style>", unsafe_allow_html=True)

# 7. DATA
@st.cache_data(ttl=2)
def load():
    s = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    g = "466678125"
    b = "https://docs.google.com/spreadsheets/d/"
    u_url = b + s + "/export?format=csv&gid=" + g
    try:
        df = pd.read_csv(u_url)
        df.columns = df.columns.str.strip().str.upper()
        return df
    except:
        return pd.DataFrame()

df = load()
u_r = st.session_state.u.get("r", "")

# 8. NAV
m = st.sidebar.radio("NAV", ["APPROVALS", "AUDIT LOG"])
if st.sidebar.button("LOGOUT"):
    st.session_state.auth = False
    st.rerun()

# 9. DASHBOARD
if m == "APPROVALS":
    st.header("PRICE APPROVALS FOR BOM ITEMS")
    if not df.empty:
        if u_r == "HOD":
            st.subheader("PENDING APPROVAL TABLE")
            if T_C in df.columns:
                p_df = df[df[T_C].isna()]
                if p_df.empty:
                    st.success("All Processed")
                else:
                    c1,c2,c3,c4,c5,c6 = st.columns([2,2,1,1,2,1])
                    c1.write("VENDOR")
                    c2.write("PART NO")
                    c3.write("PRICE")
                    c4.write("STATUS")
                    c5.write("COMMENT")
                    c6.write("ACTION")
                    for i, r in p_df.iterrows():
                        x1,x2,x3,x4,x
