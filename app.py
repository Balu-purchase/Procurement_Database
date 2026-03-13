# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    login_col, img_col = st.columns([1, 2])
    with login_col:
        st.markdown("# 🏗️ Procurement \n### Approval Portal")
        st.divider()
        uid = st.text_input("Username").strip().upper() 
        upw = st.text_input("Password", type="password")
        if st.button("ENTER SYSTEM", use_container_width=True):
            creds = {
                "BOMTEAM": "BOM123", 
                "NONBOMTEAM": "NONBOM123", 
                "HOD": "HOD789", 
                "GM_OFFICE": "GM2026"
            }
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun() 
            else:
                st.error("Invalid Credentials.")
    with img_col:
        st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1200", 
                 caption="Resolute Factory Management", use_container_width=True)
    st.stop()
