import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Audit Portal", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "hod_office": {
        "pass": "HOD789", "role": "HOD", 
        "name": "Bixapathi", "desig": "Head of Department (HOD)"
    },
    "bom_team": {
        "pass": "BOM2026", "role": "BOM", 
        "name": "BOM Team", "desig": "Executive"
    }
}

# 3. INITIALIZE SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u_info" not in st.session_state:
    st.session_state.u_info = {}

# 4. ACCESS CONTROL (The Gatekeeper)
if not st.session_state.auth:
    st.sidebar.title("🔐 LOGIN")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN"):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[u_id]
            st.rerun()
        else:
            st.sidebar.error("Invalid ID/Password")
    st.stop()

# 5. STYLING
st.markdown("""
<style>
    .audit-card { 
        background: white; padding: 20px; border-radius: 10px; 
        border-left: 8px solid #1e40af; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        margin-bottom: 15px;
    }
    .sig-font { font-family: 'Brush Script MT', cursive; font-size: 26px; color: #1e40af; }
    h1 { text-align: center; color: #1e40af; }
</style>
""", unsafe_allow_html=True)

# 6. DATA LOADING (GID 466678125)
@st.cache_data(ttl=10)
def load_data():
    sid = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    gid = "466678125" 
    base = "https://docs.google.com/spreadsheets/d/"
    url = base + sid + "/export?format=csv&gid=" + gid
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip().str.upper()
        return data
    except Exception as e:
        st.error("Sheet Connection Error")
        return pd.DataFrame()

df = load_data()
u = st.session_state.u_info

# 7. NAVIGATION
menu = st.sidebar.radio("NAVIGATE", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 8. DASHBOARD (FIXED LINE 84)
if menu == "🏠 DASHBOARD":
    role = u.get('role', 'User')
    st.markdown("<h1>🏭 " + role + " CONTROL CENTER</h1>", unsafe_allow_html=True)
    
    if not df.empty:
        # Check if user is HOD to show approval buttons
        if role == "HOD":
            st.subheader("🔔 PENDING APPROVALS")
            col = "HOD APPROVAL"
            if col in df.columns:
                pending = df[df[col].isna()]
                if pending.empty:
                    st.success("🎉 All entries are approved!")
                else:
                    for i, r in pending.iterrows():
                        v_name = str(r.get('VENDOR NAME', 'Row ' + str(i)))
                        with st.expander("Review: " + v_name):
                            st.write("**Price:** " + str(r.get('PRICE', 'N/A')))
                            if st.button("APPROVE " + str(i), key="b"+str(i)):
                                st.success("Verified by " + u.get('name'))
            else:
                st.info("Header 'HOD APPROVAL' not found in Sheet.")
        
        st.divider()
        st.dataframe(df, use_container_width=True, hide_index=True)

# 9. AUDIT LOG (Bixapathi Signature & Designation)
else:
    st.markdown("<h1>📜 OFFICIAL AUDIT LOG</h1>", unsafe_allow_html=True)
    col = "HOD APPROVAL"
    
    if not df.empty and col in df.columns:
        approved = df[df[col].notna()]
        if approved.empty:
            st.info("No approved records found.")
        else:
            for _, r in approved.iterrows():
                now = datetime.now().strftime('%Y-%m-%d %H:%M')
                v = str(r.get('VENDOR NAME', 'N/A'))
                p = str(r.get('PRICE', 'N/A'))
                
                html = '<div class="audit-card">'
                html += '<b>VENDOR: ' + v + ' | PRICE: ' + p + '</b><hr>'
                html += '<table style="width:100%"><tr>'
                html += '<td><b>APPROVER:</b> ' + u.get('name') + '</td>'
                html += '<td><b>DESIGNATION:</b> ' + u.get('desig') + '</td></tr>'
                html += '<tr><td><b>TIME:</b> ' + now + '</td>'
                html += '<td class="sig-font">Sig: ' + u.get('name') + '</td></tr>'
                html += '</table></div>'
                st.markdown(html, unsafe_allow_html=True)
