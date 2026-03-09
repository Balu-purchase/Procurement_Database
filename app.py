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
        df.columns = df.columns.str.strip() # Remove hidden spaces

        st.markdown("<h2 style='text-align: center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h2>", unsafe_allow_html=True)

        # --- 3. THE SUMMARY LOGIC ---
        if 'Plant' in df.columns:
            # We group by Plant so each Plant gets only ONE row
            # 'count' finds how many PRs exist
            # 'count' on PO Done finds how many POs are actually filled in
            summary = df.groupby('Plant').agg(
                PR_Receipt=('PR Receipt', 'count'),
                PO_Done=('PO Done', 'count')
            ).reset_index()

            # Calculate Balance (PR Receipt minus PO Done)
            summary['Balance_PR'] = summary['PR_Receipt'] - summary['PO_Done']

            # Add S.No Column
            summary.insert(0, 'S.No', range(1, len(summary) + 1))
            
            # Rename for display
            summary.columns = ['S.No', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCE PR']

            # Add Grand Total Row
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR RECEIPT'].sum(), 
                summary['PO DONE'].sum(), 
                summary['BALANCE PR'].sum()
            ]], columns=summary.columns)

            final_summary = pd.concat([summary, total_row], ignore_index=True)

            # Display the Summary Table
            st.markdown("### 📊 SUMMARY REPORT")
            st.table(final_summary)
        else:
            st.error("Column 'Plant' not found. Please check your Excel header.")

        # --- 4. DETAILED DATA ---
        st.divider()
        st.markdown("### 📂 DETAILED DATA LIST")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # --- 5. AUTO-REFRESH ---
        time.sleep(15)
        st.rerun()

    except Exception as e:
        st.error("Updating Data...")
        time.sleep(5)
        st.rerun()
