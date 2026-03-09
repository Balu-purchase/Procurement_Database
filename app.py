import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Audit Portal", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "hod_office": {"pass": "HOD789", "role": "HOD", "name": "Bixapathi", "desig": "Head of Department (HOD)"},
    "bom_team": {"pass": "BOM2026", "role": "BOM", "name": "BOM Team", "desig": "Executive"}
}

# 3. INITIALIZE SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = None

# 4. PROFESSIONAL STYLING
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .audit-card { 
        background: white; padding: 25px; border-radius: 12px; 
        border-left: 10px solid #1e40af; box-shadow: 0 4px 10px rgba(0,0,0,0.1); 
        margin-bottom: 20px;
    }
    .sig-font { font-family: 'Brush Script MT', cursive; font-size: 28px; color: #1e40af; }
    h1 { text-align: center; color: #0f172a; font-weight: 800; border-bottom: 2px solid #1e40af; padding-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 5. SIDEBAR LOGIN
st.sidebar.title("🔐 ACCESS CONTROL")
if not st.session_state.auth:
    u_id = st.sidebar.text_input("USER ID")
    u_pw = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("SIGN IN", use_container_width=True):
        if u_id in USER_DB and USER_DB[u_id]["pass"] == u_pw:
            st.session_state.auth, st.session_state.user = True, USER_DB[u_id]
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid ID or Password")
    st.stop()

# 6. NAVIGATION
menu = st.sidebar.radio("NAVIGATE", ["🏠 DASHBOARD", "🏛️ AUDIT LOG"])
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# 7. DATA LOADING
@st.cache_data(ttl=30)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv&gid=2061093150"
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame()

df = load_data()

# 8. DASHBOARD VIEW
if menu == "🏠 DASHBOARD":
    u = st.session_state.user
    st.markdown(f"<h1>🏭 {u['role']} CONTROL CENTER</h1>", unsafe_allow_html=True)
    
    if not df.empty:
        if u['role'] == "HOD":
            st.subheader("🔔 PENDING HOD APPROVALS")
            if 'HOD APPROVAL' in df.columns:
                # Clean check for empty/NaN cells
                pending = df[df['HOD APPROVAL'].fillna('').eq('')]
                if not pending.empty:
                    for i, r in pending.iterrows():
                        with st.expander(f"Review: {r.get('VENDOR NAME')} | {r.get('PART NUMBER')}"):
                            st.write(f"**Price:** {r.get('PRICE')}")
                            if st.button(f"APPROVE S.NO {r.get('S.NO')}", key=f"btn_{i}"):
                                st.success(f"Approved by {u['name']}")
                else:
                    st.info("No records pending approval.")
        
        st.divider()
        st.dataframe(df, use_container_width=True, hide_index=True)

# 9. AUDIT LOG VIEW
else:
    st.markdown("<h1>📜 OFFICIAL AUDIT & APPROVAL TRAIL</h1>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 Search Vendor or Part Number").lower()
    
    if not df.empty and 'HOD APPROVAL' in df.columns:
        # Get only approved rows
        approved = df[df['HOD APPROVAL'].fillna('').ne('')]
        
        # Apply Search Filter
        if search:
            approved = approved[approved.astype(str).apply(lambda x: x.str.lower().str.contains(search)).any(axis=1)]

        if approved.empty:
            st.info("No records found.")
        else:
            u = st.session_state.user
            for _, r in approved.iterrows():
                st.markdown(f"""
                <div class="audit-card">
                    <div style="display:flex; justify-content:space-between;">
                        <b>S.NO: {r.get('S.NO')}</b>
                        <b style="color:green;">✅ HOD VERIFIED</b>
                    </div>
                    <hr>
                    <p><b>VENDOR:</b> {r.get('VENDOR NAME')} | <b>PART:</b> {r.get('PART NUMBER')} | <b>PRICE:</b> {r.get('PRICE')}</p>
                    <table style="width:100%; margin-top:10px; border-top:1px dashed #ccc;">
                        <tr>
                            <td style="padding-top:10px;"><b>APPROVER:</b> {u['name']}</td>
                            <td style="padding-top:10px;"><b>DESIGNATION:</b> {u['desig']}</td>
                        </tr>
                        <tr>
                            <td><b>TIME:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
                            <td class="sig-font">Signature: {u['name']}</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
