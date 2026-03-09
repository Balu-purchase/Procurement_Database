import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skyquad Electronics | Procurement", layout="wide")

# --- CUSTOM CSS (The "Ultra-Impressive" Design) ---
st.markdown("""
    <style>
    /* 1. Industrial Background Image */
    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.85)), 
                    url("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* 2. Floating Watermark */
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        opacity: 0.15;
        font-size: 2.5rem;
        color: white;
        transform: rotate(-15deg);
        z-index: -1;
        font-weight: 900;
        pointer-events: none;
    }

    /* 3. Glass-morphism Cards */
    div[data-testid="stMetric"], div.stDataFrame, .stAlert {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        color: white !important;
    }

    /* 4. Glowing Title */
    h1 {
        color: #60a5fa !important;
        text-shadow: 0 0 15px rgba(96, 165, 250, 0.5);
        font-size: 3rem !important;
        text-align: center;
        letter-spacing: 2px;
    }

    /* 5. Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 30, 0.95) !important;
        border-right: 1px solid #3b82f6;
    }
    
    input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid #3b82f6 !important;
    }
    </style>
    
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.sidebar.markdown("### 🔐 SKYQUAD SECURE ACCESS")
    role = st.sidebar.selectbox("Select Your Unit", ["BOM Team", "Non-BOM Team", "GM Management"])
    pwd = st.sidebar.text_input("Access Key", type="password")
    
    if st.sidebar.button("ENTER PORTAL"):
        creds = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}
        if pwd == creds.get(role):
            st.session_state.auth = True
            st.session_state.role = role
            st.rerun()
        else:
            st.sidebar.error("Access Denied")

# --- MAIN DASHBOARD ---
else:
    st.sidebar.markdown(f"## SKYQUAD PORTAL")
    st.sidebar.info(f"User: {st.session_state.role}")
    
    if st.sidebar.button("EXIT PORTAL"):
        st.session_state.auth = False
        st.rerun()

    st.markdown("<h1>SKYQUAD ELECTRONICS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Industrial Procurement & Supply Chain Command Center</p>", unsafe_allow_html=True)

    st.divider()

    uploaded_file = st.file_uploader("Upload 'Procurement_Database.csv'", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Line Items", f"{len(df)} Units")
        with c2:
            st.metric("Vendor Count", f"{len(df.iloc[:, 1].unique()) if len(df.columns) > 1 else 'N/A'}")
        with c3:
            st.metric("System Health", "CONNECTED")

        st.markdown("---")
        search = st.text_input("🔍 Filter Database")
        
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            
        st.dataframe(df, use_container_width=True)
    else:
        st.info("👋 System Ready. Awaiting CSV Database Upload...")
