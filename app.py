import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide")

# High-Visibility CSS (Dark theme with white bold text)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    h1, h2, h3, p, span, label, .stMetric { 
        color: #ffffff !important; 
        font-weight: bold !important; 
    }
    .stDataFrame { background: rgba(255,255,255,0.05); border: 1px solid #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PERSISTENT LOGIN ---
# This keeps you logged in even when the data changes
if "auth" not in st.session_state:
    st.session_state.auth = False

ACCESS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

if not st.session_state.auth:
    st.title("🔐 SKYQUAD LOGIN")
    role = st.selectbox("Role", list(ACCESS.keys()))
    key = st.text_input("Passkey", type="password")
    if st.button("Login"):
        if key == ACCESS[role]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid Key")
else:
    # --- 3. THE REAL-TIME DASHBOARD ---
    # Auto-refresh logic (Forces browser to check for changes every 20s)
    st.empty() 
    st.write(f"Logged in as: {st.session_state.role if 'role' in st.session_state else 'Operator'}")
    
    # Google Sheet Link
    SID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    URL = f"https://docs.google.com/spreadsheets/d/{SID}/export?format=csv"

    # Load Data (No caching so it stays fresh)
    try:
        df = pd.read_csv(URL)
        st.title("🚀 Live Command Center")
        
        # Display Metrics
        c1, c2 = st.columns(2)
        c1.metric("Items", len(df))
        c2.metric("Last Sync", datetime.now().strftime("%H:%M:%S"))

        # Search box
        search = st.text_input("🔍 Search Database")
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

        st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.error("Sheet Connection Error. Check Google Sheet Share settings.")

    # Auto-refresh hack: Refresh every 20 seconds
    import time
    time.sleep(20)
    st.rerun()
