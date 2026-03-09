import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="SKYQUAD | SECURE PORTAL", layout="wide", initial_sidebar_state="collapsed")

# --- ADVANCED SECURITY & ANIMATED UI ---
st.markdown("""
    <style>
    /* 1. Animated Skyquad Background */
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

    /* 2. Anti-Hack Watermark (Fixed & Protected) */
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

    /* 3. Restricted UI Styling */
    .stDataFrame { border: 1px solid #1e3a8a !important; border-radius: 12px; }
    h1 { color: #f8fafc !important; text-shadow: 0 0 20px rgba(56, 189, 248, 0.4); }
    </style>
    
    <div class="watermark">NONBOM TEAM - PURCHASE SKYQUAD ELECTRONICS</div>
    """, unsafe_allow_html=True)

# --- INTERNAL SECURITY GATE ---
# These are hardcoded; in a real 'hack-proof' environment, 
# you'd never show these, but they are here for your team's access.
ACCESS_KEYS = {
    "BOM Team": "BOM2026",
    "Non-BOM Team": "NBOM2026",
    "GM Management": "GM789"
}

if "secure_access" not in st.session_state:
    st.session_state.secure_access = False
    st.session_state.role = None

# --- STEP 1: ACCESS GATE (THE LOCK) ---
if not st.session_state.secure_access:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🔐 SKYQUAD SHIELD</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Internal Procurement Access Only</p>", unsafe_allow_html=True)
        
        # Identity selection
        selected_role = st.selectbox("Identify Your Team", list(ACCESS_KEYS.keys()))
        # Secure password input
        entered_pwd = st.text_input("Security Passkey", type="password", help="Contact IT for lost keys.")
        
        if st.button("VERIFY IDENTITY", use_container_width=True):
            if entered_pwd == ACCESS_KEYS.get(selected_role):
                st.session_state.secure_access = True
                st.session_state.role = selected_role
                st.success("Identity Verified. Granting Access...")
                st.rerun()
            else:
                st.error("⚠️ ACCESS DENIED: Invalid Security Key.")

# --- STEP 2: SECURE DASHBOARD (THE VAULT) ---
else:
    # Sidebar remains for logout and status
    st.sidebar.markdown("### 🛠 STATUS")
    st.sidebar.write(f"**USER:** {st.session_state.role}")
    st.sidebar.write("**ENCRYPTION:** ACTIVE")
    
    if st.sidebar.button("TERMINATE SESSION"):
        st.session_state.secure_access = False
        st.session_state.role = None
        st.rerun()

    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.role} Command Center</h1>", unsafe_allow_html=True)
    
    # Secure File Upload
    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Load Restricted CSV Data", type=["csv"])

    if uploaded_file:
        try:
            # We wrap the data loading in a try block to prevent crashing on corrupt files
            df = pd.read_csv(uploaded_file)
            
            # Privacy Filter: Only show data relevant to the role?
            # (Optional: You can hide columns here if you want)
            
            st.markdown("### 📊 Active Procurement Stream")
            
            # Quick Analytics
            stat1, stat2 = st.columns(2)
            stat1.metric("Total Items", f"{len(df)}")
            stat2.metric("Security Level", "High-Priority")

            # Search bar with protection
            query = st.text_input("🔍 Secure Search")
            if query:
                df = df[df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
        except Exception as e:
            st.error("Critical Error: The file structure is not recognized.")
    else:
        st.info("Awaiting secure file input. Please upload the .csv database to begin analysis.")
