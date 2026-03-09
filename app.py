import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Purchase Report", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

# 2. LOGIN SECTION
if not st.session_state.auth:
    st.title("SECURITY ACCESS")
    pwd = st.text_input("PASSWORD", type="password")
    if st.button("LOGIN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid Password")

# 3. MAIN APPLICATION
else:
    st.header("PURCHASE NONBOM DAILY TRACKING REPORT")
    
    if st.button("REFRESH DATA"):
        st.rerun()

    try:
        # Load Google Sheet
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        
        # Clean headers and remove duplicate columns
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SUMMARY REPORT (TOP TABLE) ---
        st.subheader("SUMMARY REPORT")
        
        if 'PLANT' in df.columns:
            # Aggregate data: Counting rows for PRs and POs
            # This 'collects' data from the detailed list below
            summary = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            # Math: PR Count - PO Count = Balance
            summary['BALANCED PR'] = summary['PR_REC'] - summary['PO_DN']
            
            # S.NO and Formatting
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Total Row
            t_pr = summary['PR RECEIPT'].sum()
            t_po = summary['PO DONE'].sum()
            t_bal = summary['BALANCED PR'].sum()
            
            total_row = pd.DataFrame([['', 'TOTAL', t_pr, t_po, t_bal]], columns=summary.columns)

            # Display the Small Summary Table
            st.table(pd.concat([summary, total_row], ignore_index=True))
        else:
            st.warning("Could not find PLANT column.")

        # --- DETAILED DATA REPORT (BOTTOM TABLE) ---
        st.divider()
        st.subheader("DETAILED DATA REPORT")
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error("Data Connection Error")
        st.write(e)
