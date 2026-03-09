import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Procurement Center", layout="wide")

# CUSTOM CSS: Dark Theme + Fit-to-Content Table
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .stTable { 
        width: auto !important; 
        margin-left: auto; 
        margin-right: auto; 
        background-color: #1e293b; 
    }
    h1, h3 { color: #38bdf8 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 2. LOGIN
if not st.session_state.auth:
    st.title("🔐 PROCUREMENT GATEWAY")
    pwd = st.text_input("PASSWORD", type="password")
    if st.button("LOGIN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
else:
    # 3. INDUSTRIAL ANIMATION & HEADER
    # This link is shortened to prevent the "Unterminated String" error
    img_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJndXhscHJndXhscHJndXhscHJndXhscHJndXhscHJndXhscHJndXhscCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKMGpxVfFvT8KMo/giphy.gif"
    
    st.image(img_url, width=300)
    st.markdown("<h1>🏭 PURCHASE NONBOM TRACKING CENTER</h1>", unsafe_allow_html=True)
    
    if st.button("🔄 REFRESH DATA"):
        st.rerun()

    try:
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SUMMARY REPORT (Fits to Text) ---
        st.markdown("### 📊 STRATEGIC SUMMARY")
        
        if 'PLANT' in df.columns:
            summary = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            summary['BALANCED PR'] = summary['PR_REC'] - summary['PO_DN']
            summary.insert(0, 'S.NO', range(1, len(summary) + 1))
            summary.columns = ['S.NO', 'PLANT', 'PR RECEIPT', 'PO DONE', 'BALANCED PR']

            # Totals
            t_pr, t_po, t_bal = summary['PR RECEIPT'].sum(), summary['PO DONE'].sum(), summary['BALANCED PR'].sum()
            total_row = pd.DataFrame([['', 'TOTAL', t_pr, t_po, t_bal]], columns=summary.columns)

            st.table(pd.concat([summary, total_row], ignore_index=True))
        
        # --- DETAILED DATA ---
        st.divider()
        st.markdown("### 📂 DETAILED PROCUREMENT LOG")
        st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error("System Refreshing...")
