import streamlit as st
import pandas as pd
import time

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Purchase Tracking Report", layout="wide")

# --- 2. SESSION MEMORY ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 3. LIVE DATABASE LINK ---
# Ensure your Google Sheet is shared as "Anyone with link can view"
SID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
URL = f"https://docs.google.com/spreadsheets/d/{SID}/export?format=csv"

# --- 4. ACCESS KEYS ---
KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 5. APP LOGIC ---
if not st.session_state.logged_in:
    # --- LOGIN SCREEN ---
    st.title("🔐 SECURITY ACCESS")
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
        st.success("SYSTEM LIVE")
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    try:
        # Load Data from Google Sheets
        df = pd.read_csv(URL)
        
        st.header("PURCHASE NONBOM DAILY TRACKING REPORT")
        
        # --- 6. SUMMARY REPORT SECTION ---
        # Required columns for the summary table
        cols = ['Plant', 'PR Receipt', 'PO Done', 'Balance PR']
        
        if all(c in df.columns for c in cols):
            st.subheader("📊 Summary Report (Plant-wise)")
            
            # Convert columns to numbers (handling errors)
            temp_df = df.copy()
            for c in ['PR Receipt', 'PO Done', 'Balance PR']:
                temp_df[c] = pd.to_numeric(temp_df[c], errors='coerce').fillna(0)
            
            # Group by Plant and Sum
            summary = temp_df.groupby('Plant')[['PR Receipt', 'PO Done', 'Balance PR']].sum().reset_index()
            
            # Add Total Row
            totals = summary[['PR Receipt', 'PO Done', 'Balance PR']].sum()
            total_row = pd.DataFrame([['TOTAL', totals[0], totals[1], totals[2]]], columns=cols)
            final_summary
