import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
# Replace this with your Google Sheet CSV Link
SHEET_URL = "https://resolutegroups-my.sharepoint.com/:x:/g/personal/purchase_resoluteelectronics_com/"data.csv""

st.set_page_config(page_title="Industrial Portal", layout="wide")

# --- LOGIN SYSTEM ---
st.sidebar.title("🔐 Secure Login")
user_role = st.sidebar.selectbox("Select Team", ["BOM Team", "Non-BOM Team", "GM Management"])
password = st.sidebar.text_input("Enter Passkey", type="password")

# Define your specific passkeys
access = False
if user_role == "BOM Team" and password == "BOM2026":
    access = True
elif user_role == "Non-BOM Team" and password == "NBOM2026":
    access = True
elif user_role == "GM Management" and password == "GM789":
    access = True

# --- WEBSITE INTERFACE ---
if access:
    st.success(f"Logged in: {user_role}")
    
    try:
        # Load data from Google Sheet
        df = pd.read_csv(SHEET_URL)
        
        st.title("🏭 Daily Procurement Tracking")
        st.markdown("---")

        # 1. SHOW THE TABLE (As you requested: 10 Columns)
        st.subheader("Live Daily Status")
        st.dataframe(df, use_container_width=True)

        # 2. NON-BOM TEAM: PRICE APPROVAL VIEW
        if user_role == "Non-BOM Team":
            st.divider()
            st.subheader("💰 Rise Price Approval")
            # Select ID from your Excel list
            selected_id = st.selectbox("Select ID to Send for Approval", df['ID'].unique())
            
            if st.button("Send Price to GM"):
                # This simulates the "Rise" action
                st.info(f"Price for {selected_id} has been submitted for GM review.")

    except Exception as e:
        st.error("Error: Please check your Google Sheet 'Publish to Web' link.")

else:
    st.warning("Please enter the correct Passkey to view the website.")
