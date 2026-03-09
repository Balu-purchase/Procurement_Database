import streamlit as st
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
    try:
        # --- 2. LOAD DATA ---
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        
        # Clean headers to ensure no hidden spaces
        df.columns = df.columns.str.strip()

        st.markdown("<h1 style='text-align: center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)

        # --- 3. THE SUMMARY CALCULATION ---
        # Match your exact CAPS headers: 'PLANT', 'PR RECEIPT', 'PO DONE'
        if 'PLANT' in df.columns:
            st.markdown("### 📊 SUMMARY REPORT")

            # We group by PLANT
            # PR RECEIPT: Counts every row for that plant
            # PO DONE: Counts only cells that have a value (ignores empty/blank cells)
            summary = df.groupby('PLANT').agg(
                PR_COUNT=('PR RECEIPT', 'count'),
                PO_COUNT=('PO DONE', 'count')
            ).reset_index()

            # Calculate Balance (Total PRs - POs Finished)
            summary['BALANCED_PR'] = summary['PR_COUNT'] - summary['PO_COUNT']

            # Add S.NO
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            
            # Rename columns to match your preferred display
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Add Grand Total Row
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR RECEIPT'].sum(), 
                summary['PO DONE'].sum(), 
                summary['BALANCED PR'].sum()
            ]], columns=summary.columns)

            final_summary = pd.concat([summary, total_row], ignore_index=True)
            
            # Show the clean Summary Table
            st.table(final_summary)
            
        else:
            st.error("Column 'PLANT' not found. Please check your Excel headers.")

        # --- 4. DETAILED DATA LIST ---
        st.divider()
        st.markdown("### 📂 DETAILED DATA LIST")
        search = st.text_input("🔍 SEARCH DATA (Type Plant Name, Item, or Date)")
        
        if search:
            mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            display_df = df[mask]
        else:
            display_df = df

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # --- 5. AUTO-REFRESH (15 Seconds) ---
        time.sleep(15)
        st.rerun()

    except Exception as e:
        st.info("🔄 Syncing latest data from Google Sheets...")
        time.sleep(5)
        st.rerun()
