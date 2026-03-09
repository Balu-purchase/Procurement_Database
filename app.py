import streamlit as st
import pandas as pd

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SKYQUAD | SECURE PORTAL", layout="wide")

# --- 2. THE ANIMATED BACKGROUND & UI ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #0369a1);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .watermark {
        position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%);
        opacity: 0.5; font-size: 1.1rem; color: #38bdf8; font-weight: 800;
        letter-spacing: 4px; z-index: 9999; pointer-events: none;
        text-transform: uppercase; border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 10px 20px; border-radius: 50px; background: rgba(0,0,0,0.4);
    }
    h1, h2, h3, p, label { color: white !important; }
</style>
<div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
""", unsafe_allow_html=True)

# --- 3. SESSION LOGIC ---
if "auth" not in st.session_state:
    st.session_state.auth = False

# --- 4. LOGIN GATE ---
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.header("🔐 SKYQUAD LOGIN
