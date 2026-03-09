import streamlit as st
import pandas as pd
import time

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SKYQUAD", layout="wide")

# --- 2. LOGIN MEMORY (Prevents Logout) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 3. LIVE DATABASE LINK ---
SID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
URL = f"https://docs.google.com/spreadsheets/d/{SID}/export?format=csv"

# --- 4. HIGH-CONTRAST STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    h1, h2, h3, p, span, label, .stMetric { 
        color: white !important; 
        font-weight: bold !important;
        text-shadow: 2px 2px 5px black;
    }
    .stDataFrame { 
        background-color: rgba(0,0,0,0.8) !important; 
        border: 2px solid #38bdf8 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. ACCESS KEYS ---
KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 6. MAIN LOGIC ---
if not st.session_state.logged_in:
    # --- LOGIN SCREEN ---
    st.markdown("<h1>🔐 SKYQUAD SECURITY ACCESS</h1>", unsafe_allow_html=True)
    
    role = st.selectbox("OPERATIONAL ROLE", list(KEYS.keys()))
    pwd = st.text_input("SECURITY PASSKEY", type="password")
    
    if st.button("AUTHORIZE"):
        if pwd == KEYS.get(role):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Passkey")

else:
    # --- AUTHORIZED DASHBOARD ---
    with st.sidebar:
        st.write("🛰️ SYSTEM LIVE")
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # THE DATA BLOCK
    try:
        # Load fresh Excel data every 15 seconds
        df = pd.read_csv(URL)
        
        st.markdown("<h1>🚀 SKYQUAD COMMAND CENTER</h1>", unsafe_allow_html=True)
        
        # Display Metrics
        col1, col2 = st.columns(2)
        col1.metric("Total Records", len(df))
        col2.metric("Sync Status", "ACTIVE")

        # Search Bar (Simplified to prevent syntax errors)
        find = st.text_input("SEARCH DATABASE")
        if find:
            # Filter logic broken into simple parts
            search_str = str(find).lower()
            mask = df.astype(str).apply(lambda x: x.str.lower().contains(search_str)).any(axis=1)
            df = df[mask]
        
        # Display the Table
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.write("---")
        st.caption("Updating automatically every 15 seconds...")

        # --- 7. AUTO-REFRESH (This keeps the connection live) ---
        time.sleep(15)
        st.rerun()

    except Exception:
        st.error("Connection Error: Check Google Sheet Share settings.")
        time.sleep(5)
        st.rerun()
