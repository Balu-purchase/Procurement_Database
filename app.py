import streamlit as st
import pandas as pd

# I have converted your SharePoint link to a direct download format below:
CSV_URL = "https://resolutegroups-my.sharepoint.com/:x:/g/personal/purchase_resoluteelectronics_com/IQD4boTyckDjSK47qYSPoVePAU6YtB8si6lcbj3i--PrWaU?download=1"

st.set_page_config(page_title="Industrial Tracking Portal", layout="wide")

# --- LOGIN SYSTEM ---
st.sidebar.title("🔐 Secure Login")
user_role = st.sidebar.selectbox("Select Team", ["BOM Team", "Non-BOM Team", "GM Management"])
password = st.sidebar.text_input("Enter Passkey", type="password")

access = False
if user_role == "BOM Team" and password == "BOM2026":
    access = True
elif user_role == "Non-BOM Team" and password == "NBOM2026":
    access = True
elif user_role == "GM Management" and password == "GM789":
    access = True

# --- MAIN INTERFACE ---
if access:
    st.success(f"Logged in: {user_role}")
    
    try:
        # We use 'read_excel' because your link is an .xlsx file
        df = pd.read_excel(CSV_URL)
        
        st.title("🏭 Daily Procurement Tracking")
        st.markdown("---")

        # Show the data
        st.subheader("Live Tracking Data")
        st.dataframe(df, use_container_width=True)

        if user_role == "Non-BOM Team":
            st.divider()
            st.subheader("💰 Price Approval Request")
            st.info("Select an item from the table above to process.")

    except Exception as e:
        st.error("Connecting to Excel...")
        st.info("If this takes too long, your company SharePoint might be blocking the connection. In that case, we will use the 'Upload to GitHub' method.")
else:
    st.info("Please enter your team's Passkey in the sidebar to view the data.")
