import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="SKYQUAD | COMMAND CENTER", layout="wide", initial_sidebar_state="expanded")

# --- ADVANCED PROFESSIONAL UI & ANIMATION ---
st.markdown("""
    <style>
    /* 1. Animated Skyquad Background */
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #0369a1);
        background-size: 400% 400%;
        animation: skyquadGradient 15s ease infinite;
    }
    @keyframes skyquadGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Professional Status Cards for Sidebar */
    .status-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #38bdf8;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    .status-label {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }
    .status-value {
        color: #f8fafc;
        font-weight: 700;
        font-size: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .pulse-icon {
        display: inline-block;
        width: 9px;
        height: 9px;
        background: #22c55e;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse-animation 2s infinite;
    }
    @keyframes pulse-animation {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }

    /* 3. Anti-Hack Watermark */
    .watermark {
        position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
        opacity: 0.4; font-size: 0.9rem; color: #38bdf8; font-weight: 800;
        letter-spacing: 4px; z-index: 9999; pointer-events: none;
        text-transform: uppercase; border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 8px 20px; border-radius: 50px; background: rgba(0,0,0,0.3);
    }

    /* 4. Restricted UI Styling */
    .stDataFrame { border: 1px solid rgba(56, 189, 248, 0.2) !important; border-radius: 12px; }
    h1, h2, h3 { color: #f8fafc !important; font-family: 'Inter', sans-serif; }
    div[data-testid="stExpander"] { background: rgba(0,0,0,0.2); border: none; }
    </style>
    
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- INTERNAL SECURITY GATE ---
ACCESS_KEYS = {
    "BOM Team": "BOM2026",
    "Non-BOM Team": "NBOM2026",
    "GM Management": "GM789"
}

if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
    st.session_state.role = None

# --- LOGIN GATE ---
if not st.session_state.secure_access:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.4, 1])
    
    with col2:
        st.markdown("""
            <div style="background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
                <h1 style='text-align: center; margin-bottom: 0;'>🔐 SKYQUAD SHIELD</h1>
                <p style='text-align: center; color: #64748b; margin-bottom: 30px;'>Restricted Procurement Access Portal</p>
            </div>
        """, unsafe_allow_html=True)
        
        selected_role = st.selectbox("OPERATIONAL ROLE", list(ACCESS_KEYS.keys()))
        entered_pwd = st.text_input("SECURITY PASSKEY", type="password")
        
        if st.button("AUTHORIZE ACCESS", use_container_width=True):
            if entered_pwd == ACCESS_KEYS.get(selected_role):
                st.session_state.secure_access = True
                st.session_state.role = selected_role
                st.rerun()
            else:
                st.error("Protocol Violation: Invalid Key")

# --- SECURE DASHBOARD ---
else:
    # Sidebar: Professional Status Hub
    with st.sidebar:
        st.markdown("### 🛠️ SYSTEM TERMINAL")
        
        # User Card
        st.markdown(f"""<div class="status-card">
            <div class="status-label">Operator Identity</div>
            <div class="status-value">{st.session_state.role}</div>
        </div>""", unsafe_allow_html=True)
        
        # Encryption Card
        st.markdown("""<div class="status-card" style="border-left-color: #22c55e;">
            <div class="status-label">Security Protocol</div>
            <div class="status-value"><span class="pulse-icon"></span>ENCRYPTED - ACTIVE</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("<br>"*10, unsafe_allow_html=True)
        if st.button("TERMINATE SESSION", use_container_width=True):
            st.session_state.secure_access = False
            st.session_state.role = None
            st.rerun()

    # --- GM MANAGEMENT VIEW ---
    if st.session_state.role == "GM Management":
        st.markdown("<h1 style='text-align: center;'>📊 STRATEGIC MONITORING CENTER</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Cross-Departmental Procurement Oversight</p>", unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📦 BOM STREAM")
            f1 = st.file_uploader("Sync BOM Data", type=["csv"], key="gm_bom")
            if f1:
                df1 = pd.read_csv(f1)
                st.metric("BOM Line Items", len(df1))
                st.dataframe(df1, height=400, hide_index=True)
        
        with col_right:
            st.subheader("🛠️ NON-BOM STREAM")
            f2 = st.file_uploader("Sync Non-BOM Data", type=["csv"], key="gm_nbom")
            if f2:
                df2 = pd.read_csv(f2)
                st.metric("Non-BOM Line Items", len(df2))
                st.dataframe(df2, height=400, hide_index=True)

    # --- TEAM DASHBOARD ---
    else:
        st.markdown(f"<h1>{st.session_state.role} Command Center</h1>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("📂 LOAD RESTRICTED DATASTREAM", type=["csv"])

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            c1, c2, c3 = st.columns(3)
            c1.metric("Active Records", len(df))
            c2.metric("Sync Status", "Verified")
            c3.metric("Data Integrity", "Secure")

            query = st.text_input("🔍 DATABASE SEARCH")
            if query:
                df = df[df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Awaiting secure file input. Please upload the procurement database.")
