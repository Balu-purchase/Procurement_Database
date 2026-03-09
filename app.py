import streamlit as st
import pandas as pd
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Procurement Audit System", layout="wide")

# 2. USER DATABASE (Recognized Users & Signatures)
USER_DB = {
    "hod_office": {
        "pass": "HOD789", 
        "role": "HOD", 
        "name": "Bixapathi", 
        "desig": "Head of Department (HOD)"
    },
    "bom_team": {"pass": "BOM2026", "role": "BOM", "name": "BOM Executive", "desig": "Data Entry"}
}

# 3. STYLING (Clean Industrial Management Look)
st.markdown("""
<style>
    .stApp { background-color: #f1f5f9; }
    .report-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .sig-style {
        font-family: 'Brush Script MT', cursive;
        font-size: 24px;
        color: #1e40af;
    }
    .status-approved { color: #10b981; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 4. AUTHENTICATION
if "auth" not in st.session_state:
    st.session_state.auth = False

st.sidebar.title("🔐 PORTAL ACCESS")
if not st.session_state.auth:
    u = st.sidebar.text_input("USER ID")
    p = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("LOG IN"):
        if u in USER_DB and USER_DB[u]["pass"] == p:
            st.session_state.auth = True
            st.session_state.user_data = USER_DB[u]
            st.rerun()
    st.stop()

# 5. NAVIGATION (The "Separate Icon/Else" logic)
menu = st.sidebar.radio("NAVIGATE SYSTEM", ["🏠 DASHBOARD", "🏛️ AUDIT & APPROVAL LOG"])

if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

# --- LOAD DATA ---
@st.cache_data(ttl=10)
def load_bom_data():
    # Replace with your actual Sheet URL and GID for BOM Team
    url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv&gid=2061093150"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

# 6. PAGE LOGIC
if menu == "🏠 DASHBOARD":
    st.markdown(f"<h1>🏭 {st.session_state.user_data['role']} CONTROL CENTER</h1>", unsafe_allow_html=True)
    df = load_bom_data()
    
    # HOD Approval Action
    if st.session_state.user_data['role'] == "HOD":
        st.subheader("🔔 PENDING APPROVALS")
        pending = df[df['HOD APPROVAL'].isna()]
        
        if not pending.empty:
            for i, row in pending.iterrows():
                with st.expander(f"Review Price: {row['VENDOR NAME']} - Part {row['PART NUMBER']}"):
                    st.write(f"**Proposed Price:** {row['PRICE']}")
                    if st.button(f"APPROVE NOW", key=f"btn_{i}"):
                        st.success("Successfully Approved & Signed by Bixapathi")
                        # Here you would trigger the write-back to Excel/Audit File
        else:
            st.info("No pending approvals today.")
    
    st.divider()
    st.dataframe(df, use_container_width=True)

elif menu == "🏛️ AUDIT & APPROVAL LOG":
    st.markdown("<h1>📜 OFFICIAL AUDIT TRAIL</h1>", unsafe_allow_html=True)
    st.write("Below are the verified records of HOD Approved Price Lists.")
    
    df = load_bom_data()
    # Filter for only approved items (where HOD Approval has a value)
    approved_items = df[df['HOD APPROVAL'].notna()]
    
    if approved_items.empty:
        st.info("No records have been formally approved yet.")
    else:
        for _, row in approved_items.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="report-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span><b>S.NO:</b> {row['S.NO']}</span>
                        <span class="status-approved">✅ VERIFIED</span>
                    </div>
                    <hr>
                    <p><b>VENDOR:</b> {row['VENDOR NAME']} | <b>PART:</b> {row['PART NUMBER']} | <b>PRICE:</b> {row['PRICE']}</p>
                    <table style="width:100%; margin-top:10px; border-top:1px dashed #ccc;">
                        <tr>
                            <td><b>APPROVER:</b> {st.session_state.user_data['name']}</td>
                            <td><b>DESIGNATION:</b> {st.session_state.user_data['desig']}</td>
                        </tr>
                        <tr>
                            <td><b>TIME:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                            <td><b>SIGNATURE:</b> <span class="sig-style">{st.session_state.user_data['name']}</span></td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
