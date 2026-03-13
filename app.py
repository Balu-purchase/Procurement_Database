import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. INITIALIZATION ---
st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

if "master_data" not in st.session_state: 
    st.session_state.master_data = []
if "auth" not in st.session_state: 
    st.session_state.auth = False
if "role" not in st.session_state: 
    st.session_state.role = None

# --- Helper Functions ---
def get_signature():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"SIGNED BY {st.session_state.role} @ {now}"

def style_status(val):
    val_upper = str(val).upper()
    if "SUCCESSFULLY APPROVED" in val_upper or "SIGNED BY" in val_upper: 
        return 'background-color: green; color: white; font-weight: bold'
    elif "PENDING" in val_upper: 
        return 'background-color: #FFCC00; color: black; font-weight: bold'
    elif "REJECTED" in val_upper: 
        return 'background-color: red; color: white; font-weight: bold'
    return ''

# --- 2. LOGIN PAGE ---
if not st.session_state.auth:
    login_col, img_col = st.columns([1, 2])
    with login_col:
        st.markdown("# 🏗️ Resolute \n### Procurement Portal")
        st.divider()
        uid = st.text_input("Username", key="l_user").strip().upper() 
        upw = st.text_input("Password", type="password", key="l_pass")
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
        st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&q=80&w=1200", use_container_width=True)
    st.stop()

# --- 3. DASHBOARD ---
else:
    st.sidebar.title(f"👤 {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    if st.session_state.role in ["HOD", "GM_OFFICE"]:
        menu = st.sidebar.radio("NAVIGATE", ["PENDING APPROVALS", "AUDIT LOGS"])
    else:
        menu = "MAIN"

    st.title("PRICE APPROVALS FOR BOM ITEMS")
    st.divider()

    # --- 🔵 BOM & NON-BOM TEAM MODULE ---
    if st.session_state.role in ["BOMTEAM", "NONBOMTEAM"]:
        st.header(f"🛠️ {st.session_state.role}: New Request")
        with st.form("entry_form", clear_on_submit=True):
            r1c1, r1c2, r1c3, r1c4 = st.columns(4)
            p_proj = r1c1.text_input("PROJECT")
            p_num = r1c2.text_input("PART NUMBER")
            p_desc = r1c3.text_input("DESCRIPTION")
            p_qps = r1c4.text_input("QPS")
            
            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            p_uom = r2c1.selectbox("UOM", ["Nos", "KG", "Mtr", "Sets"])
            p_supp = r2c2.text_input("SUPPLIER NAME")
            p_price = r2c3.text_input("PRICE")
            p_rem = r2c4.text_input("REMARKS")
            
            # Form Submit Button
            submit_btn = st.form_submit_button("SUBMIT FOR APPROVAL")
            
            if submit_btn:
                st.session_state.master_data.append({
                    "VENDOR NAME": p_supp, "PART NUMBER": p_num, "MATERIAL DESCRIPTION": p_desc, 
                    "PRICE": p_price, "QPS": p_qps, "UOM": p_uom, "REMARKS": p_rem,
                    "HOD_SIGN": "PENDING", "GM_SIGN": "PENDING", "STATUS": "PENDING AT HOD"
                })
                st.success("Request Submitted Successfully!")
                st.rerun()
        
        st.subheader("📋 My Submission Status")
        if st.session_state.master_data:
            df_view = pd.DataFrame(st.session_state.master_data)
            st.dataframe(df_view.style.applymap(style_status, subset=['STATUS', 'HOD_SIGN', 'GM_SIGN']), use_container_width=True)

    # --- 🟠 HOD & GM APPROVAL (WATERFALL LOGIC) ---
    elif menu == "PENDING APPROVALS":
        st.header(f"🖊️ {st.session_state.role} Approval Queue")
        has_pending = False
        for i, row in enumerate(st.session_state.master_data):
            show = (st.session_state.role == "HOD" and row["STATUS"] == "PENDING AT HOD") or \
                   (st.session_state.role == "GM_OFFICE" and row["STATUS"] == "PENDING AT GM")
            
            if show:
                has_pending = True
                with st.container(border=True):
                    st.write(f"**VENDOR:** {row['VENDOR NAME']} | **PART:** {row['PART NUMBER']} | **PRICE:** {row['PRICE']}")
                    c1, col2 = st.columns(2)
                    if c1.button(f"✅ DIGITALLY SIGN AS {st.session_state.role}", key=f"s_{i}"):
                        sig = get_signature()
                        if st.session_state.role == "HOD":
                            st.session_state.master_data[i].update({"HOD_SIGN": sig, "STATUS": "PENDING AT GM"})
                        else:
                            st.session_state.master_data[i].update({"GM_SIGN": sig, "STATUS": "SUCCESSFULLY APPROVED"})
                        st.rerun()
                    if col2.button(f"❌ REJECT", key=f"r_{i}"):
                        st.session_state.master_data[i]["STATUS"] = f"REJECTED BY {st.session_state.role}"
                        st.session_state.master_data[i]["HOD_SIGN" if st.session_state.role == "HOD" else "GM_SIGN"] = "REJECTED"
                        st.rerun()
        if not has_pending: st.info("No pending tasks available.")

    # --- 📊 AUDIT LOGS ---
    elif menu == "AUDIT LOGS":
        st.header("📝 Transaction Audit Logs")
        if st.session_state.master_data:
            df_audit = pd.DataFrame(st.session_state.master_data)
            st.dataframe(df_audit.style.applymap(style_status, subset=['STATUS', 'HOD_SIGN', 'GM_SIGN']), use_container_width=True)
        else:
            st.info("No records found.")
