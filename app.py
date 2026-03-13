# --- 🟢 NON-BOM TEAM MODULE ---
    elif st.session_state.role == "NONBOMTEAM":
        st.header("📦 Non-BOM Activity Management")
        
        # Form for Non-BOM data entry
        with st.form("non_bom_entry", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            nb_item = col1.text_input("ITEM NAME")
            nb_qty = col2.text_input("QUANTITY")
            nb_supp = col3.text_input("PROPOSED SUPPLIER")
            
            if st.form_submit_button("SUBMIT NON-BOM REQUEST"):
                st.session_state.master_data.append({
                    "VENDOR NAME": nb_supp, "PART NUMBER": "NON-BOM", "MATERIAL DESCRIPTION": nb_item, 
                    "PRICE": "N/A", "QPS": nb_qty, "UOM": "Nos", "REMARKS": "Non-BOM Entry",
                    "HOD_SIGN": "PENDING", "GM_SIGN": "PENDING", "STATUS": "PENDING AT HOD"
                })
                st.success("Non-BOM Request Submitted")
                st.rerun()

        st.subheader("📋 Non-BOM Status Tracker")
        if st.session_state.master_data:
            df_all = pd.DataFrame(st.session_state.master_data)
            # Filter to show only Non-BOM items if desired, or show all
            df_nb = df_all[df_all["PART NUMBER"] == "NON-BOM"]
            if not df_nb.empty:
                st.dataframe(df_nb.style.applymap(style_status, subset=['STATUS', 'HOD_SIGN', 'GM_SIGN']), use_container_width=True)
            else:
                st.info("No Non-BOM records found.")

    # --- 📊 AUDIT LOGS MODULE ---
    elif menu == "AUDIT LOGS":
        st.header("📝 Transaction Audit Logs")
        if st.session_state.master_data:
            df_audit = pd.DataFrame(st.session_state.master_data)
            # Full color-coded table for HOD and GM
            st.dataframe(df_audit.style.applymap(style_status, subset=['STATUS', 'HOD_SIGN', 'GM_SIGN']), use_container_width=True)
        else:
            st.info("No records found.")
