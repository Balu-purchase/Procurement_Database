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

# 4. SESSION (CRITICAL FOR SAVING)
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u" not in st.session_state:
    st.session_state.u = {}
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
            st.session_state.u = DB[uid]
            st.rerun()
    st.stop()

# 6. STYLE
st.markdown("<style>.card { background: white; padding: 15px; border-left: 10px solid #1e40af; margin-bottom: 10px; border-radius: 5px; box-shadow: 1px 1px 3px rgba(0,0,0,0.1); } .sig { font-family: 'Brush Script MT', cursive; font-size: 24px; color: #1e40af; }</style>", unsafe_allow_html=True)

# 7. DATA LOADING
@st.cache_data(ttl=1)
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
m = st.sidebar.radio("NAV", ["APPROVALS", "AUDIT LOG"])
if st.sidebar.button("OUT"):
    st.session_state.auth = False
    st.rerun()

# 9. DASHBOARD (APPROVALS)
if m == "APPROVALS":
    st.header("BOM PRICE APPROVALS")
    if not df.empty and u_r == "HOD":
        st.subheader("PENDING FOR BIXAPATHI")
        
        # Filter out items already approved in this session
        approved_vendors = [x['V'] for x in st.session_state.log_data]
        
        if T_C in df.columns:
            # Only show items not approved in Excel AND not approved in Session
            p_df = df[df[T_C].isna()]
            p_df = p_df[~p_df[V_C].isin(approved_vendors)]
            
            if p_df.empty:
                st.success("All Items Reviewed")
            else:
                for i, r in p_df.iterrows():
                    v_n = str(r.get(V_C))
                    p_n = str(r.get(P_C))
                    pr = str(r.get(R_C))
                    st.write("**" + v_n + "** | Part: " + p_n + " | Price: " + pr)
                    
                    t = st.text_input("Comment", key="t"+str(i))
                    if st.button("APPROVE", key="b"+str(i)):
                        if t.upper() in ["APPROVED", "OK"]:
                            # SAVE TO SESSION LOG IMMEDIATELY
                            new_entry = {
                                "V": v_n, "N": p_n, "P": pr,
                                "S": str(r.get(S_C, "N/A")),
                                "T": datetime.now().strftime('%Y-%m-%d %H:%M')
                            }
                            st.session_state.log_data.append(new_entry)
                            st.success("Success: " + v_n + " sent to Audit Log")
                            st.rerun()
    st.divider()
    st.dataframe(df)

# 10. AUDIT LOG (DISPLAY SAVED REVIEWS)
else:
    st.header("OFFICIAL AUDIT LOG")
    
    # 10a. Show what Bixapathi just approved in this session
    if st.session_state.log_data:
        for item in st.session_state.log_data:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write("**VENDOR:** " + item["V"] + " | **PART:** " + item["N"])
            st.write("**PRICE:** " + item["P"] + " | **STATUS:** " + item["S"])
            st.write("**APPROVER:** " + H_N + " | **DESIG:** " + H_D)
            st.write("**TIME:** " + item["T"])
            st.markdown('<span class="sig">Sig: ' + H_N + '</span>', unsafe_allow_html=True)
            st.markdown('</div>',
