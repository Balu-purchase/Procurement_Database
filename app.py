import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resolute Procurement Portal", layout="wide")

# --- LOGIN SYSTEM ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.sidebar.title("🔐 Secure Access")
    role = st.sidebar.selectbox("Select Team", ["BOM Team", "Non-BOM Team", "GM Management"])
    pwd = st.sidebar.text_input("Passkey", type="password")
    
    if st.sidebar.button("Login"):
        # Match your existing passwords
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
    st.title("🏭 Daily Procurement Tracking")
    st.sidebar.success(f"Role: {st.session_state.role}")
    
    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    # --- STEP: UPLOAD CSV ---
    st.info("Please upload your 'Procurement_Database.csv' file below.")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        # read_csv DOES NOT require openpyxl or any extra installs
        df = pd.read_csv(uploaded_file)
        
        # Search Filter
        search = st.text_input("🔍 Search Database")
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            
        st.subheader("Live Data")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Waiting for file upload...")
