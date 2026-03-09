import streamlit as st
import pandas as pd
from datetime import datetime

# 1. SETUP
st.set_page_config(page_title="BOM Approval", layout="wide")

# 2. CONFIG
H_N = "Bixapathi"
H_D = "Head of Department (HOD)"
G_N = "General Manager"

# 3. LOGIN
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.sidebar.title("🔐 OFFICIAL LOGIN")
    uid = st.sidebar.text_input("ID")
    upw = st.sidebar.text_input("PW", type="password")
    if st.sidebar.button("LOG IN"):
        db = {"hod_office": "HOD789", "gm_office": "GM2026"}
        if uid in db and db[uid] == upw:
            st.session_state.auth = True
            st.session_state.u_role = "HOD" if "hod" in uid else "GM"
            st.rerun()
    st.stop()

# 4. DATA LOADING
@st.cache_data(ttl=1)
def load():
    s = "1H43MSA3ff3KQ6QGVQLapkn9RjPR7e69V4s0JlOC_oI4"
    g = "466678125"
    u = "https://docs.google.com/spreadsheets/d/" + s + "/export?format=csv&gid=" + g
    try:
        df = pd.read_csv(u)
        df.columns = df.columns.str.strip().str.upper()
        return df
    except:
        return pd.DataFrame()

df = load()

# 5. NAVIGATION
m = st.sidebar.radio("MENU", ["PENDING APPROVALS", "OFFICIAL RECORDS"])
if st.sidebar.button("LOGOUT"):
    st.session_state.auth = False
    st.rerun()

# 6. PENDING APPROVALS
if m == "PENDING APPROVALS":
    st.header("🏭 PENDING PRICE VERIFICATION")
    role = st.session_state.get("u_role")
    
    if not df.empty:
        # Determine which column to check based on who is logged in
        T_C = "HOD APPROVAL" if role == "HOD" else "GM APPROVAL"
        V_C, P_C, R_C, S_C = "VENDOR NAME", "PART NUMBER", "PRICE", "BOM STATUS"

        # Show only rows where Approval is EMPTY (None/NaN)
        p_df = df[df[T_C].isna() | (df[T_C].astype(str).str.strip() == "")]

        if p_df.empty:
            st.success("✅ No pending items. Everything is approved!")
        else:
            # Table Header
            h1, h2, h3, h4, h5 = st.columns([2, 2, 1, 2, 1])
            h1.subheader("VENDOR")
            h2.subheader("PART NO")
            h3.subheader("PRICE")
            h4.subheader("SIGNATURE")
            h5.subheader("ACTION")

            for i, r in p_df.iterrows():
                c1, c2, c3, c4, c5 = st.columns([2, 2, 1, 2, 1])
                vn, pn, pr = str(r.get(V_C)), str(r.get(P_C)), str(r.get(R_C))
                c1.write(vn)
                c2.write(pn)
                c3.write(pr)
                
                sig = c4.text_input("Sig", key="sig"+str(i), label_visibility="collapsed")
                if c5.button("OK", key="btn"+str(i)):
                    if sig.upper() in ["OK", "APPROVED", "OKAY"]:
                        st.success("Successfully Approved: " + vn)
                        st.info("Note: Update your Excel sheet to see this move permanently.")
                st.divider()

# 7. OFFICIAL RECORDS (READING DIRECTLY FROM EXCEL)
else:
    st.header("📜 OFFICIAL ARCHIVED RECORDS")
    V_C, P_C, R_C, S_C = "VENDOR NAME", "PART NUMBER", "PRICE", "BOM STATUS"
    
    # Logic: If HOD APPROVAL contains "OK" or "APPROVED" in the Excel file
    if not df.empty:
        # Filter for rows that are ALREADY approved in the Google Sheet
        mask = df["HOD APPROVAL"].astype(str).str.upper().isin(["OK", "APPROVED", "OKAY"])
        approved_df = df[mask]

        if approved_df.empty:
            st.warning("No records found in Excel with 'OK' or 'APPROVED' in the HOD column.")
        else:
            for _, r in approved_df.iterrows():
                with st.container(border=True):
                    st.success("VERIFIED BY: " + H_N)
                    st.write("**VENDOR:** " + str(r.get(V_C)) + " | **PART:** " + str(r.get(P_C)))
                    st.write("**PRICE:** " + str(r.get(R_C)) + " | **STATUS:** " + str(r.get(S_C)))
                    st.write("**HOD COMMENT:** " + str(r.get("HOD APPROVAL")))
                    st.markdown("*Digital Signature: " + H_N + "*")
