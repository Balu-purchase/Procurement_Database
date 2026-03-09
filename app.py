import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Executive Procurement Summary", layout="wide")

# 2. FULL-SCREEN BEAUTIFUL 3D BACKGROUND
# We use a peaceful, high-quality industrial factory loop
st.markdown("""
    <style>
    .stApp {
        background: transparent;
    }
    #myVideo {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        opacity: 0.12; /* Subtle visibility for a clean look */
    }
    .stTable {
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 10px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.15);
    }
    h1 {
        color: #0F172A;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        padding: 20px;
    }
    </style>
    <video autoplay muted loop id="myVideo">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-top-view-of-a-large-factory-warehouse-34407-large.mp4" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 3. LOGIN
if not st.session_state.auth:
    st.markdown("<h1>🔐 MANAGEMENT ACCESS</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Enter Management Key", type="password")
    if st.button("SIGN IN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied")
# 4. DASHBOARD
else:
    st.markdown("<h1>🏭 PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔄 REFRESH DATABASE", use_container_width=True):
            st.rerun()

    try:
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SUMMARY SECTION ---
        st.markdown("<h3 style='text-align:center; color:#334155;'>📊 STRATEGIC SUMMARY</h3>", unsafe_allow_html=True)
        
        if 'PLANT' in df.columns:
            # Calculation: Collecting data from details below
            summary = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
