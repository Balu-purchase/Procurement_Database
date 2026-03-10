import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "master_data" not in st.session_state:
    st.session_state.master_data = []

# --- Helper Function for Status Colors ---
def style_status(val):
    if val == "APPROVED":
        return 'background-color: green; color: white; font-weight: bold'
    elif val == "REJECTED":
        return 'background-color: red; color: white; font-weight: bold'
    return ''

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://t3.ftcdn.net/jpg/09/94/98/98/360_F_994989868_JVms41RbTVCoI1wmY7JOwTGG3CsGQ8wr.webp");
        background-size: cover;
        background-position: center;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px; padding: 20px;
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
            
            if st.button("ENTER SYSTEM", use_container_width=True):
                # Added GM_OFFICE to your existing credentials
                credentials = {
                    "BOMTEAM": "BOM123", 
                    "NONBOMTEAM": "NONBOM123", 
                    "HOD": "HOD789",
                    "GM_OFFICE": "GM2026"
                }
                if uid in credentials and credentials[uid] == upw:
                    st.session_state.auth = True
                    st.session_state.role = uid
                    st.rerun() 
                else:
                    st.error("Invalid Credentials.")

# --- 3. DASHBOARD PAGE ---
else:
    st.sidebar.title(f"👤 {st.session_state.role}")
    
    # NAVIGATION FOR HOD & GM
    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("GO TO", ["BOM", "NONBOM", "AUDIT LOGS"])
    else:
        menu = "MAIN"

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.title("Factory Procurement Dashboard")
    st.divider()

    # --- BOM TEAM DASHBOARD ---
    if st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team: Manual Entry")
        
        with st.container(border=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            proj = r1c1.text_input("PROJECT")
            pnum = r1c2.text_input("PART NUMBER")
            desc = r1c3.text_input("DESCRIPTION")
            qps = r1c4.text_input("QPS")
            
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            uom = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Ltr"])
            supp = r2c2.text_input("SUPPLIER NAME")
            price = r2c3.text_input("PRICE")
            opt_supp = r2c4.text_input("OPTIONAL SUPPLIER")
            
            if st.button("SUBMIT REQUEST", type="primary"):
                new_entry = {
                    "PROJECT": proj, "PARTNUMBER": pnum, "DESCRIPTION": desc,
                    "QPS": qps, "UOM": uom, "SUPPLIER": supp, "PRICE": price,
                    "OPT_SUPP": opt_supp, "HOD APPROVAL": "", "GM APPROVAL": "",
                    "STATUS": "PENDING", "REMARKS": ""
                }
                st.session_state.master_data.append(new_entry)
                st.success("Submitted to HOD!")
                st.rerun()

        st.subheader("📋 PRICE APPROVAL REQUEST STATUS")
        if st.session_state.master_data:
            df = pd.DataFrame(st.session_state.master_data)
            disp_cols = ["PROJECT", "PARTNUMBER", "DESCRIPTION", "QPS", "UOM", "SUPPLIER", "PRICE", "HOD APPROVAL", "GM APPROVAL", "STATUS"]
            st.dataframe(df[disp_cols].style.applymap(style_status, subset=['STATUS']), use_container_width=True)

    # --- HOD & GM DASHBOARD ---
    elif st.session_state.role in ["HOD", "GM_OFFICE"]:
        role_label = "HOD" if st.session_state.role == "HOD" else "GM"
        
        if menu == "BOM":
            st.header(f"📋 {role_label}: BOM APPROVAL QUEUE")
            if not st.session_state.master_data:
                st.info("No pending requests.")
            else:
                for i, row in enumerate(st.session_state.master_data):
                    # Filter: HOD sees PENDING, GM sees HOD_APPROVED
                    show_item = False
                    if st.session_state.role == "HOD" and row["STATUS"] == "PENDING":
                        show_item = True
                    elif st.session_state.role == "GM_OFFICE" and row["HOD APPROVAL"] == "APPROVED" and row["GM APPROVAL"] == "":
                        show_item = True

                    if show_item:
                        with st.container(border=True):
                            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
                            c1.write(f"**PROJECT:** {row['PROJECT']} | **PART:** {row['PARTNUMBER']}")
                            c2.write(f"**DESC:** {row['DESCRIPTION']}")
                            c3.write(f"**PRICE:** {row['PRICE']}")
                            
                            status_choice = st.selectbox("DECISION", ["PENDING", "APPROVED", "REJECTED"], key=f"stat{i}")
                            rem = st.text_input("REMARKS (Optional)", key=f"rem{i}")
                            
                            if st.button("CONFIRM", key=f"btn{i}"):
                                if st.session_state.role == "HOD":
                                    st.session_state.master_data[i]["HOD APPROVAL"] = status_choice
                                    st.session_state.master_data[i]["STATUS"] = status_choice
                                else:
                                    st.session_state.master_data[i]["GM APPROVAL"] = status_choice
                                    st.session_state.master_data[i]["STATUS"] = status_choice
                                
                                st.session_state.master_data[i]["REMARKS"] = rem
                                st.rerun()
        
        elif menu == "AUDIT LOGS":
            st.header("📁 OFFICIAL AUDIT LOGS")
            if st.session_state.master_data:
                df_audit = pd.DataFrame(st.session_state.master_data)
                df_audit = df_audit[df_audit["STATUS"] != "PENDING"]
                st.dataframe(df_audit.style.applymap(style_status, subset=['STATUS']), use_container_width=True)

    # --- NON-BOM DASHBOARD ---
    elif st.session_state.role == "NONBOMTEAM":
        st.header("📦 Non-BOM Team Dashboard")
        st.info("Module active. Ready for Non-BOM entries.")
