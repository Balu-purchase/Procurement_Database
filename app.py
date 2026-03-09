import streamlit as st
import pandas as pd

# 1. PAGE SETUP & INDUSTRIAL THEME
st.set_page_config(page_title="Procurement Control Center", layout="wide")

# CUSTOM CSS: Dark Industrial Theme + Fit-to-Content Tables + Animation Styling
st.markdown("""
    <style>
    /* Dark Charcoal Industrial Background */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }
    /* Summary Table: Fit to Text Length & Centered */
    .stTable {
        width: fit-content !important;
        margin-left: auto;
        margin-right: auto;
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    /* Detailed Table: Dark Mode Styling */
    .stDataFrame {
        background-color: #1e293b;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        text-align: center;
        font-weight: bold;
    }
    /* Animation Header Box */
    .header-box {
        display: flex;
        justify-content: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 2. LOGIN SECTION
if not st.session_state.auth:
    st.markdown("<h1>🔐 PROCUREMENT GATEWAY</h1>", unsafe_allow_html=True)
    pwd = st.text_input("AUTHORIZATION KEY", type="password")
    if st.button("ACCESS SYSTEM"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied")

# 3. MAIN DASHBOARD
else:
    # --- INDUSTRIAL 3D ANIMATION HEADER ---
    # Using a professional 3D Industrial loop (GIF) for instant loading
    st.markdown('<div class="header-box">', unsafe_allow_html=True)
    st.image("
