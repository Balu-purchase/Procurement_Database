import streamlit as st
import pandas as pd
from datetime import datetime

# Optional: Plotly for charts
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# Persistent state management
state_keys = {
    "auth": False, "role": None, "master_data": [], 
    "daily_tracker": [], "advance_payments": [], 
    "mis_data": [], "nb_choice": "DAILY" 
}
for key, default in state_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Helper Functions for Styling ---
def style_status(val):
    val_upper = str(val).upper()
    if val_upper in ["APPROVED", "CLOSED", "DONE", "RECEIVED", "ACCOUNTED"]: 
        return 'background-color: green; color: white; font-weight: bold'
    if val_upper in ["REJECTED", "PENDING", "INCOMPLETE"]: 
        return 'background-color: red; color: white; font-weight: bold'
    if val_upper in ["OPEN", "INPROCESS"]: 
        return 'background-color: orange; color: black; font-weight: bold'
    return ''

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://t3.ftcdn.net/jpg/09/94/98/98/360_F_994989868_JVms41RbTVCoI1wmY7JOwTGG3CsGQ8wr.webp");
        background-size: cover; background-position: center;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.9); border-radius: 10px; padding: 20px;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    _, col_login = st.columns([1.8, 1])
    with col_login:
        st.write("###")
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #333;'>SYSTEM LOGIN</h2>", unsafe_allow_html=True)
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
    
    # Navigation logic
    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("GO TO", ["BOM", "NONBOM", "AUDIT LOGS"])
    else:
        menu = "MAIN"

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.title("Factory Procurement Dashboard")
    st.divider()

    # --- 🟢 NON-BOM TEAM MODULE ---
    if st.session_state.role == "NONBOMTEAM" or (menu == "NONBOM" and st.session_state.role in ["HOD", "GM_OFFICE"]):
        st.header("📦 Non-BOM Activity Management")
        tab1, tab2, tab3 = st.tabs(["📅 DAILY TRACKER", "💳 ADVANCE PAYMENT", "📊 MIS TRACKER"])
        
        # --- TAB 1: DAILY TRACKER ---
        with tab1:
            if st.session_state.role == "NONBOMTEAM":
                st.subheader("Daily PR to PO Tracker Entry")
                with st.form("dt_form", clear_on_submit=True):
                    c1, c2, c3, c4 = st.columns(4)
                    d_date = c1.date_input("DATE")
                    d_plant = c2.text_input("PLANT")
                    d_pr = c3.number_input("PR RECEIPTS", min_value=0)
                    d_po = c4.number_input("PO DONE", min_value=0)
                    if st.form_submit_button("SUBMIT ENTRY"):
                        st.session_state.daily_tracker.append({
                            "S.NO": len(st.session_state.daily_tracker)+1, "DATE": str(d_date), 
                            "PLANT": d_plant, "PR RECEIPTS": d_pr, "PO DONE": d_po, 
                            "BALANCE PR'S": d_pr - d_po, "HOD COMMENTS": ""
                        })
                        st.rerun()

            st.subheader("Daily PR to PO Data")
            if st.session_state.daily_tracker:
                df_dt = pd.DataFrame(st.session_state.daily_tracker)
                st.dataframe(df_dt, use_container_width=True)

        # --- TAB 2: ADVANCE PAYMENT ---
        with tab2:
            if st.session_state.role == "NONBOMTEAM":
                st.subheader("Advance Payment Manual Entry")
                with st.form("adv_form", clear_on_submit=True):
                    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
                    v_name = r1c1.text_input("VENDOR NAME")
                    v_type = r1c2.selectbox("TYPE", ["Advance", "Partial", "Full"])
                    v_pi = r1c3.text_input("PI/INVOICE NO")
                    v_idate = r1c4.date_input("INVOICE DATE")
                    
                    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
                    v_po = r2c1.text_input("PO NO")
                    v_pdate = r2c2.date_input("PO DATE")
                    v_amt = r2c3.number_input("AMOUNT", min_value=0.0)
                    v_rem = r2c4.text_input("REMARKS")
                    
                    if st.form_submit_button("SUBMIT ADVANCE PAYMENT REQUEST"):
                        st.session_state.advance_payments.append({
                            "S NO.": len(st.session_state.advance_payments)+1,
                            "SUBMIT DATE": str(datetime.now().date()),
                            "VENDOR NAME": v_name, "TYPE": v_type, "PI/INVOICE NO": v_pi,
                            "INVOICE DATE": str(v_idate), "PO NO": v_po, "PO DATE": str(v_pdate),
                            "AMOUNT": v_amt, "REMARKS": v_rem,
                            "PAYMENT STATUS": "PENDING", "PAID ON": "N/A",
                            "MATERIAL STATUS": "PENDING", "RECEIVED ON": "N/A",
                            "GRN No": "PENDING", "PIC": "N/A",
                            "TAX INVOICE NO": "N/A", "ACCOUNTING STATUS": "PENDING"
                        })
                        st.success("Entry Added")
                        st.rerun()

            st.subheader("Advance Payment Tracker Table")
            if st.session_state.advance_payments:
                df_adv = pd.DataFrame(st.session_state.advance_payments)
                # Apply styles to columns like PAYMENT STATUS and ACCOUNTING STATUS
                styled_adv = df_adv.style.applymap(style_status, subset=["PAYMENT STATUS", "MATERIAL STATUS", "ACCOUNTING STATUS"])
                st.dataframe(styled_adv, use_container_width=True)

        # --- TAB 3: MIS TRACKER ---
        with tab3:
            if st.session_state.role == "NONBOMTEAM":
                st.subheader("MIS Data Entry")
                with st.form("mis_form", clear_on_submit=True):
                    m1, m2, m3, m4 = st.columns(4)
                    m_supp = m1.text_input("SUPPLIER NAME")
                    m_po = m2.text_input("MIS PO NO")
                    m_pdate = m3.date_input("MIS PO DATE")
                    m_part = m4.text_input("PART NO")
                    
                    m5, m6, m7, m8 = st.columns(4)
                    m_desc = m5.text_input("MATERIAL DESCRIPTION")
                    m_qty = m6.number_input("QUANTITY", min_value=0)
                    m_uom = m7.selectbox("UOM", ["Nos", "KG", "Mtr", "Sets"])
                    m_price = m8.number_input("Act Unit Price", min_value=0.0)
                    
                    if st.form_submit_button("SUBMIT MIS DATA"):
                        st.session_state.mis_data.append({
                            "S.NO": len(st.session_state.mis_data)+1, "SUPPLIER NAME": m_supp,
                            "PO NO": m_po, "PO DATE": str(m_pdate), "PART NO": m_part,
                            "MATERIAL DESCRIPTION": m_desc, "QUANTITY": m_qty, "UOM": m_uom,
                            "Act Unit price": m_price, "Act Basic Amt": m_qty * m_price,
                            "RECEIVED QTY": 0, "PENDING QTY": m_qty, "GRN NO": "PENDING", "GRNDATE": "N/A",
                            "PAYMENT STATUS": "INCOMPLETE", "PAYMENT DATE": "N/A",
                            "MATERIAL RECEIVE DATE": "N/A", "INVOICE NO": "N/A",
                            "ACCOUNTING STATUS": "PENDING"
                        })
                        st.rerun()

            st.subheader("MIS Tracker Table")
            if st.session_state.mis_data:
                df_mis = pd.DataFrame(st.session_state.mis_data)
                # Apply logic for selection mode visualization (simulated via status coloring)
                styled_mis = df_mis.style.applymap(style_status, subset=["PAYMENT STATUS", "ACCOUNTING STATUS"])
                st.dataframe(styled_mis, use_container_width=True)

    # --- 🔵 BOM TEAM MODULE ---
    elif st.session_state.role == "BOMTEAM" or (menu == "BOM" and st.session_state.role in ["HOD", "GM_OFFICE"]):
        st.header("🛠️ BOM Procurement Requests")
        # (Existing BOM code would go here - preserved space for your existing logic)
        st.info("BOM Module Content Loaded")

    # --- 📊 AUDIT LOGS ---
    elif menu == "AUDIT LOGS":
        st.header("📝 System Audit Logs")
        st.write("All Transaction Histories")
        # Combined view or master list
