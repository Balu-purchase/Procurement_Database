# --- 3. DASHBOARD PAGE ---
else:
    st.sidebar.title(f"👤 {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    # Determine menu based on role
    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("NAVIGATE", ["PENDING APPROVALS", "NON-BOM REVIEW", "AUDIT LOGS"])
    else:
        menu = "MAIN"

    st.title("PRICE APPROVALS FOR BOM ITEMS")
    st.divider()

    # --- 🔵 BOM TEAM MODULE ---
    if st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team: New Price Request")
        with st.form("bom_entry", clear_on_submit=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            p_proj = r1c1.text_input("PROJECT")
            p_num = r1c2.text_input("PART NUMBER")
            p_desc = r1c3.text_input("DESCRIPTION")
            p_qps = r1c4.text_input("QPS")
            
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            p_uom = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Ltr"])
            p_supp = r2c2.text_input("SUPPLIER NAME")
            p_price = r2c3.text_input("PRICE")
            p_rem = r2c4.text_input("REMARKS")
            
            if st.form_submit_button("SUBMIT FOR APPROVAL"):
                st.session_state.master_data.append({
                    "VENDOR NAME": p_supp, "PART NUMBER": p_num, "MATERIAL DESCRIPTION": p_desc, 
                    "PRICE": p_price, "QPS": p_qps, "UOM": p_uom, "REMARKS": p_rem,
                    "HOD_SIGN": "PENDING", "GM_SIGN": "PENDING", "STATUS": "PENDING AT HOD"
                })
                st.rerun()
        
        st.subheader("📋 Submission Status")
        if st.session_state.master_data:
            df_bom = pd.DataFrame(st.session_state.master_data)
            st.dataframe(df_bom.style.applymap(style_status, subset=['STATUS', 'HOD_SIGN', 'GM_SIGN']), use_container_width=True)

    # ---
