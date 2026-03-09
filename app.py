import streamlit as st
import pandas as pd

# --- 1. SETUP ---
st.set_page_config(page_title="Purchase Report", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 SECURITY ACCESS")
    pwd = st.text_input("PASSWORD", type="password")
    if st.button("LOGIN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
else:
    st.title("PURCHASE NONBOM DAILY TRACKING REPORT")
    
    if st.button("🔄 REFRESH DATA"):
        st.rerun()

    try:
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() # Clean names

        # --- THE FIX: REMOVE DUPLICATE COLUMNS ---
        # This removes the extra 'PLANT' column that is causing the 1-dimensional error
        df = df.loc[:, ~df.columns.duplicated()]

        # --- 2. SUMMARY REPORT (The Small Table) ---
        st.subheader("📊 SUMMARY REPORT")
        
        # We use your exact CAPS headers: PLANT, PR RECEIPT, PO DONE
        if 'PLANT' in df.columns:
            # Count PRs and Count POs that are finished
            summary = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            # Calculate Balance
            summary['BALANCED PR'] = summary['PR_REC'] - summary['PO_DN']
            
            # Serial Number & Column Naming
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Total Row Calculation
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR RECEIPT'].sum(), 
                summary['PO DONE'].sum(), 
                summary['BALANCED PR'].sum()
            ]], columns=summary.columns)

            # SHOW THE SMALL TABLE
            st.table(pd.concat([summary, total_row], ignore_index=True))
        else:
            st.warning(f"Header 'PLANT' not found. Available: {list(df.columns)}")

        # --- 3. DETAILED DATA REPORT ---
        st.divider()
        st.subheader("📂 DETAILED DATA REPORT")
