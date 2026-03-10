# --- 3. DASHBOARD (POST-LOGIN) ---
else:
    # Sidebar Logout
    st.sidebar.title(f"Welcome, {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.session_state.role = None
        st.rerun()

    st.title("Factory Procurement Dashboard")
    
    # --- ROLE: BOM TEAM ---
    if st.session_state.role == "BOMTEAM":
        st.subheader("BOM Submission Form")
        with st.form("bom_form"):
            item_name = st.text_input("Item Name")
            quantity = st.number_input("Quantity", min_value=1)
            uom = st.selectbox("UOM", ["Units", "KG", "Meters", "Liters"])
            
            if st.form_submit_button("Submit to HOD"):
                new_entry = {
                    "Item": item_name, 
                    "Qty": quantity, 
                    "UOM": uom, 
                    "Status": "Pending",
                    "Submitted By": st.session_state.role
                }
                st.session_state.bom_list.append(new_entry)
                st.success("Request sent to HOD!")

    # --- ROLE: HOD (The Approval Queue) ---
    elif st.session_state.role == "HOD":
        st.subheader("📋 Pending Approvals")
        
        if not st.session_state.bom_list:
            st.info("No pending requests at the moment.")
        else:
            # Convert the list to a DataFrame for display
            df = pd.DataFrame(st.session_state.bom_list)
            
            # Show the table
            st.table(df)
            
            # Simple approval logic
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Approve All", type="primary"):
                    for item in st.session_state.bom_list:
                        item["Status"] = "Approved"
                    st.success("All items approved!")
                    st.rerun()
            with col2:
                if st.button("Clear Queue"):
                    st.session_state.bom_list = []
                    st.rerun()

    # --- ROLE: NON-BOM TEAM ---
    elif st.session_state.role == "NONBOMTEAM":
        st.warning("Non-BOM Dashboard Under Construction")
