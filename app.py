import streamlit as st
import pandas as pd

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Purchase Report", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

# --- 2. LOGIN SECTION ---
if not st.session_state.auth:
    st.title("🔐 SECURITY ACCESS")
    pwd = st.text_input("PASSWORD", type="password")
    if st.button("LOGIN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid Password")

# --- 3. MAIN APPLICATION ---
else:
    st.markdown("<h1 style='text-align:center;'>PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
    
    if st.button("🔄 REFRESH DATA"):
        st.rerun()

    try:
        # Load Google Sheet
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        
        # Clean headers and remove duplicate columns (Fixes the '1-dimensional' error)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SUMMARY REPORT (TOP TABLE) ---
        st.subheader("📊 SUMMARY REPORT")
        
        if 'PLANT' in df.columns:
            # Aggregate data: Counting rows for PRs and POs
            summary = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            # Math: PR Count - PO Count
            summary['BALANCED PR'] = summary['PR_REC'] - summary['PO_DN']
            
            # S.NO and Formatting
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Total Row
            total_row = pd.DataFrame([[
                '', 'TOTAL', 
                summary['PR RECEIPT'].sum(), 
                summary['PO DONE'].sum(), 
                summary['BALANCED PR'].sum()
            ]], columns=summary.columns)

            st.table(pd.concat([summary, total_row], ignore_index=True))
        else:
            st.warning("Could not find 'PLANT' column in the Excel file.")

        # --- DETAILED DATA REPORT (BOTTOM TABLE) ---
        st.divider()
        st.subheader("📂 DETAILED DATA REPORT")
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"⚠️
