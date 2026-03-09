import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skyquad Electronics | Procurement", layout="wide")

# --- CUSTOM CSS (The "Ultra-Impressive" Design) ---
st.markdown("""
    <style>
    /* 1. Industrial Background Image */
    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.85)), 
                    url("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* 2. Floating Watermark */
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        opacity: 0.15;
        font-size: 2.5rem;
        color: white;
        transform: rotate(-15deg);
        z-index: -1;
        font-weight: 900;
        pointer-events: none;
    }

    /* 3. Glass-morphism Cards */
    div[data-testid="stMetric"], div.stDataFrame, .stAlert {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        color: white !important;
    }

    /* 4. Glowing Title */
    h1 {
        color: #60a5fa !important;
        text-shadow: 0 0 15px rgba(96, 165, 250, 0.5);
        font-size: 3rem !important;
        text-align: center;
        letter-spacing: 2px;
    }

    /* 5. Custom Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 30, 0.95) !important;
        border-right: 1px solid #3b82f6;
    }

    /* Sidebar Labels */
    .st-emotion-cache-6qob1r { color: #60a5fa !important; }
    
    /* Input Boxes */
    input
