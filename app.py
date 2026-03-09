import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skyquad Electronics | Procurement", layout="wide")

# --- CUSTOM CSS (Animated Background & Watermark) ---
st.markdown("""
    <style>
    /* Smooth Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #0369a1, #1e1b4b);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Fixed Watermark */
    .watermark {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0.3;
        font-size: 1.1rem;
        color: #60a5fa;
        font-weight: bold;
        letter-spacing: 2px;
        z-index: 999;
        pointer-events: none;
        text-transform: uppercase;
        font-family: sans-serif;
    }

    /* Glass Effect for Data Tables */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Titles */
    h1 {
        color: white !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    </style>
    
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>SKYQUAD LOGIN</h1>", unsafe_allow_html=True)
        role = st.selectbox("Select Team", ["BOM Team", "Non-BOM Team", "GM Management"])
        pwd = st.text_input("Enter Passkey", type="password")
        
        if st.button("Access Dashboard", use_container_width=True):
            creds = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}
            if pwd == creds.get(role):
                st.session_state.auth = True
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Invalid Credentials")

# --- MAIN DASHBOARD ---
else:
    # Sidebar
    st.sidebar.title("Skyquad Menu")
    st.sidebar.write(f"Logged as: **{st.session_state.role}**")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    # Header
    st.markdown("<h1 style='text-align: center;'>Procurement Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1;'>Skyquad Electronics Industrial Tracking</p>", unsafe_allow_html=True)
    
    # File Upload
    uploaded_file = st.file_uploader("Upload CSV Database", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Dashboard Stats
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Items", len(df))
        c2.metric("Team Access", st.session_state.role)
        c3.metric("Status", "Online")

        st.divider()
        
        # Search
        search = st.text_input("🔍 Quick Search Database")
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

        # Display Data
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("👋 System online. Please upload the Procurement CSV file to view data.")
