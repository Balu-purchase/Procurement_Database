import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "bom_list" not in st.session_state:
    st.session_state.bom_list = []

# --- 2. FULL PAGE BACKGROUND & SIDE LOGIN ---
if not st.session_state.auth:
    # Updated background image link (Adobe Stock via FTCDN)
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://t3.ftcdn.net/jpg/09/94/98/98/360_F_994989868_JVms41RbTVCoI1wmY7JOwTGG3CsGQ8wr.webp");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* Making the login box look clean against the lighter image */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    col_empty, col_login = st.columns([1.8, 1]) # Adjusted ratio for better alignment
    with col_login:
        st.write("###")
        st.write("###")
        with st.container(border=True):
            # Changed text color to dark for visibility on light background
            st.markdown("<h2 style='text-align: center; color: #333;'>SYSTEM LOGIN</h2>", unsafe_allow_html=True)
            uid = st.text_input("Username")
            upw = st.text_input("Password", type="password")
            
            if st.button("ENTER SYSTEM", use_container_width=True):
                creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
                if uid in creds and creds[uid] == upw:
                    st.session_state.auth = True
                    st.session_state.role = uid
                    st.rerun() # Refresh to clear the login screen
                else:
                    st.error("Invalid Credentials")

# --- 3. DASHBOARD (POST-LOGIN) ---
else:
    # Sidebar Logout
    st.sidebar.title(f"Welcome, {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.session_state.role = None
        st.rerun()

    st.title("Factory Procurement Dashboard")
    st.write(f"Logged in as: **{st.session_state.role}**")
    
    # Placeholder for different views based on role
    if st.session_state.role == "BOMTEAM":
        st.info("Displaying BOM Management Tools...")
        # Add your BOM specific code here
        
    elif st.session_state.role == "HOD":
        st.success("Displaying Approval Queue...")
        # Add your HOD specific code here
