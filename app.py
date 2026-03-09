import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="BOM Approval", layout="wide")

# 2. CONFIG
H_N = "Bixapathi"
H_D = "Head of Department (HOD)"
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
st.markdown("<style>.card { background: white; padding: 15px; border-left: 10px solid #1e40af; margin-bottom: 15px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); } .sig { font-family: 'Brush Script MT', cursive; font-size: 24px; color: #1e40af; } th { background-color: #f1f5f9 !important; }</style>", unsafe_allow_html=True)

# 7. DATA
@st.cache_data(ttl=2)
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
m = st.sidebar.radio("NAV", ["🏠 PRICE APPROVALS", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOGOUT"):
    st.session_state.auth = False
    st.rerun()

# 9. DASHBOARD (TABLE FORMAT)
if m == "🏠 PRICE APPROVALS":
    st.header("🏭 PRICE APPROVALS FOR BOM ITEMS")
    
    if not df.empty:
        if u_r == "HOD":
            st.subheader("📋 PENDING APPROVAL TABLE")
            if T_C in df.columns:
                # Get rows where HOD Approval is empty
                p_df = df[df[T_C].isna() | (df[T_C].astype(str).str.strip() == "")]
                
                if p_df.empty:
                    st.success("✅ All Items Processed")
                else:
                    # Create a manual table with columns
                    h1, h2, h3, h4, h5 = st.columns([2, 2, 1, 2, 1])
                    h1.write("**VENDOR**")
                    h2.write("**PART NO**")
                    h3.write("**PRICE**")
                    h4.write("**HOD COMMENT**")
                    h5.write("**ACTION**")
                    st.divider()

                    for i, r in p_df.iterrows():
                        c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 2, 1])
                        v = str(r.get('VENDOR NAME', 'N/A'))
                        pn = str(r.get('PART NUMBER', 'N/A'))
                        pr = str(r.get('PRICE', '0'))
                        
                        c1.write(v)
                        c2.write(pn)
                        c3.write(pr)
                        cmt = c4.text_input("Comment", key=f"t{i}", label_visibility="collapsed")
                        if c5.button("OK", key=f"b{i}"):
                            if cmt.upper() == "APPROVED":
                                st.success(f"Finalized: {v}")
            else:
                st.error("Column 'HOD APPROVAL' not found.")
        
        st.write("###
