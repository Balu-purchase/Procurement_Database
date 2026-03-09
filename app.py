import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Executive Portal", layout="wide")

# 2. USER DATABASE
USER_DB = {"BOMTEAM": "BOM2026", "NONBOM TEAM": "NONBOM 2026", "HOD": "SCM"}

# 3. BACKGROUND STYLING
bg_img = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
.stApp {{ background-image: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), url("{bg_img}"); background-size: cover; background-attachment: fixed; }}
section[data-testid="stSidebar"] {{ background-color: #1e293b !important; color: white; }}
.stTable {{ width: auto !important; margin: auto; background-color: white !important; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
h1 {{ color: #0F172A; text-align: center; font-weight: 800; }}
</style>
""", unsafe_allow_html=True)

# 4. AUTHENTICATION LOGIC
if "auth" not in st.session_state:
    st.session_state.auth = False

# SIDEBAR LOGIN UI
st.sidebar.title("🔐 USER ACCESS")
if not st.session_state.auth:
    u_in = st.sidebar.text_input("USER ID")
    p_in = st.sidebar.text_input("PASSWORD", type="password")
    if st.sidebar.button("LOG IN", use_container_width=True):
        if u_in in USER_DB and USER_DB[u_in] == p_in:
            st.session_state.auth = True
            st.rerun()
        else:
            st.sidebar.error("❌ Access Denied")
    st.warning("Please login via Sidebar to view the Industrial Report.")
    st.stop() # Stops execution here if not logged in

# 5. PROTECTED CONTENT (Only runs if logged in)
st.sidebar.success("✅ AUTHORIZED ACCESS")
if st.sidebar.button("LOG OUT"):
    st.session_state.auth = False
    st.rerun()

st.markdown("<h1>🏭 PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)

# DATA LOADING (Outside try/except for simplicity)
try:
    url = "https://docs.google.com/spreadsheets/d/1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4/export?format=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated()]
    
    # --- SUMMARY SECTION ---
    st.markdown("<h3 style='text-align:center;'>📊 STRATEGIC PLANT SUMMARY</h3>", unsafe_allow_html=True)
    
    if 'PLANT' in df.columns:
        # Grouping
        sm = df.groupby('PLANT').agg(PR_REC=('PR RECEIPT', 'count'), PO_DN=('PO DONE', 'count')).reset_index()
        # Calculation
        sm['BALANCED PR'] = sm['PR_REC'] - sm['PO_DN']
        sm.insert(0, 'S.NO', range(1, len(sm) + 1))
        # Totals
        t1, t2, t3 = sm['PR_REC'].sum(), sm['PO_DN'].sum(), sm['BALANCED PR'].sum()
        tr = pd.DataFrame([['', 'TOTAL', t1, t2, t3]], columns=sm.columns)
        # Display
        st.table(pd.concat([sm, tr], ignore_index=True))
    
    # --- DETAILS ---
    st.divider()
    st.markdown("<h3 style='text-align:center;'>📂 DETAILED DATA LOG</h3>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"System Refreshing... Status: {e}")
