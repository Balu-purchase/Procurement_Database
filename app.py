import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# --- CONFIGURATION ---
# This is a modified version of your link to trigger a direct file stream
# We extracted the unique ID from your original link
FILE_ID = "F2846EF8-4072-48E3-AE3B-A9848FA1578F"
LIVE_URL = f"https://resolutegroups-my.sharepoint.com/:x:/g/personal/purchase_resoluteelectronics_com/_layouts/15/download.aspx?SourceDoc=%7B{FILE_ID}%7D"

st.set_page_config(page_title="Resolute Live Tracker", layout="wide")

# --- LOGIN ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    role = st.sidebar.selectbox("Team", ["BOM Team", "Non-BOM Team", "GM Management"])
    pwd = st.sidebar.text_input("Passkey", type="password")
    if st.sidebar.button("Login"):
        if (role == "BOM Team" and pwd == "BOM2026") or \
           (role == "Non-BOM Team" and pwd == "NBOM2026") or \
           (role == "GM Management" and pwd == "GM789"):
            st.session_state.auth = True
            st.rerun()

# --- MAIN LIVE INTERFACE ---
else:
    st.title("🏭 Real-Time Procurement Tracking")
    
    # Refresh Button
    if st.button("🔄 Refresh Data Now"):
        st.cache_data.clear()
        st.rerun()

    try:
        # This function fetches the file LIVE from your SharePoint
        @st.cache_data(ttl=60) # Automatically refreshes every 60 seconds
        def fetch_live_data():
            response = requests.get(LIVE_URL)
            # If SharePoint blocks this, it will jump to the 'except' block below
            return pd.read_excel(BytesIO(response.content))

        df = fetch_live_data()
        
        st.success("✅ Connected to Live SharePoint Database")
        
        # Search Filter
        search = st.text_input("🔍 Search Live Data")
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error("❌ Live Sync Failed: SharePoint Security Block")
        st.warning("""
        Your company's SharePoint security requires a manual login. 
        Because I cannot 'Log In' as a human, you have two choices:
        1. Ask IT to enable 'Anyone with the link' for this specific file.
        2. Use the 'Manual Upload' method we discussed earlier.
        """)
