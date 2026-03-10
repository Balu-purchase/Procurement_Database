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

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://t3.ftcdn.net/jpg/09/94/98/98/360_F_994989868_JVms41RbTVCoI1wmY7JOwTGG3CsGQ8wr.webp");
        background-size: cover;
        background-position: center;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    _, col_login = st.columns([1.8, 1])
    with col_login:
        st.write("###")
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #333;'>SYSTEM LOGIN</h2>", unsafe_allow_html=True)
            uid = st.text_input("Username").strip().upper() 
            upw = st.text_input("Password", type="password")
            
            if st.button("ENTER SYSTEM", use_container_width=True, key="login_btn"):
                # Complete Credentials Dictionary
                credentials = {
                    "BOMTEAM": "BOM123", 
                    "NONBOMTEAM": "NONBOM123", 
                    "HOD": "HOD789"
                }
                
                if uid in credentials and credentials[uid] == upw:
                    st.session_state.auth = True
                    st.session_state.role = uid
                    st.rerun() 
                else:
                    st.error("Invalid Credentials. Please check your username and password.")

# --- 3. DASHBOARD PAGE ---
else:
    # Sidebar for logout
    st.sidebar.title(f"👤 {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.session_state.role = None
        st.rerun()

    st.title("Factory Procurement Dashboard")
    st.divider()

    # --- ROLE: BOM TEAM ---
    if st.session_state.role == "BOMTEAM":
        st.subheader("🛠️ BOM
