import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="BOM Approval", layout="wide")

# 2. CONFIG
H_N = "Bixapathi"
H_D = "Head of Department (HOD)"
G_N = "General Manager"
DB = {
 "hod_office": {"p": "HOD789", "r": "HOD"},
 "gm_office": {"p": "GM2026", "r": "GM"}
}

# 3. SESSION STORAGE (OFFICIAL RECORDS)
if "auth" not in st.session_state:
    st.session_state.auth = False
if "official_records" not in st.session_state:
    st.session_state.official_records = []

# 4. LOGIN
if not st.session_state.auth:
    st.sidebar.title("🔐 OFFICIAL LOGIN")
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
m = st.sidebar.radio("MENU", ["PENDING APPROVALS", "OFFICIAL RECORDS"])
if st.sidebar.button("LOGOUT"):
    st.session_state.auth = False
    st.rerun()

# 7. PENDING APPROVALS (HOD & GM WORKBENCH)
if m == "PENDING APPROVALS":
    st.header("🏭 PENDING PRICE VERIFICATION")
    role = st.session_state.get("u_role")
    
    if not df.empty:
        # Define the target columns based on user role
        T_C = "HOD APPROVAL" if role == "HOD" else "GM APPROVAL"
        V_C, P_C, R_C, S_C = "VENDOR NAME", "PART NUMBER", "PRICE", "BOM STATUS"

        # Filter: Only show rows where the specific approval column is EMPTY
        p_df = df[df[T_C].isna() | (df[T_C].astype(str).str.strip() == "")]
        
        # Filter out what we already moved to records in this session
        done_ids = [x['V'] + x['N'] for x in st.session_state.official_records]
        p_df = p_df[~(p_df[V_C] + p_df[P_C]).isin(done_ids)]

        if p_df.empty:
            st.success("✅ All pending items have been cleared.")
        else:
            # Table Header
            h1, h2, h3, h4, h5 = st.columns([2, 2, 1, 2, 1])
            h1.subheader("VENDOR")
            h2.subheader("PART NO")
            h3.subheader("PRICE")
            h4.subheader("SIGNATURE (TYPE OK)")
            h5.subheader("ACTION")

            # Table Rows
            for i, r in p_df.iterrows():
                c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 2, 1])
                vn, pn, pr = str(r.get(V_C)), str(r.get(P_C)), str(r.get(R_C))
                
                c1.write(vn)
                c2.write(pn)
                c3.write(pr)
                
                # Signature Input (Empty by default)
                sig_input = c4.text_input("Sig", key="sig"+str(i), label_visibility="collapsed")
                
                if c5.button("OK", key="btn"+str(i)):
                    if sig_input.upper() in ["OK", "APPROVED", "OKAY"]:
                        ts = datetime.now().strftime('%Y-%m-%d %H:%M')
                        approver = H_N if role == "HOD" else G_N
                        
                        # MOVE ENTIRE ROW TO OFFICIAL RECORDS
                        record = {
                            "V": vn, "N": pn, "P": pr, 
                            "S": str(r.get(S_C)), 
                            "SIG": sig_input.upper(),
                            "BY": approver,
                            "TIME": ts
                        }
                        st.session_state.official_records.append(record)
                        st.success("Record Finalized: " + vn)
                        st.rerun()
                st.divider()

    st.write("### 📊 LIVE DATABASE VIEW")
    st.dataframe(df, use_container_width=True)

# 8. OFFICIAL RECORDS (THE DRAFTS / AUDIT LOG)
else:
    st.header("📜 OFFICIAL ARCHIVED RECORDS")
    if not st.session_state.official_records:
        st.info("No records have been moved to official logs yet.")
    
    for r in st.session_state.official_records:
        with st.container(border=True):
            st.success("VERIFIED BY: " + r['BY'])
            st.write("**VENDOR:** " + r['V'] + " | **PART:** " + r['N'])
            st.write("**PRICE:** " + r['P'] + " | **STATUS:** " + r['S'])
            st.write("**OFFICIAL SIGNATURE:** " + r['SIG'])
            st.write("**TIMESTAMP:** " + r['TIME'])
            st.markdown("*Archived Document - Signed by " + r['BY'] + "*")
