import streamlit as st
import pandas as pd

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SKYQUAD | SECURE PORTAL", layout="wide")

# --- 2. THE ANIMATED BACKGROUND (STRICT CSS) ---
st.markdown("""
    <style>
    /* Fixed background container with moving gradient */
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #0369a1);
        background-size: 400% 400% !important;
        animation: gradientBG 15s ease infinite !important;
        height: 100vh;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating Watermark */
    .watermark {
        position: fixed;
        bottom: 25px;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0.5;
        font-size: 1.1rem;
        color: #38bdf8;
        font-weight: 800;
        letter-spacing: 4px;
        z-index: 9999;
        pointer-events: none;
        text-transform: uppercase;
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 10px 20px;
        border-radius: 50px;
        background: rgba(0,0,0,0.4);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Force text to be visible */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: white !important;
    }

    /* Glass Effect Box */
    .glass-panel {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 40px;
        border-radius
