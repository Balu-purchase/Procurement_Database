import streamlit as st
import pandas as pd
import time

# --- 1. SETUP ---
st.set_page_config(page_title="Purchase Tracking", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 2. DATA SOURCE ---
SHEET_ID = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- 3. ACCESS KEYS ---
KEYS = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}

# --- 4. MAIN APP ---
if not st.session_state.logged_in:
    st.title("🔐 SECURITY ACCESS")
    role = st.selectbox("ROLE", list(KEYS.keys()))
    pwd = st.text_input("PASSKEY", type="password")
    if st.button("AUTHORIZE"):
        if pwd == KEYS.get(role):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Key")
else:
    # Sidebar for logout
    with st.sidebar:
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # DATA PROCESSING BLOCK
    try:
        df = pd.read_csv(URL)
        st.header("PURCHASE NONBOM DAILY TRACKING REPORT")
        
        # --- SUMMARY SECTION ---
        # Columns must be exactly: 'Plant', 'PR Receipt', 'PO Done', 'Balance PR'
        target_cols = ['Plant', 'PR Receipt', 'PO Done', 'Balance PR']
        
        if all(col in df.columns for col in target_cols):
            st.subheader("📊 Summary Report (Plant-wise)")
            
            # Clean data: convert to numbers
            work_df = df.copy()
            for c in ['PR Receipt', 'PO Done', 'Balance PR']:
                work_df[c] = pd.to_numeric(work_df[c], errors='coerce').fillna(0)
            
            # Create the Summary Table
            summary = work_df.groupby('Plant')[['PR Receipt', 'PO Done', 'Balance PR']].sum().reset_index()
            
            # Calculate Totals for the bottom row
            t_pr = summary['PR Receipt'].sum()
            t_po = summary['PO Done'].sum()
            t_bal = summary['Balance PR'].sum()
            
            # Append Total row
            total_data = pd.DataFrame([['TOTAL', t_pr, t_po, t_bal]], columns=target_cols)
            final_table = pd.concat([summary, total_data], ignore_index=True)
            
            # Display as static table
            st.table(final_table)
        else:
            st.warning("Ensure Excel has columns: Plant, PR Receipt, PO Done, Balance PR")

        st.divider()
        
        # --- FULL DATA SECTION ---
        st.subheader("📂 Detailed Tracking Data")
        search = st.text_input("SEARCH DATABASE")
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        st.dataframe(df, use_container_width=True, hide_index=True)

        # AUTO-REFRESH (Every 20 seconds)
        time.sleep(20)
        st.rerun()

    except Exception as e:
        st.error(f"Sync Error: {e}")
        time.sleep(5)
        st.rerun()
