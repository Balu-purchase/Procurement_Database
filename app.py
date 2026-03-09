import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="SKYQUAD | GM COMMAND CENTER", layout="wide")

# --- CUSTOM CSS (Animated Background & Watermark) ---
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
    /* Glassmorphism containers for side-by-side view */
    [data-testid="column"] {
        background: rgba(255, 255, 255, 0.03);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3 { color: #f8fafc !important; }
    </style>
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- ACCESS CONTROL ---
if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
    st.session_state.role = None

if not st.session_state.secure_access:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🔐 SKYQUAD SHIELD</h1>", unsafe_allow_html=True)
        role = st.selectbox("Identify Your Team", ["BOM Team", "Non-BOM Team", "GM Management"])
        pwd = st.text_input("Security Passkey", type="password")
        if st.button("VERIFY IDENTITY", use_container_width=True):
            creds = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}
            if pwd == creds.get(role):
                st.session_state.secure_access = True
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Invalid Passkey")

# --- LOGGED IN AREA ---
else:
    # Sidebar Logout
    st.sidebar.title("System Status")
    st.sidebar.success(f"Mode: {st.session_state.role}")
    if st.sidebar.button("TERMINATE SESSION"):
        st.session_state.secure_access = False
        st.rerun()

    # --- GM MANAGEMENT VIEW (MASTER MONITORING) ---
    if st.session_state.role == "GM Management":
        st.markdown("<h1 style='text-align: center;'>📊 GM MASTER MONITORING</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Real-time tracking of BOM and Non-BOM Procurement streams.</p>", unsafe_allow_html=True)
        
        # Dual Uploaders for Side-by-Side Comparison
        col_bom, col_nbom = st.columns(2)
        
        with col_bom:
            st.subheader("📦 BOM Team Stream")
            file_bom = st.file_uploader("Upload BOM CSV", type=["csv"], key="bom_up")
            if file_bom:
                df_bom = pd.read_csv(file_bom)
                st.metric("BOM Items", len(df_bom))
                st.dataframe(df_bom, height=400)
            else:
                st.info("Awaiting BOM data...")

        with col_nbom:
            st.subheader("🛠 Non-BOM Team Stream")
            file_nbom = st.file_uploader("Upload Non-BOM CSV", type=["csv"], key="
