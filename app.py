import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resolute Procurement Portal", layout="wide")

# --- CUSTOM CSS (The "Beautiful" Part) ---
st.markdown("""
    <style>
    /* Background and overall font */
    .stApp {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        color: white;
    }
    
    /* Heading style */
    h1 {
        color: #0f172a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 10px;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Customizing buttons */
    .stButton>button {
        border-radius: 8px;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.sidebar.markdown("## 🔐 Portal Security")
    role = st.sidebar.selectbox("Select Team", ["BOM Team", "Non-BOM Team", "GM Management"])
    pwd = st.sidebar.text_input("Passkey", type="password")
    
    if st.sidebar.button("Login to Dashboard"):
        if (role == "BOM Team" and pwd == "BOM2026") or \
           (role == "Non-BOM Team" and pwd == "NBOM2026") or \
           (role == "GM Management" and pwd == "GM789"):
            st.session_state.auth = True
            st.session_state.role = role
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid Passkey")

# --- MAIN DASHBOARD ---
else:
    # Top Header Section
    col_title, col_logo = st.columns([4, 1])
    with col_title:
        st.title("🏭 Industrial Procurement Tracking")
        st.subheader(f"Welcome back, {st.session_state.role}")
    
    # Sidebar Info
    st.sidebar.success(f"Online: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    # --- DATA UPLOAD ---
    st.markdown("### 📥 Data Sync")
    uploaded_file = st.file_uploader("Upload 'Procurement_Database.csv' for real-time analysis", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # --- KEY PERFORMANCE METRICS ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Line Items", len(df))
        m2.metric("Active Vendors", len(df.iloc[:, 1].unique()) if len(df.columns)>1 else "N/A")
        m3.metric("Database Status", "Live/Healthy")
        
        st.divider()

        # --- DATA VIEW ---
        col_search, col_filter = st.columns([2, 1])
        with col_search:
            search = st.text_input("🔍 Search Database (Project, Part, or Status)")
        
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            
        st.markdown("#### 📋 Procurement Data Table")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.warning("Please upload the CSV file to populate the dashboard metrics.")
        
        # Visual placeholder when no data is uploaded
        st.info("💡 Tip: Export your SharePoint file as CSV for the fastest, most reliable experience.")

st.markdown("---")
st.caption("© 2026 Resolute Electronics - High Precision Industrial Tracking")
