import streamlit as st
import pandas as pd
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resolute Procurement Portal", layout="wide")

# --- SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "data" not in st.session_state:
    st.session_state.data = None

# --- LOGIN SYSTEM ---
if not st.session_state.authenticated:
    st.sidebar.title("🔐 Secure Access")
    role = st.sidebar.selectbox("Select Your Team", ["BOM Team", "Non-BOM Team", "GM Management"])
    pwd = st.sidebar.text_input("Enter Team Passkey", type="password")
    
    if st.sidebar.button("Login"):
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
    
    if st.session_state.data is None:
        st.info("👋 Welcome! Please upload the 'Procurement_Database.xlsx' file.")
        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
        
        if uploaded_file:
            try:
                # Load the data
                st.session_state.data = pd.read_excel(uploaded_file, engine='openpyxl')
                st.success("✅ Database Loaded!")
                st.rerun()
            except ImportError:
                st.error("🚨 Missing Dependency: Please run 'pip install openpyxl' in your terminal.")
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    else:
        df = st.session_state.data
        st.subheader("Live Tracking Data")
        st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Resolute Electronics v2.1")
