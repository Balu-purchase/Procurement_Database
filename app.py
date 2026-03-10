import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Ensure all session variables exist to prevent startup crashes
if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "BOM"
if "bom_list" not in st.session_state:
    st.session_state.bom_list = []

# --- 2. LOGIN SYSTEM ---
if not st.session_state.auth:
    st.title("🏭 Factory Management Login")
    with st.container(border=True):
        uid = st.text_input("Username")
        upw = st.text_input("Password", type="password")
        if st.button("LOG IN", use_container_width=True):
            # User credentials
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun()
            else:
                st.error("Invalid Username or Password.")
    st.stop()

# Set current role
role = st.session_state.role
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 3. BOM TEAM VIEW ---
if role == "BOMTEAM":
    st.header("📦 BOM TEAM - Data Entry")
    
    # Entry Form
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
                    st.success("Entry added!")
                    st.rerun()
                else:
                    st.warning("Please enter Vendor and Part Number.")

    st.divider()
    
    # Reflect the table below the form
    st.subheader("📋 CURRENT BOM RECORD")
    if st.session_state.bom_list:
        df_display = pd.DataFrame(st.session_state.bom_list)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Sidebar option to delete the last row if a mistake was made
        if st.sidebar.button("🗑️ Delete Last Entry"):
            if st.session_state.bom_list:
                st.session_state.bom_list.pop()
                st.rerun()
    else:
        st.info("No data entered. Add items using the form above.")

# --- 4. HOD VIEW ---
elif role == "HOD":
    st.title("👨‍💼 HOD COMMAND CENTER")
    
    if st.button("📦 VIEW BOM REQUESTS", use_container_width=True):
        st.session_state.hod_view = "BOM"

    st.divider()
    
    if st.session_state.hod_view == "BOM":
        if st.session_state.bom_list:
            st.subheader("BOM Price Approvals")
            df_hod = pd.DataFrame(st.session_state.bom_list)
            
            # HOD can edit the "HOD APPROVAL" column directly
            edited_df = st.data_editor(df_hod, use_container_width=True, hide_index=True)
            
            if st.button("💾 SAVE ALL CHANGES"):
                st.session_state.bom_list = edited_df.to_dict('records')
                st.success("Approvals saved!")
        else:
            st.info("BOM Team has not entered any data yet.")
