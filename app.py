import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skyquad Electronics | Procurement", layout="wide")

# --- CUSTOM CSS (Animated Background & Simple Effective UI) ---
st.markdown("""
    <style>
    /* 1. Smooth Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #0ea5e9, #1e1b4b);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Fixed Watermark */
    .watermark {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0.3;
        font-size: 1.2rem;
        color: #60a5fa;
        font-weight: bold;
        letter-spacing: 3px;
        z-index: 0;
        pointer-events: none;
        text-transform: uppercase;
    }

    /* 3. Clean Glass Container */
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 4. Minimalist Headers */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: white;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* 5. Styled Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }

    /* Sidebar adjustment */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3) !important;
    }
    </style>
    
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<h1>SKYQUAD PORTAL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Please login to access procurement records</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            role = st.selectbox("Select Team", ["BOM Team", "Non-BOM Team", "GM Management"])
            pwd = st.text_input("Enter Passkey", type="password")
            if st.button("Login"):
                creds = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}
                if pwd == creds.get(role):
