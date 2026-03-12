import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu

# --- PAGE CONFIG ---
st.set_page_config(page_title="Resolute Admin Portal", layout="wide", page_icon="🚀")

# --- INITIALIZE DATABASE (Session State) ---
if "bom_data" not in st.session_state:
    st.session_state.bom_data = []
if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []

# --- HELPER FUNCTIONS ---
def add_audit_log(user, action, details):
    log = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User": user,
        "Action": action,
        "Details": details
    }
    st.session_state.audit_logs.append(log)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/Logo_placeholder.png", width=100)
    st.title("Resolute Admin")
    
    selected = option_menu(
        menu_title="Main Menu",
        options=["Dashboard", "BOM Team", "Non-BOM Team", "Audit Logs", "Logout"],
        icons=["speedometer2", "cpu", "box-seam", "journal-text", "door-open"],
        menu_icon="cast",
        default_index=0,
    )

# --- LOGOUT LOGIC ---
if selected == "Logout":
    st.session_state.clear()
    st.success("Logged out successfully.")
    st.stop()

# ---------------- MODULE 1: DASHBOARD ---------------- #
if selected == "Dashboard":
    st.title("📊 Procurement Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total BOM Requests", len(st.session_state.bom_data))
    with col2:
        approved_count = len([x for x in st.session_state.bom_data if x['STATUS'] == "APPROVED"])
        st.metric("Approved Requests", approved_count)
    with col3:
        st.metric("System Status", "Live", delta="Active")

    if st.session_state.bom_data:
        df = pd.DataFrame(st.session_state.bom_data)
        st.subheader("Recent Activity Trend")
        st.line_chart(df['Price'])
    else:
        st.info("No data available yet to display charts.")

# ---------------- MODULE 2: BOM TEAM ---------------- #
elif selected == "BOM Team":
    st.title("💻 BOM Procurement Module")
    
    with st.form("bom_entry"):
        col_a, col_b = st.columns(2)
        vendor = col_a.text_input("Vendor Name")
        part = col_b.text_input("Part Number")
        price = col_a.number_input("Unit Price", min_value=0.0)
        bom_type = col_b.selectbox("BOM Type", ["Production", "R&D", "Sample"])
        
        if st.form_submit_button("Submit BOM Request"):
            new_req = {
                "Vendor": vendor, "Part": part, "Price": price, 
                "BOM": bom_type, "STATUS": "PENDING", "Date": datetime.now().date()
            }
            st.session_state.bom_data.append(new_req)
            add_audit_log("ADMIN", "BOM_SUBMISSION", f"Added {part} from {vendor}")
            st.success("BOM Request logged!")
            st.rerun()

    if st.session_state.bom_data:
        st.write("Current BOM Submissions")
        st.table(pd.DataFrame(st.session_state.bom_data))

# ---------------- MODULE 3: NON-BOM TEAM ---------------- #
elif selected == "Non-BOM Team":
    st.title("📦 Non-BOM & Consumables")
    tab1, tab2 = st.tabs(["Daily Tracker", "Advance Payments"])
    
    with tab1:
        st.subheader("Daily PR/PO Tracker")
        plant = st.text_input("Plant Location")
        if st.button("Log Daily Activity"):
            add_audit_log("ADMIN", "NON_BOM_DAILY", f"Activity logged for {plant}")
            st.toast(f"Activity for {plant} saved!")

# ---------------- MODULE 4: AUDIT LOGS ---------------- #
elif selected == "Audit Logs":
    st.title("📜 System Audit Logs")
    st.markdown("Track every action taken by users across the portal.")
    
    if st.session_state.audit_logs:
        log_df = pd.DataFrame(st.session_state.audit_logs)
        # Reverse to show newest logs first
        st.dataframe(log_df.iloc[::-1], use_container_width=True)
        
        if st.button("Clear Logs"):
            st.session_state.audit_logs = []
            st.rerun()
    else:
        st.info("No logs generated yet.")
