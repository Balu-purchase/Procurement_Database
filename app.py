import streamlit as st
import pandas as pd

# 1. PAGE SETUP (Executive Wide Layout)
st.set_page_config(page_title="Executive Procurement Summary", layout="wide")

# CUSTOM CSS: Professional Management Theme
st.markdown("""
    <style>
    /* Professional White Background */
    .stApp {
        background-color: #FFFFFF;
        color: #1E293B;
    }
    /* Summary Table: Centered, Clean, and Fit-to-Content */
    .stTable {
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    /* Executive Headers */
    h1 {
        color: #0F172A;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        text-align: center;
        padding-bottom: 10px;
    }
    h3 {
        color: #334155;
        text-align: center;
        border-bottom: 2px solid #3B82F6;
        display: inline-block;
        width: 100%;
        padding-bottom: 5px;
    }
    /* Center the Animation */
    .img-container {
        display: flex;
        justify-content: center;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 2. LOGIN SECTION
if not st.session_state.auth:
    st.markdown("<h1>🔐 AUTHORIZED ACCESS ONLY</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Enter Management Key", type="password")
    if st.button("SIGN IN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid Credentials")

# 3. MAIN EXECUTIVE DASHBOARD
else:
    # Small Professional Animation as a Header Logo
    st.markdown('<div class="img-container">', unsafe_allow_html=True)
    st.image("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJndXhscHJndXhscHJndXhscHJndXhscHJndXhscHJndXhscHJndXhscCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKMGpxVfFvT8KMo/giphy.gif", width=150)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h1>PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
    
    # Simple Refresh for Management
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔄 REFRESH REPORT"):
            st.rerun()

    try:
        # Load Data from Google Sheets
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
