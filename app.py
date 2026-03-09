import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Executive Dashboard", layout="wide")

# 2. FULL-SCREEN 3D INDUSTRIAL BACKGROUND
# Clean, bright factory floor animation (12% visibility for text clarity)
st.markdown("""
    <style>
    .stApp { background: transparent; }
    #myVideo {
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1; opacity: 0.12;
    }
    .stTable {
        width: auto !important;
        margin-left: auto; margin-right: auto;
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 12px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
    }
    h1 { color: #0F172A; text-align: center; font-weight: 800; padding: 20px; }
    h3 { color: #334155; text-align: center; }
    </style>
    <video autoplay muted loop id="myVideo">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-top-view-of-a-large-factory-warehouse-34407-large.mp4" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 3. LOGIN GATEWAY
if not st.session_state.auth:
    st.markdown("<h1>🔐 PROCUREMENT GATEWAY</h1>", unsafe_allow_html=True)
    pwd = st.text_input("ENTER MANAGEMENT KEY", type="password")
    if st.button("SIGN IN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Invalid Credentials")

# 4. MAIN EXECUTIVE DASHBOARD
else:
    st.markdown("<h1>🏭 PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
    
    if st.button("🔄 REFRESH LIVE DATABASE"):
        st.rerun()

    try:
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SUMMARY SECTION (AUTO-CALCULATED FROM DETAILS) ---
        st.markdown("### 📊 STRATEGIC SUMMARY")
        
        if 'PLANT' in df.columns:
            # Grouping and Counting
            smry = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            smry['BALANCED PR'] = smry['PR_REC'] - smry['PO_DN']
            smry.insert(0, 'S.NO', range(1, len(smry) + 1))
            smry.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Grand Totals
            t_pr, t_po, t_bal = smry['PR RECEIPT'].sum(), smry['PO DONE'].sum(), smry['BALANCED PR'].sum()
            tot_row = pd.DataFrame([['', 'TOTAL', t_pr, t_po, t_bal]],
