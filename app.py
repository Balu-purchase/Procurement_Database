import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="BOM")

# 2. CONFIG
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
if "log_data" not in st.session_state:
    st.session_state.log_data = []

# 5. LOGIN
if not st.session_state.auth:
    st.sidebar.title("BOM LOGIN")
    uid = st.sidebar.text_input("ID")
    upw = st.sidebar.text_input("PW", type="password")
    if st.sidebar.button("IN"):
        if uid in DB and DB[uid]["p"] == upw:
            st.session_state.auth = True
            st.session_state.u_role = DB[uid]["r"]
            st.rerun()
    st.stop()

# 6. STYLE
st.markdown("<style>.card { background: white; padding: 15px; border-left: 10px solid #1e40af; margin-bottom: 10px; border-radius: 5px; box-shadow: 1px 1px 3px rgba(0,0,0,0.1); } .sig { font-family: 'Brush Script MT', cursive; font-size: 24px; color: #1e40af; }</style>", unsafe_allow_html=True)

# 7. DATA
@st.cache_data(ttl=1)
def load():
    s = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    g = "466678125"
    u = "https://docs.google.com/spreadsheets/d/" + s + "/export?format=csv&gid=" + g
    try:
        df = pd.read_csv(u)
        df.columns = df.columns.str.strip().str.upper()
        return df
    except:
        return pd.DataFrame()

df = load()

# 8. NAV
m = st.sidebar.radio("NAV", ["APPROVALS", "AUDIT LOG"])
if st.sidebar.button("OUT"):
    st.session_state.auth = False
    st.rerun()

# 9. DASHBOARD
if m == "APPROVALS":
    st.header("BOM PRICE APPROVALS")
    if not df.empty and st.session_state.u_role == "HOD":
        st.subheader("PENDING FOR BIXAPATHI")
        appr_list = [x['V'] for x in st.session_state.log_data]
        if T_C in df.columns:
            p_df = df[df[T_C].isna()]
            p_df = p_df[~p_df[V_C].isin(appr_list)]
            for i, r in p_df.iterrows():
                # SHORT VERTICAL ASSIGNMENT
                vn = str(r.get(V_C))
                pn = str(r.get(P_C))
                pr
