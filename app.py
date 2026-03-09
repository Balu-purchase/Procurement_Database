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

# 4. ACCESS CONTROL
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

# 5. STYLING
st.markdown("""
<style>
    .audit-card { 
        background: white; padding: 20px; border-radius: 10px; 
        border-left: 8px solid #1e40af; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        margin-bottom: 15px;
    }
    .sig-font { font-family: 'Brush Script MT', cursive; font-size: 26px; color: #1e40af; }
</style>
""", unsafe_allow_html=True)

# 6. DATA LOADING (SWITCH TO SHEET2 GID)
@st.cache_data(ttl=10)
def load_data():
    # PASTE YOUR SHEET 2 GID HERE
    # To find it: Open Sheet2 in your browser and look at the URL for 'gid=XXXX'
    SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    GID_SHEET2 = "2061093150" 
    
    url = "https://docs.google.com/spreadsheets/d/" + SHEET_ID + "/export?format=csv&gid=" + GID_SHEET2
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame()

df = load_data()
u = st.session_state.u_info

# 7. NAVIGATION
menu = st.sidebar.radio("NAVIGATE", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])

# 8. DASHBOARD (FIXED EMPTY DATA LOGIC)
if menu == "🏠 DASHBOARD":
    st.title(u.get('role', 'User') + " CONTROL CENTER")
    
    if df.empty:
        st.error("⚠️ Data is Empty. Please check if GID is correct and Sheet is Public.")
    else:
        if u.get('role') == "HOD":
            st.subheader("🔔 PENDING APPROVALS")
            # Logic: If 'HOD APPROVAL' column exists, show rows where it's blank
            if 'HOD APPROVAL' in df.columns:
                pending = df[df['HOD APPROVAL'].isna()]
                if pending.empty:
                    st.success("All items from Sheet 2 are approved!")
                else:
                    for i, r in pending.iterrows():
                        v_name = str(r.get('VENDOR NAME', 'Unknown'))
                        with st.expander("Review: " + v_name):
                            st.write("**Price:** " + str(r.get('PRICE', '0')))
                            if st.button("APPROVE " + str(i), key="b"+str(i)):
                                st.success("Approved by " + u.get('name'))
            else:
                st.warning("Column 'HOD APPROVAL' not found in Sheet 2.")
        
        st.divider()
        st.dataframe(df, use_container_width=True, hide_index=True)

# 9. AUDIT LOG (BIXAPATHI SIGNATURE)
else:
    st.title("📜 OFFICIAL AUDIT LOG")
    if not df.empty and 'HOD APPROVAL' in df.columns:
        approved = df[df['HOD APPROVAL'].notna()]
        for _, r in approved.iterrows():
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            html = '<div class="audit-card">'
            html += '<b>VENDOR: ' + str(r.get('VENDOR NAME')) + '</b><hr>'
            html += '<table style="width:100%"><tr>'
            html += '<td><b>APPROVER:</b> ' + u.get('name') + '</td>'
            html += '<td><b>DESIGNATION:</b> ' + u.get('desig') + '</td></tr>'
            html += '<tr><td><b>TIME:</b> ' + now + '</td>'
            html += '<td class="sig-font">Sig: ' + u.get('name') + '</td></tr>'
            html += '</table></div>'
            st.markdown(html, unsafe_allow_html=True)
