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
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    col_empty, col_login = st.columns([2, 1])
    with col_login:
        st.write("###")
        st.write("###")
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: white;'>SYSTEM LOGIN</h2>", unsafe_allow_html=True)
            uid = st.text_input("Username")
            upw = st.text_input("Password", type="password")
            if st.button("ENTER SYSTEM", use_container_width=True):
                creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
                if uid in creds and creds[uid] == upw:
                    st.session_state.auth = True
                    st.session_state.role = uid
