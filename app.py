import streamlit as st
import pandas as pd

# 1. PAGE SETUP
st.set_page_config(page_title="Executive Dashboard", layout="wide")

# 2. FULL-SCREEN ANIMATED BACKGROUND (Industrial 3D Loop)
# This uses a professional 3D factory/technical animation as a live background
st.markdown("""
    <style>
    /* Make the app background transparent to show the video */
    .stApp {
        background: transparent;
    }
    /* The Animated Background Video */
    #bgVideo {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        opacity: 0.20; /* 20% visibility for a professional look */
        filter: brightness(0.8);
    }
    /* Summary Table: White, Centered, and Elevated */
    .stTable {
        width: auto !important;
        margin-left: auto;
        margin-right: auto;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0px 12px 40px rgba(0, 0, 0, 0.3);
    }
    h1 {
        color: #0F172A;
        text-align: center;
        font-weight: 800;
        background: rgba(255, 255, 255, 0.6);
        padding: 15px;
        border-radius: 20px;
        margin-bottom: 30px;
    }
    h3 { color: #1E293B; text-align: center; font-weight: 700; }
    </style>
    
    <video autoplay muted loop id="bgVideo">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-a-circuit-board-1542-large.mp4" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# 3. LOGIN
if not st.session_state.auth:
    st.markdown("<h1>🔐 PROCUREMENT COMMAND CENTER</h1>", unsafe_allow_html=True)
    pwd = st.text_input("AUTHORIZATION KEY", type="password")
    if st.button("LOG IN"):
        if pwd in ["BOM2026", "NBOM2026", "GM789"]:
            st.session_state.auth = True
