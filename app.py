import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# --- CONFIGURATION ---
# Your WPS Office Cloud Link
WPS_LINK = "https://in.docworkspace.com/d/sIKXr38L0Aczgus0G?sa=601.1037"

st.set_page_config(page_title="Resolute Industrial Portal", layout="wide")

# --- LOGIN SYSTEM ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.sidebar.title("🔐 Secure Login")
    role = st.sidebar.selectbox("Select Team", ["BOM Team", "Non-BOM Team", "GM Management"])
    pwd = st.sidebar.text_input("Enter Passkey", type="password")
    
    if st.sidebar.button("Access Portal"):
        # Credentials check
        creds = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}
        if pwd == creds.get(role):
            st.session_state.authenticated = True
            st.session_state.role = role
            st.rerun()
        else:
            st.sidebar.error("❌ Incorrect Passkey")

# --- MAIN INTERFACE ---
else:
    st.title("🏭 Daily Procurement Tracking (LIVE)")
    st.sidebar.success(f"Connected: {st.session_state.role}")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # --- LIVE DATA FETCHING ---
    @st.cache_data(ttl=300)  # Automatically refreshes every 5 minutes
    def get_data_from_cloud(url):
        try:
            # We try to grab the file stream directly
            response = requests.get(url)
            # This reads the Excel file into memory
            # Note: If this still asks for openpyxl, you MUST run 'pip install openpyxl' once.
            return pd.read_excel(BytesIO(response.content))
        except Exception as e:
            st.error(f"Sync Error: {e}")
            return None

    df = get_data_from_cloud(WPS_LINK)

    if df is not None:
        st.info("✅ Data is live and synced with WPS Cloud.")
        
        # Search Bar
        search = st.text_input("🔍 Quick Search (Project, Vendor, or Status)")
        if search:
            # Filters the table based on your typing
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

        # Display Table
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Refresh Data Manual Button
        if st.button("🔄 Sync Latest Changes Now"):
            st.cache_data.clear()
            st.rerun()

    else:
        st.warning("⚠️ Could not reach the cloud file. Please check your internet or the link permissions.")

st.markdown("---")
st.caption("Resolute Electronics v3.0 | Auto-Sync Enabled")
