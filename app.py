import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resolute Procurement Portal", layout="wide")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
if "data" not in st.session_state:
    st.session_state.data = None

# --- LOGIN SYSTEM ---
if not st.session_state.authenticated:
    st.sidebar.title("🔐 Secure Access")
    role = st.sidebar.selectbox("Select Your Team", ["BOM Team", "Non-BOM Team", "GM Management"])
    pwd = st.sidebar.text_input("Enter Team Passkey", type="password")
    
    if st.sidebar.button("Login"):
        # Credentials
        creds = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}
        if pwd == creds.get(role):
            st.session_state.authenticated = True
            st.session_state.role = role
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid Passkey")

# --- MAIN DASHBOARD ---
else:
    st.sidebar.success(f"Logged in: {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.data = None
        st.rerun()

    st.title("🏭 Daily Procurement Tracking")
    
    # --- STEP 1: DATA SOURCE ---
    if st.session_state.data is None:
        st.info("👋 Welcome! Since SharePoint is restricted, please upload the latest 'Procurement_Database.xlsx' file to start.")
        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
        
        if uploaded_file:
            try:
                # Load the data into the session so it stays there while you work
                st.session_state.data = pd.read_excel(uploaded_file, engine='openpyxl')
                st.success("✅ Database Loaded Successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    # --- STEP 2: DISPLAY DATA & TOOLS ---
    else:
        df = st.session_state.data

        # Global Search
        search = st.text_input("🔍 Search by Project Name, Part Number, or Vendor:")
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

        # Tabs for better organization
        tab1, tab2 = st.tabs(["📊 Live Tracking Table", "🛠️ Action Center"])

        with tab1:
            st.subheader("Current Procurement Status")
            st.dataframe(df, use_container_width=True, hide_index=True)

        with tab2:
            if st.session_state.role == "Non-BOM Team":
                st.subheader("💰 Price Approval Request")
                col1, col2 = st.columns(2)
                with col1:
                    item_id = st.text_input("Item ID / Description")
                    current_price = st.number_input("Current Price", min_value=0.0)
                with col2:
                    new_price = st.number_input("Revised Price", min_value=0.0)
                    vendor = st.text_input("Vendor Name")
                
                if st.button("Submit for GM Review"):
                    st.toast(f"Request for {item_id} sent to GM Management!")

            elif st.session_state.role == "GM Management":
                st.subheader("📈 Management Overview")
                st.metric("Total Items Tracked", len(df))
                st.info("Review pending approvals in the table below.")
                # You could add charts here later

            else:
                st.info("BOM Team: Reviewing mode active. Select items in the table to see details.")

# --- FOOTER ---
st.markdown("---")
st.caption("Resolute Electronics - Industrial Tracking Portal v2.0 (Local Upload Mode)")
