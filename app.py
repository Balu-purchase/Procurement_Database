import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Executive Dashboard", layout="wide")

# 2. BEAUTIFUL 3D BACKGROUND (15% Opacity for Professional Clarity)
st.markdown("""
    <style>
    .stApp { background: transparent; }
    #myVideo {
        position: fixed; right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1; opacity: 0.15;
    }
    .stTable {
        width: auto !important;
        margin-left: auto; margin-right: auto;
        background-color: rgba(255, 255, 255, 0.98);
        border-radius: 12px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.15);
    }
    h1 { color: #0F172A; text-align: center; font-weight: 800; padding: 20px; }
    </style>
    <video autoplay muted loop id="myVideo">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-top-view-of-a-large-factory-warehouse-34407-large.mp4" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 3. LOGIN GATEWAY
if not st.session_state.auth:
    st.markdown("<h1>🔐 AUTHORIZED ACCESS</h1>", unsafe_allow_html=True)
    pwd = st.text_input("PASSWORD", type="password")
    if st.button("LOGIN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
# 4. DASHBOARD
else:
    st.markdown("<h1>🏭 PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
    
    if st.button("🔄 REFRESH DATA"):
        st.rerun()

    try:
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SUMMARY SECTION (AUTO-CALCULATED) ---
        st.markdown("<h3 style='text-align:center;'>📊 STRATEGIC SUMMARY</h3>", unsafe_allow_html=True)
        
        if 'PLANT' in df.columns:
            # Grouping Logic
            sm = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            sm['BALANCED PR'] = sm['PR_REC'] - sm['PO_DN']
            sm.insert(0, 'S.NO', range(1, len(sm) + 1))
            sm.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Totals Logic (Short lines to prevent SyntaxErrors)
            t1, t2, t3 = sm['PR RECEIPT'].sum(), sm['PO DONE'].sum(), sm['BALANCED PR'].sum()
            tr = pd.DataFrame([['', 'TOTAL', t1, t2, t3]], columns=sm.columns)

            st.table(pd.concat([sm, tr], ignore_index=True))
        
        # --- DETAILED LOG ---
        st.divider()
        st.markdown("<h3 style='text-align:center;'>📂 DETAILED DATA REPORT</h3>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.info("🔄 Synchronizing with Cloud Database...")
