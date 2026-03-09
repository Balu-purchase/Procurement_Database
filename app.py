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
if "u" not in st.session_state:
 st.session_state.u = {}
if "local_log" not in st.session_state:
 st.session_state.local_log = []

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
m = st.sidebar.radio("NAV", ["APPROVALS", "AUDIT LOG"])
if st.sidebar.button("OUT"):
 st.session_state.auth = False
 st.rerun()

# 9. DASHBOARD
if m == "APPROVALS":
 st.header("BOM PRICE APPROVALS")
 if not df.empty:
  if u_r == "HOD":
   st.subheader("HOD REVIEW")
   if T_C in df.columns:
    p_df = df[df[T_C].isna()]
    for i, r in p_df.iterrows():
     vn, pn, pr = str(r.get(V_C)), str(r.get(P_C)), str(r.get(R_C))
     st.write(f"**{vn}** | {pn} | {pr}")
     t = st.text_input("Comment", key=f"t{i}")
     if st.button("OK", key=f"b{i}"):
      if t.upper() in ["APPROVED", "OK"]:
       entry = {"V": vn, "N": pn, "P": pr, "S": str(r.get(S_C)), "T": datetime.now().strftime('%Y-%m-%d %H:%M')}
       st.session_state.local_log.append(entry)
       st.success("Sent to Logs: " + vn)
  st.divider()
  st.dataframe(df)

# 10. AUDIT LOG (SAFE FORMAT)
else:
 st.header("OFFICIAL AUDIT LOG")
 
 # 10a. Show Session Approvals
 for r in st.session_state.local_log:
  with st.container():
   st.markdown('<div class="card">', unsafe_allow_html=True)
   st.write(f"**VENDOR:** {r['V']} | **PART:** {r['N']}")
   st.write(f"**PRICE:** {r['P']} | **STATUS:** {r['S']}")
   st.write(f"**APPROVER:** {H_N} | **DESIG:** {H_D}")
   st.write(f"**TIME:** {r['T']}")
   st.markdown(f'<span class="sig">Sig: {H
