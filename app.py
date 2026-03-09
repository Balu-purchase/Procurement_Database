import streamlit as st
import pd as pd
import pandas as pd
import time

# --- 1. SETUP ---
st.set_page_config(page_title="Purchase Report", layout="wide")
if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🔐 SECURITY ACCESS</h2>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password")
    if st.button("LOGIN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
else:
    # --- 2. DATA LOADING ---
    url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
    
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() # Clean column names

        st.markdown("<h1 style='text-align: center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)

        # --- 3. SUMMARY REPORT SECTION ---
        st.markdown("### 📊 SUMMARY REPORT")
        
        if 'PLANT' in df.columns:
            # We group by PLANT and calculate counts
            # count() only counts non-empty cells
            summary = df.groupby('PLANT').agg(
                PR_RECEIPT=('PR RECEIPT', 'count'),
                PO_DONE=('PO DONE', 'count')
            ).reset_index()

            # Calculate the Balance
            summary['BALANCED PR'] = summary['PR_RECEIPT'] - summary['PO_DONE']

            # Add Serial Number (S.NO)
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            
            # Create Total Row
            total_pr = summary['PR_RECEIPT'].sum()
            total_po = summary['PO_DONE'].sum()
            total_bal = summary['BALANCED PR'].sum()
            
            total_row = pd.DataFrame([['', 'TOTAL', total_pr, total_po, total_bal]], 
                                     columns=['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR'])

            # Combine Summary and Total
            final_summary = pd.concat([summary, total_row], ignore_index=True)
            
            # DISPLAY THE TABLE
            st.table(final_summary)
        else:
            st.error("Error: Could not find 'PL
