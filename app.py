import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Procurement Control Center", layout="wide")

# 2. FULL-SCREEN 3D VIDEO BACKGROUND CSS
# This code injects a background video that loops smoothly
st.markdown("""
    <style>
    #tabs-b3-container { background: transparent; }
    .stApp {
        background: transparent;
    }
    /* The Video Background */
    #myVideo {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        opacity: 0.15; /* Adjusted for readability: 15% visibility */
        filter: grayscale(50%);
    }
    /* Summary Table Styling: Clean White with Glow */
    .stTable {
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
    }
    h1 {
        color: #0F172A;
        font-family: 'Trebuchet MS', sans-serif;
        font-weight: 800;
        text-align: center;
        background: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 15px;
    }
    </style>
    
    <video autoplay muted loop id="myVideo">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-a-circuit-board-1542-large.mp4" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 3. LOGIN
if not st.session_state.auth:
    st.markdown("<h1>🔐 MANAGEMENT LOGIN</h1>", unsafe_allow_html=True)
    pwd = st.text_input("ENTER KEY", type="password")
    if st.button("AUTHORIZE SYSTEM"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
            st.rerun()
else:
    # 4. MAIN INTERFACE
    st.markdown("<h1>🏭 PURCHASE NONBOM DAILY TRACKING REPORT</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        if st.button("🔄 REFRESH LIVE DATABASE", use_container_width=True):
