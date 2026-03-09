import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="BOM", layout="wide")

# 2. CONFIG
H_N = "Bixapathi"
H_D = "Head of Department (HOD)"
B_D = "BOM Executive"
T_C = "HOD APPROVAL"

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
    st.sidebar.title("🔐 BOM LOGIN")
    uid = st.sidebar.text_input("ID")
    upw = st.sidebar.text_input("PW", type="password")
    if st.sidebar.button("IN"):
        if uid in DB and DB[uid]["p"] == upw:
            st.session_state.auth = True
            st.session_state.u = DB[uid]
            st.rerun()
    st.stop()

# 6. STYLE
st.markdown("<style>.card { background: white; padding: 10px; border-left: 5px solid #1e40af; margin-bottom: 10px; } .sig { font-family: 'Brush Script MT', cursive; font-size: 22px; color: #1e40af; }</style>", unsafe_allow_html=True)

# 7. DATA
@st.cache_data(ttl=5)
def load():
    s = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    g = "466678125"
    b = "https://docs.google.com/spreadsheets/d/"
    u = b + s + "/export?format=csv&gid=" + g
    try:
        df = pd.read_csv(u)
        df.columns = df.columns.str.strip().str.upper()
        return df
    except:
        return pd.DataFrame()

df = load()
u_r = st.session_state.u.get("r", "")

# 8. NAV
m = st.sidebar.radio("NAV", ["🏠 APPR", "🏛️ LOG"])
if st.sidebar.button("OUT"):
    st.session_state.auth = False
    st.rerun()

# 9. DASHBOARD
if m == "🏠 APPR":
    st.header("🏭 PRICE APPROVALS: BOM")
    if not df.empty:
        if u_r == "HOD":
            st.subheader("📝 REVIEW")
            if T_C in df.columns:
                p = df[df[T_C].isna()]
                for i, r in p.iterrows():
                    v = str(r.get('VENDOR NAME', 'N/A'))
                    with st.expander("Review: " + v):
                        st.write("Price: " + str(r.get('PRICE', '0')))
                        t = st.text_input("Comment", key="c"+str(i))
                        if st.button("OK", key="b"+str(i)):
                            if t.upper() == "APPROVED":
                                st.success("Signed: " + H_N)
        else:
            st.info("BOM VIEW: Waiting for HOD.")
        st.divider()
        st.dataframe(df, use_container_width=True)

# 10. AUDIT LOG
else:
    st.header("📜 OFFICIAL AUDIT LOG")
    if not df.empty and T_C in df.columns:
        # Fixed logic for short lines
        is_ok = df[T_C].astype(str).str.upper() == "APPROVED"
        ok_df = df[is_ok]
        if ok_df.empty:
            st.info("No records.")
        for _, r in ok_df.iterrows():
            v = str(r.get('VENDOR NAME'))
            ts = datetime.now().strftime('%Y-%m-%d %H:%M')
            st
