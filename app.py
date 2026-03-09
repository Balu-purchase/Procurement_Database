import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Executive Portal", layout="wide")

# 2. USER DATABASE
USER_DB = {
    "management_01": "MGMT2026",
    "admin_procure": "ADMIN789",
    "procure_team": "NBOM2026"
}

# 3. PROFESSIONAL STYLING
bg_img = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("{bg_img}");
        background-size: cover; background-attachment: fixed;
    }}
    section[data-testid="stSidebar"] {{ background-color: #1e293b !important; color: white; }}
    .stTable {{
        width: auto !important; margin-left: auto; margin-right: auto;
        background-color: white !important; border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }}
    h1 {{ color: #0F172A; text-align: center; font-weight: 800; }}
    </style>
    """, unsafe_allow_html=True)

# 4. LOGIN SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""

# 5. SIDEBAR LOGIN
st.sidebar.title("🔐 USER ACCESS")

if not st.session_state.auth:
    u_in = st.sidebar.text_input("USER ID")
    p_in = st.sidebar.text_input("PASSWORD", type="password")
    
    if st.sidebar.button("LOG IN", use_container_width=True):
        if u_in in USER_DB and USER_DB[u_in] == p_in:
            st.session_state.auth = True
            st.session_state.user = u_in
            st.rerun()
        else:
            st.sidebar.error("❌ Access Denied")
    
    st.warning("Authorized Access Only. Please login via Sidebar.")

# 6. PROTECTED DASHBOARD
else:
    st.sidebar.success(f"User: {st.session_state.user.upper()}")
    if st.sidebar.button("LOG OUT"):
        st.session_state.auth = False
        st.rerun()

    st.markdown("<h1>🏭 PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
    
    try:
        url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # --- SUMMARY SECTION ---
        st.markdown("<h3 style='text-align:center;'>📊 STRATEGIC PLANT SUMMARY</h3>", unsafe_allow_html=True)
        
        if 'PLANT' in df.columns:
            # Grouping and counting logic
            sm = df.groupby('PLANT').agg(
                PR_REC=('PR RECEIPT', 'count'),
                PO_DN=('PO DONE', 'count')
            ).reset_index()

            sm['BALANCED PR'] = sm['PR_REC']
