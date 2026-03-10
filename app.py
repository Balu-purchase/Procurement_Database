import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Ensure all session variables exist
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "BOM"
if "bom_list" not in st.session_state:
    st.session_state.bom_list = []

# --- 2. SIDE-ALIGNED LOGIN INTERFACE ---
if not st.session_state.auth:
    # Create two columns: Left for Industry Image/Text, Right for Login
    col_img, col_login = st.columns([2, 1], gap="large")

    with col_img:
        st.title("🏭 Industrial Procurement & Inventory System")
        st.markdown("""
        ### Strategic Supply Chain Management
        * Real-time BOM Approval Tracking
        * Daily Non-BOM Activity Logging
        * Multi-level HOD & GM Verification
        """)
        # Industrial visual placeholder
        st.image("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=1000", 
                 caption="Factory Smart Procurement Dashboard")

    with col_login:
        st.write("### 🔐 Secure Access")
        with st.container(border=True):
            uid = st.text_input("Username")
            upw = st.text_input("Password", type="password")
            if st.button("ENTER PORTAL", use_container_width=True):
                # User credentials
                creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
                if uid in creds and creds[uid] == upw:
                    st.session_state.auth = True
                    st.session_state.role = uid
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")
    st.stop()

# --- 3. DASHBOARD (POST-LOGIN) ---
role = st.session_state.role
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 4. BOM TEAM VIEW ---
if role == "BOMTEAM":
    st.header("📦 BOM TEAM - Data Entry")
    
    with st.expander("➕ Add New Entry to Table", expanded=True):
        with st.form("bom_entry_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            v_name = c1.text_input("VENDOR NAME")
            p_num = c2.text_input("PART NUMBER")
            
            c3, c4 = st.columns(2)
            price_val = c3.text_input("PRICE")
            bom_val = c4.text_input("BOM")
            
            if st.form_submit_button("ADD TO TABLE"):
                if v_name and p_num:
                    new_entry = {
                        "S.NO": len(st.session_state.bom_list) + 1,
                        "VENDOR NAME": v_name,
                        "PART NUMBER": p_num,
                        "PRICE": price_val,
                        "BOM": bom_val,
                        "HOD APPROVAL": "", 
                        "GM APPROVAL": ""
                    }
                    st.session_state.bom_list.append(new_entry)
                    st.success("Entry added to live table!")
                    st.rerun()
                else:
                    st.warning("Please enter Vendor and Part Number.")

    st.divider()
    st.subheader("📋 CURRENT BOM RECORD")
    if st.session_state.bom_list:
        df_display = pd.DataFrame(st.session_state.bom_list)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No data entered. Add items using the form above.")

# --- 5. HOD VIEW ---
elif role == "HOD":
    st.title("👨‍💼 HOD COMMAND CENTER")
    
    if st.button("📦 VIEW BOM REQUESTS", use_container_width=True):
        st.session_state.hod_view = "BOM"

    st.divider()
    
    if st.session_state.hod_view == "BOM":
        if st.session_state.bom_list:
            st.subheader("BOM Price Approvals")
            df_hod = pd.DataFrame(st.session_state.bom_list)
            edited_df = st.data_editor(df_hod, use_container_width=True, hide_index=True)
            
            if st.button("💾 SAVE ALL CHANGES"):
                st.session_state.bom_list = edited_df.to_dict('records')
                st.success("Approvals saved!")
        else:
            st.info("BOM Team has not entered any data yet.")
