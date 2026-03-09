if not st.session_state.secure_access:
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px);'>
                <h1 style='text-align: center; margin-bottom: 0;'>🔐 SKYQUAD SHIELD</h1>
                <p style='text-align: center; color: #64748b;'>Restricted Procurement Access Portal</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Ensure these lines have no leading invisible spaces
        role_list = list(ACCESS_KEYS.keys())
        selected_role = st.selectbox("OPERATIONAL ROLE", role_list)
        entered_pwd = st.text_input("SECURITY PASSKEY", type="password")
        
        if st.button("AUTHORIZE ACCESS", use_container_width=True):
            if entered_pwd == ACCESS_KEYS.get(selected_role):
                st.session_state.secure_access = True
                st.session_state.role = selected_role
                st.rerun()
            else:
                st.error("Protocol Violation: Invalid Key")
