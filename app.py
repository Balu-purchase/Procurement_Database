import streamlit as st
import pandas as pd

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False
if "role" not in st.session_state:
    st.session_state.role = None
if "hod_view" not in st.session_state:
    st.session_state.hod_view = "NONBOM"

# --- 2. THE EMPTY BOM TABLE STRUCTURE ---
# We initialize with the headers you provided, but no data.
if "bom_db" not in st.session_state:
    st.session_state.bom_db = pd.DataFrame(columns=[
        "S.NO", "VENDOR NAME", "PART NUMBER", "PRICE", "BOM", "HOD APPROVAL", "GM APPROVAL"
    ])

# --- 3. LOGIN ---
if not st.session_state.auth:
    st.title("🏭 Factory Management Login")
    with st.container(border=True):
        uid = st.text_input("Username")
        upw = st.text_input("Password", type="password")
        if st.button("LOG IN", use_container_width=True):
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun()
            else:
                st.error("Invalid Username or Password.")
    st.stop()

role = st.session_state.role
st.sidebar.title(f"👤 {role}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 4. BOM TEAM VIEW (MANAGE TABLE) ---
if role == "BOMTEAM":
    st.header("📦 BOM TEAM - Price Approval Dashboard")
    
    # --- ADD NEW DATA SECTION ---
    with st.expander("➕ Add New Entry to Table", expanded=True):
        with st.form("entry_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            v_name = c1.text_input("VENDOR NAME")
            p_num = c2.text_input("PART NUMBER")
            price = c3.text_input("PRICE")
            
            c4, c5 = st.columns(2)
            bom_val = c4.text_input("BOM")
            
            if st.form_submit_button("Add to Table"):
                new_sno = len(st.session_state.bom_db) + 1
                new_row = {
                    "S.NO": new_sno,
                    "VENDOR NAME": v_name,
                    "PART NUMBER": p_num,
                    "PRICE": price,
                    "BOM": bom_val,
                    "HOD APPROVAL": "PENDING",
                    "GM APPROVAL": "PENDING"
                }
                # Append new row to the dataframe
                st.session_state.bom_db = pd.concat([st.session_state.bom_db, pd.DataFrame([new_row])], ignore_index=True)
                st.rerun()

    st.divider()

    # --- DISPLAY & DELETE SECTION ---
    st.subheader("Current BOM Approval Table")
    if st.session_state.bom_db.empty:
        st.info("The table is currently empty. Add an entry above.")
    else:
        # Display the table
        st.dataframe(st.session_state.bom_db, use_container_width=True, hide_index=True)
        
        # Delete Functionality
        row_to_delete = st.number_input("Enter S.NO to Delete", min_value=1, max_value=len(st.session_state.bom_db), step=1)
        if st.button("🗑️ Delete Selected Row"):
            st.session_state.bom_db = st.session_state.bom_db[st.session_state.bom_db["S.NO"] != row_to_delete]
            # Reset S.NO for remaining items
            st.session_state.bom_db["S.NO"] = range(1, len(st.session_state.bom_db) + 1)
            st.rerun()

# --- 5. HOD VIEW ---
elif role == "HOD":
    st.title("👨‍💼 HOD COMMAND CENTER")
    c1, c2, c3 = st.columns(3)
    if c1.button("📊 NON-BOM ACTIVITY", use_container_width=True): st.session_state.hod_view = "NONBOM"
    if c2.button("📦 BOM APPROVALS", use_container_width=True): st.session_state.hod_view = "BOM"
    if c3.button("📜 AUDIT LOGS", use_container_width=True): st.session_state.hod_view = "AUDIT"

    st.divider()
    view = st.session_state.hod_view

    if view == "BOM":
        st.subheader("Reviewing Pending BOM Requests")
        if st.session_state.bom_db.empty:
            st.info("No data entered by BOM Team yet.")
        else:
            # Show interactive data editor for HOD to write comments directly
            edited_df = st.data_editor(st.session_state.bom_db, use_container_width=True, hide_index=True)
            if st.button("Save All Approvals"):
                st.session_state.bom_db = edited_df
                st.success("Changes saved successfully!")

    elif view == "AUDIT":
        st.subheader("📜 Official Records")
        st.dataframe(st.session_state.bom_db, use_container_width=True, hide_index=True)
