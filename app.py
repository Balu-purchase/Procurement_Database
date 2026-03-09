import streamlit as st

# --- CONFIGURATION ---
# I have extracted the 'sourcedoc' ID from your link to create an Embed URL
SOURCE_ID = "%7BF2846EF8-4072-48E3-AE3B-A9848FA1578F%7D"
# This link tells SharePoint to show the file in 'embed' mode
EMBED_URL = f"https://resolutegroups-my.sharepoint.com/:x:/g/personal/purchase_resoluteelectronics_com/_layouts/15/Doc.aspx?sourcedoc={SOURCE_ID}&action=embedview"

st.set_page_config(page_title="Resolute Procurement Portal", layout="wide")

# --- LOGIN SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.sidebar.title("🔐 Secure Access")
    role = st.sidebar.selectbox("Select Team", ["BOM Team", "Non-BOM Team", "GM Management"])
    pwd = st.sidebar.text_input("Enter Passkey", type="password")
    
    if st.sidebar.button("Login"):
        # Your specific passwords
        creds = {"BOM Team": "BOM2026", "Non-BOM Team": "NBOM2026", "GM Management": "GM789"}
        if pwd == creds.get(role):
            st.session_state.logged_in = True
            st.session_state.role = role
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid Passkey")

# --- LIVE VIEW INTERFACE ---
else:
    st.title("🏭 Daily Procurement Tracking")
    st.write(f"Showing live data for: **{st.session_state.role}**")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # This creates the live window to your Excel file
    # It will auto-update whenever the Excel file is changed
    st.components.v1.html(
        f"""
        <iframe 
            width="100%" 
            height="800" 
            frameborder="0" 
            scrolling="no" 
            src="{EMBED_URL}">
        </iframe>
        """,
        height=800,
    )

st.markdown("---")
st.caption("Resolute Electronics | Live SharePoint Sync")
