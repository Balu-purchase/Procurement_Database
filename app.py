import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="SKYQUAD | SECURE PORTAL", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #000000);
        background-size: 400% 400%;
        animation: skyquadGradient 20s ease infinite;
    }
    @keyframes skyquadGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .watermark {
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0.25;
        font-size: 1rem;
        color: #38bdf8;
        font-weight: 800;
        letter-spacing: 5px;
        z-index: 9999;
        pointer-events: none;
        text-transform: uppercase;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 5px 15px;
        border-radius: 50px;
    }
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3, p { color: #f8fafc !important; }
    </style>
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- ACCESS CONTROL ---
if "secure_access" not in st.session_state:
    st.session_state
