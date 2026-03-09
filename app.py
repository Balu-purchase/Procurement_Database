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
    # --- 2. DATA PROCESSING ---
    try:
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() # Clean column headers

        st.markdown("<h1 style='text-align:center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)

        # --- 3. SUMMARY REPORT SECTION ---
        st.subheader("📊 SUMMARY REPORT")
        
        # We use the exact headers found in your Excel: PLANT, PR RECEIPT, PO DONE
        if 'PLANT' in df.columns:
            # Group by Plant and count occurrences
            summary = df.groupby('PLANT').agg(
                PR_RECEIPT=('PR RECEIPT', 'count'),
                PO_DONE=('PO DONE', 'count')
            ).reset_index()

            # Logic: Balance = Total PRs - POs Finished
            summary['BALANCED PR'] = summary['PR_RECEIPT'] - summary['PO_DONE']
            
            # Add Serial Number
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))

            # Add Total Row
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR_RECEIPT'].sum(), 
                summary['PO_DONE'].sum(), 
                summary['BALANCED PR'].sum()
            ]], columns=['S.NO', 'PLANT', 'PR_RECEIPT', 'PO_DONE', 'BALANCED PR'])

            # Combine and Display
            final_table = pd.concat([summary, total_row], ignore_index=True)
            st.table(final_table)
        else:
            st.error("Missing 'PLANT' column in Google Sheet.")

        # --- 4. DETAILED DATA SECTION ---
        st.divider()
        st.subheader("📂 DETAILED DATA LIST")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # --- 5. REFRESH ---
        time.sleep(15)
        st.rerun()

    except Exception as e:
        st.warning("🔄 Syncing latest data from Google Sheets...")
        time.sleep(5)
        st.rerun()
