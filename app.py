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
st.markdown("<style>.card { background: white; padding: 12px; border-left: 10px solid #1e40af; margin-bottom: 10px; } .sig { font-family: 'Brush Script MT', cursive; font-size: 22px; color: #1e40af; }</style>", unsafe_allow_html=True)

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
m = st.sidebar.radio("NAV", ["APPROVALS", "LOG"])
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
    p = df[df[T_C].isna()]
    for i, r in p.iterrows():
     vn = str(r.get(V_C))
     pn = str(r.get(P_C))
     pr = str(r.get(R_C))
     st.write(f"**{vn}** | {pn} | {pr}")
     t = st.text_input("CMT", key=f"t{i}")
     if st.button("OK", key=f"b{i}"):
      if t.upper() in ["APPROVED", "OK"]:
       st.success("Approved: " + vn)
  st.divider()
  st.dataframe(df)

# 10. AUDIT LOG
else:
 st.header("OFFICIAL AUDIT LOG")
 if not df.empty:
  if T_C in df.columns:
   mask = df[T_C].astype(str).str.upper()
   is_ok = mask.isin(["APPROVED", "OK"])
   ok_df = df[is_ok]
   for _, r in ok_df.iterrows():
    v = str(r.get(V_C))
    n = str(r.get(P_C))
    p = str(r.get(R_C))
    s = str(r.get(S_C))
    ts = datetime.now().strftime('%H-%M')
    st.markdown(f"""<div class="card">
    <b>VENDOR:</b> {v} | <b>PART:</b> {n}<br>
    <b>PRICE:</b> {p} | <b>STATUS:</b> {s}<br><hr>
    <b>APPROVER:</b> {H_N} | <b>DESIG:</b> {H_D}<br>
    <b>TIME:</b> {ts} | <span class="sig">Sig: {H_N}</span>
    </div>""", unsafe_allow_html=True)
