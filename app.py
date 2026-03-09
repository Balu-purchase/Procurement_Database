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
if "u_role" not in st.session_state:
    st.session_state.u_role = None

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

# 5. STYLE
st.markdown("<style>.card { background: white; padding: 15px; border-left: 10px solid #1e40af; margin-bottom: 10px; border-radius: 5px; box-shadow: 1px 1px 3px rgba(0,0,0,0.1); } .sig { font-family: 'Brush Script MT', cursive; font-size: 24px; color: #1e40af; } .hdr { font-weight: bold; background: #f0f2f6; padding: 10px; border-bottom: 2px solid #ccc; }</style>", unsafe_allow_html=True)

# 6. DATA LOADING
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

# 7. NAVIGATION
m = st.sidebar.radio("MENU", ["PENDING APPROVALS", "AUDIT LOG"])
if st.sidebar.button("LOGOUT"):
    st.session_state.auth = False
    st.rerun()

# 8. PENDING APPROVALS TAB
if m == "PENDING APPROVALS":
    st.header("🏭 PRICE APPROVAL PENDING FOR HOD")
    
    if st.session_state.u_role == "HOD" and not df.empty:
        # Find column names dynamically to prevent "Missing" errors
        cols = df.columns.tolist()
        T_C = next((c for c in cols if "HOD APPROVAL" in c), None)
        V_C = next((c for c in cols if "VENDOR" in c), "VENDOR NAME")
        P_C = next((c for c in cols if "PART" in c), "PART NUMBER")
        R_C = next((c for c in cols if "PRICE" in c), "PRICE")
        S_C = next((c for c in cols if "STATUS" in c), "BOM STATUS")

        if T_C:
            # Filter for items not yet approved in Excel or local memory
            p_df = df[df[T_C].isna() | (df[T_C].astype(str).str.strip() == "")]
            seen = [x['V'] for x in st.session_state.log_data]
            p_df = p_df[~p_df[V_C].isin(seen)]

            if p_df.empty:
                st.success("✅ No pending reviews for Bixapathi.")
            else:
                # TABLE HEADER
                st.markdown('<div class="hdr">', unsafe_allow_html=True)
                h1, h2, h3, h4, h5 = st.columns([2, 2, 1, 2, 1])
                h1.write("VENDOR")
                h2.write("PART NO")
                h3.write("PRICE")
                h4.write("HOD COMMENT")
                h5.write("ACTION")
                st.markdown('</div>', unsafe_allow_html=True)

                # TABLE ROWS
                for i, r in p_df.iterrows():
                    c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 2, 1])
                    v, n, p = str(r.get(V_C)), str(r.get(P_C)), str(r.get(R_C))
                    s = str(r.get(S_C))
                    
                    c1.write(v)
                    c2.write(n)
                    c3.write(p)
                    t_input = c4.text_input("cmt", key=f"t{i}", label_visibility="collapsed", placeholder="APPROVED")
                    
                    if c5.button("OK", key=f"b{i}"):
                        if t_input.upper() in ["APPROVED", "OK"]:
                            new = {"V": v, "N": n, "P": p, "S": s, "T": datetime.now().strftime('%Y-%m-%d %H:%M')}
                            st.session_state.log_data.append(new)
                            st.success(f"Finalized: {v}")
                            st.rerun()
                    st.divider()
        else:
            st.error("Could not find 'HOD APPROVAL' column in your sheet.")

    st.write("### 📊 MASTER DATABASE")
    st.dataframe(df, use_container_width=True)

# 9. AUDIT LOG TAB
else:
    st.header("📜 OFFICIAL AUDIT LOG")
    if not st.session_state.log_data:
        st.info("No items approved this session.")
    
    for r in st.session_state.log_data:
        st.markdown(f"""
        <div class="card">
            <b>VENDOR:</b> {r['V']} | <b>PART:</b> {r['N']}<br>
            <b>PRICE:</b> {r['P']} | <b>BOM STATUS:</b> {r['S']}<br><hr>
            <b>APPROVER:</b> {H_N} | <b>DESIG:</b> {H_D}<br>
            <b>TIME:</b> {r['T']} | <span class="sig">Sig: {H_N}</span>
        </div>
        """, unsafe_allow_html=True)
