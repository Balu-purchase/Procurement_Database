# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    login_col, img_col = st.columns([1, 2])
    with login_col:
        st.markdown("## 🏗️ Procurement Portal")
        uid = st.text_input("Username").upper()
        upw = st.text_input("Password", type="password")
        if st.button("ENTER SYSTEM"):
            creds = {"BOMTEAM": "BOM123", "HOD": "HOD789", "GM_OFFICE": "GM2026"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun()
    with img_col:
        st.image("https://images.unsplash.com/photo-1497366216548-37526070297c", use_container_width=True)
    st.stop()

# --- 3. DASHBOARD PAGE (This is where your 'else' starts) ---
else:
    st.sidebar.title(f"👤 {st.session_state.role}")
    # ... Rest of your code for BOM Team, HOD, and GM goes here ...
