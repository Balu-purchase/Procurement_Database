import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Safe initialization of session state
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "BOM"
if "bom_list" not in st.session_state:
    st.session_state.bom_list = []

# --- 2. FULL PAGE BACKGROUND & SIDE LOGIN ---
if not st.session_state.auth:
    # Custom CSS to inject the background image and style the login box
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    /* Making the login container stand out against the background */
    .stSecondaryBlock {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Creating the side-login layout (2/3 empty, 1/3 login)
    col_empty, col_login = st.columns([2, 1])

    with col_login:
        st.write("#") # Vertical spacing
        st.write("#")
        st.write("#")
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #1E1E1E;'>PORTAL LOGIN</h2>", unsafe_allow_html=True)
            uid = st.text_input("Username")
            upw = st.text_input("Password", type="password")
            if st.button("ENTER SYSTEM", use_container
