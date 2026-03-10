import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

if "master_data" not in st.session_state: st.session_state.master_data = []
if "daily_tracker" not in st.session_state: st.session_state.daily_tracker = []
if "advance_payments" not in st.session_state: st.session_state.advance_payments = []

if "auth" not in st.session_state: st.session_state.auth = False
if "role" not in st.session_state: st.session_state.role = None

# --- Helper Functions for Stamps & Styles ---
def get_blue_stamp(role_name):
    """Creates an HTML/CSS Blue Round Digital Stamp."""
    now = datetime.now().strftime("%d %b %Y %H:%M")
    stamp_html = f"""
    <div style="
        border: 3px solid #0000FF;
        border-radius: 50%;
        width: 130px;
        height: 130px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #0000FF;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        line-height: 1.1;
        transform: rotate(-5deg);
        box-shadow: 2px 2px 5px rgba(0,0,255,0.2);
        background: rgba(255,255,255,0.8);
        padding: 5px;
        font-size: 10px;
    ">
        <div style="font-size: 8px; margin-bottom: 2px;">ELECTRONICS COMPANY</div>
        <div style="border-top: 1px solid #0000FF; border-bottom: 1px solid #0000FF; width: 80%; padding: 2px 0;">
            {role_name}<br>APPROVED
        </div>
        <div style="font-size: 8px; margin-top: 2px;">{now}</div>
    </div>
    """
    return stamp_html

def style_status(val):
    if val == "SUCCESSFULLY APPROVED": return 'background-color: #d4edda; color: #155724; font-weight: bold'
    if "PENDING AT GM" in val: return 'background-color: #cce5ff; color: #004085;'
    if "REJECTED" in val: return 'background-color: #f8d7da; color: #721c24;'
    return 'background-color: #fff3cd; color: #856404;'

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        st.markdown("<h2 style='text-align: center;'>PRICE APPROVALS LOGIN</h2>", unsafe_allow_html=True)
        uid = st.text_input("Username").strip().upper() 
        upw = st.text_input("Password", type="password")
        if st.button("ENTER SYSTEM", use_container_width=True):
            creds = {"BOMTEAM": "BOM123", "NONBOMTEAM": "NONBOM123", "HOD": "HOD789", "GM_OFFICE": "GM2026"}
            if uid in creds and creds[uid] == upw:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun() 
            else: st.error("Invalid Credentials.")

# --- 3. DASHBOARD PAGE ---
else:
    st.sidebar.title(f"👤 {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    menu = st.sidebar.radio("NAVIGATE", ["BOM REQUESTS", "AUDIT LOGS"]) if st.session_state.role in ["HOD", "GM_OFFICE"] else "MAIN"

    # --- 🔵 BOM TEAM MODULE ---
    if st.session_state.role == "BOMTEAM":
        st.header("🛠️ BOM Team Entry")
        with st.form("bom_entry", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            p_proj, p_supp, p_price = c1.text_input("PROJECT"), c2.text_input("VENDOR NAME"), c3.text_input("PRICE")
            p_desc = st.text_area("MATERIAL DESCRIPTION")
            if st.form_submit_button("SUBMIT"):
                st.session_state.master_data.append({
                    "VENDOR NAME": p_supp, "PROJECT": p_proj, "DESCRIPTION": p_desc, 
                    "PRICE": p_price, "HOD_STAMP": "", "GM_STAMP": "", "STATUS": "PENDING AT HOD"
                })
                st.rerun()
        
        if st.session_state.master_data:
            st.dataframe(pd.DataFrame(st.session_state.master_data).drop(columns=['HOD_STAMP', 'GM_STAMP']), use_container_width=True)

    # --- 🟠 HOD & GM APPROVAL (WATERFALL) ---
    elif menu == "BOM REQUESTS":
        st.header(f"🖊️ {st.session_state.role} Approval Queue")
        for i, row in enumerate(st.session_state.master_data):
            show = (st.session_state.role == "HOD" and row["STATUS"] == "PENDING AT HOD") or \
                   (st.session_state.role == "GM_OFFICE" and row["STATUS"] == "PENDING AT GM")
            if show:
                with st.container(border=True):
                    st.write(f"**VENDOR:** {row['VENDOR NAME']} | **PRICE:** {row['PRICE']}")
                    if st.button(f"✅ APPLY DIGITAL STAMP", key=f"s_{i}"):
                        stamp = get_blue_stamp(st.session_state.role)
                        if st.session_state.role == "HOD":
                            st.session_state.master_data[i].update({"HOD_STAMP": stamp, "STATUS": "PENDING AT GM"})
                        else:
                            st.session_state.master_data[i].update({"GM_STAMP": stamp, "STATUS": "SUCCESSFULLY APPROVED"})
                        st.rerun()

    # --- 📊 AUDIT LOGS (WITH VISUAL STAMPS) ---
    elif menu == "AUDIT LOGS":
        st.header("📁 Official Procurement Audit Trail")
        if not st.session_state.master_data:
            st.info("No records to display.")
        else:
            for row in st.session_state.master_data:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([2, 1, 1])
                    with c1:
                        st.markdown(f"**VENDOR:** {row['VENDOR NAME']}")
                        st.markdown(f"**PRICE:** {row['PRICE']}")
                        st.markdown(f"**STATUS:** {row['STATUS']}")
                    with c2:
                        if row['HOD_STAMP']:
                            st.markdown("##### HOD Signature")
                            st.markdown(row['HOD_STAMP'], unsafe_allow_html=True)
                    with c3:
                        if row['GM_STAMP']:
                            st.markdown("##### GM Signature")
                            st.markdown(row['GM_STAMP'], unsafe_allow_html=True)
