import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Executive Procurement Summary", layout="wide")

# 2. PROFESSIONAL 3D INDUSTRIAL BACKGROUND (STABLE IMAGE)
# Using a high-quality 3D industrial render as a background
bg_img = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)), url("{bg_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Summary Table: Modern 'Glass' Look */
    .stTable {{
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }}
    h1 {{
        color: #1e293b;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 800;
        padding: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 3. LOGIN GATEWAY
if not st.session_state.auth:
    st.markdown("<h1>🔐 PROCUREMENT GATEWAY</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        pwd = st.text_input("MANAGEMENT KEY", type="password")
        if st.button("AUTHORIZE", use_container_width=True):
            if pwd in ["BOM2026", "NBOM2026", "GM789"]:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Key")

# 4. MAIN DASHBOARD
else:
    st.markdown("<h1>🏭 PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
    
    # Refresh Button
    if st.sidebar.button("🔄 REFRESH DATA"):
        st.rerun()

    try:
        # Load Google Sheets Data
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SUMMARY SECTION ---
        st.markdown("<h3 style='text-align:center;'>📊 STRATEGIC PLANT SUMMARY</h3>", unsafe_allow_html=True)
        
        if 'PLANT' in df.columns:
            # Grouping Logic
            sm = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            sm['BALANCED PR'] = sm['PR_REC'] - sm['PO_DN']
            sm.insert(0, 'S.NO', range(1, len(sm) + 1))
            sm.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Calculate Totals
            t1, t2, t3 = sm['PR RECEIPT'].sum(), sm['PO DONE'].sum(), sm['BALANCED PR'].sum()
            tr = pd.DataFrame([['', 'TOTAL', t1, t2, t3]], columns=sm.columns)

            # Display the Table
            st.table(pd.concat([sm, tr], ignore_index=True))
        
        # --- DETAILED DATA ---
        st.divider()
        st.markdown("<h3 style='text-align:center;'>📂 DETAILED DATA REPORT</h3>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error("⚠️ System Syncing... Please wait.")
        st.stop()
