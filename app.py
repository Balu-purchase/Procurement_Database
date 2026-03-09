import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Audit Portal", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "hod_office": {
        "pass": "HOD789", 
        "role": "HOD", 
        "name": "Bixapathi", 
        "desig": "Head of Department (HOD)"
    },
    "bom_team": {
        "pass": "BOM2026", 
        "role": "BOM", 
        "name": "BOM Team", 
        "desig": "Executive"
    }
}

# 3. INITIALIZE SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "u_info" not in st.session_state:
    st.session_state.u_info = {}

# 4. STYLING
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .audit-card { 
        background: white; padding: 25px; border-radius: 12px; 
        border-left: 10px solid #1e40af; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        margin-bottom: 20px;
    }
    .sig-font { 
        font-family: 'Brush Script MT', cursive; 
        font-size: 28px; color: #1e40af; 
    }
    h1 { text-align: center; color: #0f172a; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# 5. ACCESS CONTROL
if not st.session_state.auth:
    st.sidebar.title("🔐 LOGIN")
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN"):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth = True
            st.session_state.u_info = USER_DB[u_id]
            st.rerun()
    st.stop()

# 6. NAVIGATION
menu = st.sidebar.radio("NAVIGATE", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 7. FAIL-SAFE DATA LOADING (NO F-STRINGS)
@st.cache_data(ttl=30)
def load_data():
    b = "https://docs.google.com/spreadsheets/d/"
    k = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    s = "/export?format=csv&gid=2061093150"
    url = b + k + s
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame()

df = load_data()
u = st.session_state.u_info

# 8. DASHBOARD VIEW
if menu == "🏠 DASHBOARD":
    role = u.get('role', 'User')
    st.title(role + " CONTROL CENTER")
    
    if not df.empty and role == "HOD":
        st.subheader("🔔 PENDING APPROVALS")
        if 'HOD APPROVAL' in df.columns:
            mask = df['HOD APPROVAL'].fillna('').eq('')
            pending = df[pending_mask]
            for i, r in pending.iterrows():
                v_name = str(r.get('VENDOR NAME'))
                with st.expander("Review: " + v_name):
                    if st.button("APPROVE ROW " + str(i), key="btn_" + str(i)):
                        st.success("Verified by " + u.get('name'))
        
    st.divider()
    st.dataframe(df, use_container_width=True, hide_index=True)

# 9. AUDIT LOG VIEW (The HOD Signature Format)
else:
    st.markdown("<h1>📜 OFFICIAL AUDIT LOG</h1>", unsafe_allow_html=True)
    search = st.text_input("🔍 Search Vendor").lower()
    
    if not df.empty and 'HOD APPROVAL' in df.columns:
        mask = df['HOD APPROVAL'].fillna('').ne('')
        approved = df[mask]
        
        if search:
            approved = approved[approved.astype(str).apply(
                lambda x: x.str.lower().str.contains(search)
            ).any(axis=1)]

        for _, r in approved.iterrows():
            # Variables to avoid long lines
            v = str(r.get('VENDOR NAME'))
            p = str(r.get('PRICE'))
            name = str(u.get('name'))
            desig = str(u.get('desig'))
            time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            # Use simple string addition to build the Audit Card
            html = '<div class="audit-card">'
            html += '<b>VENDOR: ' + v + ' | PRICE: ' + p + '</b><hr>'
            html += '<table style="width:100%">'
            html += '<tr><td><b>APPROVER:</b> ' + name + '</td>'
            html += '<td><b>DESIGNATION:</b> ' + desig + '</td></tr>'
            html += '<tr><td><b>TIME:</b> ' + time_now + '</td>'
            html += '<td class="sig-font">Sig: ' + name + '</td></tr>'
            html += '</table></div>'
            
            st.markdown(html, unsafe_allow_html=True)
