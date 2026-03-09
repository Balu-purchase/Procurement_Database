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
        df = pd.read_csv(url)
        
        # CLEAN ALL HEADERS (Removes spaces and converts to lowercase for searching)
        df.columns = df.columns.str.strip()
        header_map = {col.lower(): col for col in df.columns}

        st.markdown("<h2 style='text-align: center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h2>", unsafe_allow_html=True)

        # --- 3. DYNAMIC COLUMN FINDER ---
        # This finds your columns even if you renamed them slightly
        plant_col = header_map.get('plant')
        pr_col = header_map.get('pr receipt')
        po_col = header_map.get('po done')

        if plant_col and pr_col and po_col:
            # Create the Summary (One row per Plant)
            # Count PRs and Count POs that are NOT empty
            summary = df.groupby(plant_col).agg(
                PR_COUNT=(pr_col, 'count'),
                PO_COUNT=(po_col, 'count')
            ).reset_index()

            # Logic: Balance = Total PRs - POs Done
            summary['BALANCE'] = summary['PR_COUNT'] - summary['PO_COUNT']

            # Add Serial Number
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            
            # Formatting for the table
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCE PR']

            # Add Total Row
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR RECEIPT'].sum(), 
                summary['PO DONE'].sum(), 
                summary['BALANCE PR'].sum()
            ]], columns=summary.columns)

            final_summary = pd.concat([summary, total_row], ignore_index=True)

            st.markdown("### 📊 SUMMARY REPORT")
            st.table(final_summary)
        else:
            # If columns are missing, show the user what names ARE in the Excel
            st.error("❌ COLUMN NAMES NOT MATCHING")
            st.write("Your Excel currently has these headers:", list(df.columns))
            st.info("Please ensure headers are: **Plant**, **PR Receipt**, and **PO Done**")

        # --- 4. DETAILED DATA ---
        st.divider()
        st.markdown("### 📂 DETAILED DATA LIST")
        st.dataframe(df, use_container_width=True, hide_index=True)

        time.sleep(15)
        st.rerun()

    except Exception as e:
        st.error(f"Updating Data... {e}")
        time.sleep(5)
        st.rerun()
