import streamlit as st
import pandas as pd
from datetime import datetime

# 1. INITIALIZE PAGE CONFIG (Must be the very first Streamlit command)
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide", initial_sidebar_state="expanded")

# 2. DEFINE SECURITY KEYS
ACCESS_KEYS = {
    "BOM Team": "BOM2026",
    "Non-BOM Team": "NBOM2026",
    "GM Management": "GM789"
}

# 3. LINK TO YOUR GOOGLE SHEET
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
LIVE_DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 4. INITIALIZE SESSION STATE (To prevent NameErrors)
if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
if "role" not in st.session_state:
    st.session_state.role = None

# 5. DATA LOADING FUNCTION
@st.cache_data(ttl=30)
def load_live_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        return None

# 6. UI STYLING (CSS)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #0369a1);
        background-size: 400% 400%;
        animation: skyquadGradient 15s ease infinite;
    }
    @keyframes skyquadGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .status-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #38bdf8;
        padding: 15px; border-radius: 10px; margin-bottom: 12px;
    }
    .status-label { color: #94a3b8; font-size: 0.75rem; text-transform: uppercase; }
    .status-value { color: #f8fafc; font-weight: 700; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# 7. MAIN LOGIC FLOW
if not st.session_state.secure_access:
    # --- LOGIN SCREEN ---
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);'>
                <h1 style='text-align: center; color: white;'>🔐 SKYQUAD SHIELD</h1>
                <p style='text-align: center; color: #64748b;'>Restricted Procurement Access Portal</p>
            </div>
        """, unsafe_allow_html=True)
        
        role_options = list(ACCESS_KEYS.keys())
        selected_role = st.selectbox("OPERATIONAL ROLE", role_options)
        entered_pwd = st.text_input("SECURITY PASSKEY", type="password")
        
        if st.button("AUTHORIZE ACCESS", use_container_width=True):
            if entered_pwd == ACCESS_KEYS.get(selected_role):
                st.session_state.secure_access = True
                st.session_state.role = selected_role
                st.rerun()
            else:
                st.error("Protocol Violation: Invalid Key")

else:
    # --- AUTHORIZED DASHBOARD ---
    with st.sidebar:
        st.markdown(f"""<div class="status-card"><div class="status-label">Operator</div><div class="status-value">{st.session_state.role}</div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="status-card" style="border-left-color: #22c55e;"><div class="status-label">Live Link</div><div class="status-value">CONNECTED</div></div>""", unsafe_allow_html=True)
        
        if st.button("TERMINATE SESSION", use_container_width=True):
            st.session_state.secure_access = False
            st.session_state.role = None
            st.rerun()

    # Load Data from Google Sheets
    df = load_live_data(LIVE_DATA_URL)

    if df is not None:
        st.markdown(f"<h1>{st.session_state.role} Command Center</h1>", unsafe_allow_html=True)
        
        # Dashboard Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Line Items", len(df))
        m2.metric("Sync Status", "Active")
        m3.metric("Last Update", datetime.now().strftime("%H:%M:%S"))

        # Search
        query = st.text_input("🔍 SEARCH DATABASE")
        if query:
            df = df[df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        if st.button("🔄 FORCE REFRESH"):
            st.cache_data.clear()
            st.rerun()
    else:
        st.error("⚠️ Connection Error: Please verify Google Sheet permissions (Anyone with link can view).")
