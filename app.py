import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="BOM Approval", layout="wide")

# 2. CONFIG
H_N = "Bixapathi"
H_D = "Head of Department (HOD)"
DB = {
 "hod_office": {"p": "HOD789", "r": "HOD"},
 "bom_team": {"p": "BOM2026", "r": "BOM"}
}

# 3. SESSION INITIALIZE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "log_data" not in st.session_state:
    st.session_state.log_data = []

# 4. LOGIN
if not st.session_state.auth:
    st.sidebar.title("🔐 BOM LOGIN")
    uid = st.sidebar.text_input("ID")
    upw = st.sidebar.text_input("PW", type="password")
    if st.sidebar.button("LOG IN"):
        if uid in DB and DB[uid]["p"] == upw:
            st.session_state.auth = True
            st.session_state.u_role = DB[uid]["r"]
            st.rerun()
    st.stop()

# 5. DATA LOADING
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

# 6. NAVIGATION
m = st.sidebar.radio("MENU", ["PENDING APPROVALS", "OFFICIAL AUDIT LOG"])
if st.sidebar.button("LOGOUT"):
    st.session_state.auth = False
    st.rerun()

# 7. PENDING APPROVALS TAB
if m == "PENDING APPROVALS":
    st.header("🏭 PRICE APPROVAL PENDING FOR HOD")
    
    if st.session_state.u_role == "HOD" and not df.empty:
        # Dynamic Column Mapping
        cols = df.columns.tolist()
        T_C = "HOD APPROVAL"
        V_C = "VENDOR NAME"
        P_C = "PART NUMBER"
        R_C = "PRICE"
        S_C = "BOM STATUS"

        # Logic for Filtering Pending Items
        p_df = df[df[T_C].isna() | (df[T_C].astype(str).str.strip() == "")]
        done = [x['V'] + x['N'] for x in st.session_state.log_data]
        p_df = p_df[~(p_df[V_C] + p_df[P_C]).isin(done)]

        if p_df.empty:
            st.success("✅ No pending reviews for Bixapathi.")
        else:
            # Table Header
            h1, h2, h3, h4, h5 = st.columns([2, 2, 1, 2, 1])
            h1.subheader("VENDOR")
            h2.subheader("PART NO")
            h3.subheader("PRICE")
            h4.subheader("COMMENT")
            h5.subheader("ACTION")

            # Table Rows
            for i, r in p_df.iterrows():
                c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 2, 1])
                v, n, p = str(r.get(V_C)), str(r.get(P_C)), str(r.get(R_C))
                s = str(r.get(S_C))
                
                c1.write(v)
                c2.write(n)
                c3.write(p)
                t_in = c4.text_input("cmt", key=f"t{i}", label_visibility="collapsed")
                
                if c5.button("OK", key=f"b{i}"):
                    if t_in.upper() == "APPROVED":
                        ts = datetime.now().strftime('%Y-%m-%d %H:%M')
                        new = {"V": v, "N": n, "P": p, "S": s, "C": t_in, "T": ts}
                        st.session_state.log_data.append(new)
                        st.success("Approved: " + v)
                        st.rerun()
                st.divider()

    st.write("### 📊 MASTER DATABASE VIEW")
    st.dataframe(df, use_container_width=True)

# 8. OFFICIAL AUDIT LOG TAB (NO TRIPLE QUOTES)
else:
    st.header("📜 OFFICIAL AUDIT LOG")
    if not st.session_state.log_data:
        st.info("No items approved this session.")
    
    for r in st.session_state.log_data:
        with st.container(border=True):
            st.success("STATUS: " + r['C'])
            st.write("**VENDOR:** " + r['V'] + " | **PART:** " + r['N'])
            st.write("**PRICE:** " + r['P'] + " | **BOM STATUS:** " + r['S'])
            st.write("**APPROVER:** " + H_N + " (" + H_D + ")")
            st.write
