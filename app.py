import streamlit as st
import pandas as pd

# 1. PAGE SETUP & 3D INDUSTRIAL STYLING
st.set_page_config(page_title="Procurement Control Center", layout="wide")

# CUSTOM CSS: Dark Industrial Theme + Fit-to-Content Tables
st.markdown("""
    <style>
    /* Dark Industrial Background */
    .stApp {
        background-color: #1a1c23;
        color: #ffffff;
    }
    /* Summary Table: Fit to Text Length */
    .stTable {
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        border: 2px solid #4e5d6c;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #00d4ff !important;
        text-align: center;
        font-family: 'Orbitron', sans-serif;
    }
    /* Video Container */
    .video-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 2. LOGIN SECTION
if not st.session_state.auth:
    st.markdown("<h1>🔐 PROCUREMENT GATEWAY</h1>", unsafe_allow_html=True)
    pwd = st.text_input("AUTHORIZATION KEY", type="password")
    if st.button("ACCESS SYSTEM"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied")

# 3. MAIN DASHBOARD
else:
    # --- INDUSTRIAL 3D ANIMATION HEADER ---
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    # This is a high-quality industrial 3D loop placeholder
    st.video("https://www.youtube.com/watch?v=9_pY033X0-g") # 3D Factory Animation
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h1>🏭 PURCHASE NONBOM TRACKING CENTER</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔄 REFRESH LIVE DATABASE", use_container_width=True):
            st.rerun()

    try:
        # Load Google Sheet
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SMALL SUMMARY TABLE (Fit to Content) ---
        st.markdown("### 📊 STRATEGIC SUMMARY")
        
        if 'PLANT' in df.columns:
            summary = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            summary['BALANCED PR'] = summary['PR_REC'] - summary['PO_DN']
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Grand Totals
            t_pr, t_po, t_bal = summary['PR RECEIPT'].sum(), summary['PO DONE'].sum(), summary['BALANCED PR'].sum()
            total_row = pd.DataFrame([['', 'TOTAL', t_pr, t_po, t_bal]], columns=summary.columns)

            # Displaying the "Fit-to-Text" Table
            st.table(pd.concat([summary, total_row], ignore_index=True))
        else:
            st.warning("PLANT header missing.")

        # --- DETAILED DATA REPORT ---
        st.divider()
        st.markdown("### 📂 DETAILED PROCUREMENT LOG")
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"System Error: {e}")
