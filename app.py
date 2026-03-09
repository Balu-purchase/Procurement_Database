import streamlit as st
import pandas as pd
import time

# --- 1. SETUP ---
st.set_page_config(page_title="Purchase Report", layout="wide")
if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("PASSWORD", type="password")
    if st.button("LOGIN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
else:
    try:
        # --- 2. LOAD DATA ---
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        # Reading data and ensuring no duplicate column names crash the app
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        
        # This fix handles the "1-dimensional" error by picking only unique columns
        df = df.loc[:, ~df.columns.duplicated()]

        st.markdown("<h2 style='text-align: center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h2>", unsafe_allow_html=True)

        # --- 3. THE CALCULATION ---
        # Look for the columns exactly as they appear in your Excel
        p_col = 'Plant'
        pr_col = 'PR Receipt'
        po_col = 'PO Done'

        if p_col in df.columns and pr_col in df.columns:
            st.markdown("### 📊 SUMMARY REPORT")
            
            # Grouping and Counting
            # We count PR Receipt to get total rows per plant
            # We count PO Done to see how many are completed
            summary = df.groupby(p_col).agg(
                PR_COUNT=(pr_col, 'count'),
                PO_COUNT=(po_col, 'count') if po_col in df.columns else (pr_col, lambda x: 0)
            ).reset_index()

            # Calculate Balance
            summary['BALANCE'] = summary['PR_COUNT'] - summary['PO_COUNT']

            # Add S.NO
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            
            # Rename for display
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCE PR']

            # Add Grand Total Row
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR RECEIPT'].sum(), 
                summary['PO DONE'].sum(), 
                summary['BALANCE PR'].sum()
            ]], columns=summary.columns)

            final_summary = pd.concat([summary, total_row], ignore_index=True)
            st.table(final_summary)
            
        else:
            st.error(f"Missing Columns! Found: {list(df.columns)}")

        # --- 4. DETAILED LIST ---
        st.divider()
        st.markdown("### 📂 DETAILED DATA LIST")
        st.dataframe(df, use_container_width=True, hide_index=True)

        time.sleep(15)
        st.rerun()

    except Exception as e:
        st.error(f"Syncing... {e}")
        time.sleep(5)
        st.rerun()
