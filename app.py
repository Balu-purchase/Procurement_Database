# --- 🔵 BOM TEAM MODULE ---
    if st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team: New Price Request")
        # ... (form code here) ...

    # --- 🟠 HOD & GM APPROVAL ---
    elif menu == "PENDING APPROVALS":
        st.header(f"🖊️ {st.session_state.role} Approval Queue")
        # ... (approval logic here) ...

    # --- 🟢 NON-BOM TEAM MODULE ---
    elif st.session_state.role == "NONBOMTEAM":
        st.header("📦 Non-BOM Activity Management")
        # ... (non-bom form here) ...

    # --- 📊 AUDIT LOGS ---
    elif menu == "AUDIT LOGS":
        st.header("📝 Transaction Audit Logs")
        # ... (audit table here) ...
