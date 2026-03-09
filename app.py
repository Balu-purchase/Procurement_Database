import streamlit as st
import pandas as pd
import time

# --- 1. SETUP & LOGIN ---
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
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() # Clean column names

        st.markdown("<h1 style='text-align:center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)

        # --- 3. SMALL SUMMARY TABLE (Top Section) ---
        st.subheader("📊 SUMMARY REPORT")
        
        if 'PLANT' in df.columns:
            # This "collects" data from the detailed list below
            # Count PRs and Count non-empty PO entries
            summary = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            # Calculation: Balance = PR - PO
            summary['BALANCED PR'] = summary['PR_REC'] - summary['PO_DN']
            
            # Add S.NO
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Add TOTAL row at the bottom of the summary
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR RECEIPT'].sum(), 
                summary['PO DONE'].sum(), 
                summary['BALANCED PR'].sum()
            ]], columns=summary.columns)

            st.table(pd.concat([summary, total_row], ignore_index=True))
        else:
            st.error("Column 'PLANT' not found in Excel.")

        # --- 4. DETAILED DATA REPORT (Bottom Section) ---
        st.divider()
        st.subheader("📂 DETAILED DATA REPORT")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # --- 5. AUTO-REFRESH (15 Seconds) ---
        time.sleep(15)
        st.rerun()

    except Exception as e:
        st.info("🔄 Syncing latest data from Google Sheets...")
        time.sleep(5)
