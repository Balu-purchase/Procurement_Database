import streamlit as st
import pandas as pd

# --- 1. SETUP ---
st.set_page_config(page_title="Purchase Report", layout="wide")

# Login Check
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
    # --- 2. DATA LOADING ---
    st.title("PURCHASE NONBOM DAILY TRACKING REPORT")
    
    # Refresh Button (Replaces the auto-timer to prevent blank screens)
    if st.button("🔄 REFRESH DATA"):
        st.rerun()

    try:
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() # Clean column names

        # --- 3. SUMMARY REPORT (Small Table) ---
        st.subheader("📊 SUMMARY REPORT")
        
        # Exact headers from your Excel: 'PLANT', 'PR RECEIPT', 'PO DONE'
        if 'PLANT' in df.columns:
            # Aggregate counts from the detailed data
            summary = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            # Math: Balance = Total PRs - POs Finished
            summary['BALANCED PR'] = summary['PR_REC'] - summary['PO_DN']
            
            # Serial Number
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Total Row
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR RECEIPT'].sum(), 
                summary['PO DONE'].sum(), 
                summary['BALANCED PR'].sum()
            ]], columns=summary.columns)

            # Display the small summary table
            st.table(pd.concat([summary, total_row], ignore_index=True))
        else:
            st.warning(f"Column 'PLANT' not found. Found these instead: {list(df.columns)}")

        # --- 4. DETAILED DATA REPORT ---
        st.divider()
        st.subheader("📂 DETAILED DATA REPORT")
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"⚠️ DATA CONNECTION ERROR: {e}")
        st.info("Check if the Google Sheet is set to 'Anyone with the link can view'.")
