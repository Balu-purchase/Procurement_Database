import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. PAGE CONFIG (Must be first) ---
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide", initial_sidebar_state="expanded")

# --- 2. SESSION STATE INITIALIZATION (The "Memory") ---
if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
if "role" not in st.session_state:
    st.session_state.role = None

# --- 3. GOOGLE SHEETS CONFIG ---
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
LIVE_DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- 4. DATA LOADING ---
@st.cache_data(ttl=15) # Short cache for faster updates
def load_live_data(url):
    try:
        # Pulling live data: S.NO, ID, DATE, PLANT, ITEM NAME, DEPT, etc.
        return pd.read_csv(url)
    except Exception:
        return None

# --- 5. VISIBILITY STYLE (High Contrast) ---
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
    h1, h2, h3, p, span, label, .stMetric {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 8px #000000 !important;
    }
    .stDataFrame {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 10px;
    }
    .status-box {
        background: rgba(0, 0, 0, 0.8);
        border-left: 5px solid #38bdf8;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

ACCESS_KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 6. MAIN LOGIC ---
if not st.session_state.secure_access:
    # --- LOGIN SCREEN (No refresh here) ---
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br><div style='background:rgba(0,0,0,0.8); padding:30px; border-radius:15px; border:2px solid #38bdf8; text-align:center;'><h1>🔐 SKYQUAD SHIELD</h1></div>", unsafe_allow_html=True)
        
        role_select = st.selectbox("OPERATIONAL ROLE", list(ACCESS_KEYS.keys()))
        pwd_input = st.text_input("SECURITY PASSKEY", type="password")
        
        if st.button("AUTHORIZE ACCESS", use_container_width=True):
            if pwd_input == ACCESS_KEYS.get(role_select):
                st.session_state.secure_access = True
                st.session_state.role = role_select
                st.rerun()
            else:
                st.error("Invalid Passkey")
else:
    # --- AUTHORIZED VIEW (Refresh ONLY active here) ---
    
    # 7. AUTO-REFRESH SCRIPT (Only runs when logged in)
    components.html(
        """
        <script>
        setTimeout(function(){
            window.parent.location.reload();
        }, 30000); // 30 seconds
        </script>
        """,
        height=0,
    )

    with st.sidebar:
        st.markdown(f'<div class="status-box"><b>OPERATOR:</b><br>{st.session_state.role}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-box"><b>STATUS:</b><br>LIVE AUTO-SYNC</div>', unsafe_allow_html=True)
        if st.button("LOGOUT"):
            st.session_state.secure_access = False
            st.session_state.role = None
            st.rerun()

    df = load_live_data(LIVE_DATA_URL)
    
    if df is not None:
        st.markdown(f"<h1>🚀 {st.session_state.role} Command Center</h1>", unsafe_allow_html=True)
        
        # Live Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Live Records", len(df))
        m2.metric("Sync Status", "Active")
        m3.metric("Last Update", datetime.now().strftime("%H:%M:%S"))

        search = st.text_input("🔍 LIVE FILTER")
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Auto-refreshing every 30 seconds... changes in Google Sheets will appear automatically.")
    else:
        st.error("📡 Link Error: Verify Google Sheet permissions (Anyone with link can view).")
