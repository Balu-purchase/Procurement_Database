import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

# ------------------------------
# SESSION STORAGE
# ------------------------------

if "master_data" not in st.session_state:
    st.session_state.master_data = []

if "daily_tracker" not in st.session_state:
    st.session_state.daily_tracker = []

if "advance_payments" not in st.session_state:
    st.session_state.advance_payments = []

if "mis_data" not in st.session_state:
    st.session_state.mis_data = []

if "auth" not in st.session_state:
    st.session_state.auth = False

if "role" not in st.session_state:
    st.session_state.role = None

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------

def get_signature():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"SIGNED BY {st.session_state.role} @ {now}"

def style_status(val):
    if "APPROVED" in str(val):
        return "background-color:green;color:white;font-weight:bold"
    if "REJECTED" in str(val):
        return "background-color:red;color:white;font-weight:bold"
    if "PENDING" in str(val):
        return "background-color:orange;color:black;font-weight:bold"
    return ""

def export_excel(dataframe):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

# ------------------------------
# LOGIN PAGE
# ------------------------------

if not st.session_state.auth:

    col1,col2 = st.columns([1,2])

    with col1:
        st.title("LOGIN")

        uid = st.text_input("Username").upper()
        pwd = st.text_input("Password", type="password")

        if st.button("ENTER SYSTEM"):

            users = {
                "BOMTEAM":"BOM123",
                "NONBOMTEAM":"NONBOM123",
                "HOD":"HOD789",
                "GM_OFFICE":"GM2026"
            }

            if uid in users and users[uid] == pwd:
                st.session_state.auth = True
                st.session_state.role = uid
                st.rerun()
            else:
                st.error("Invalid Credentials")

    with col2:
        st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d",use_container_width=True)

# ------------------------------
# MAIN DASHBOARD
# ------------------------------

else:

    st.sidebar.title(f"👤 {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.auth=False
        st.rerun()

    if st.session_state.role in ["HOD","GM_OFFICE"]:
        menu = st.sidebar.radio("Navigation",[
            "PENDING APPROVALS",
            "NON-BOM REVIEW",
            "GM DASHBOARD",
            "AUDIT LOGS"
        ])
    else:
        menu="MAIN"

    st.title("FACTORY PROCUREMENT PORTAL")
    st.divider()

# ---------------------------------------------------------
# BOM TEAM MODULE
# ---------------------------------------------------------

    if st.session_state.role == "BOMTEAM":

        st.header("BOM PRICE REQUEST")

        with st.form("bom_form"):

            c1,c2,c3,c4 = st.columns(4)

            vendor = c1.text_input("Vendor")
            part = c2.text_input("Part Number")
            desc = c3.text_input("Description")
            price = c4.number_input("Price")

            qps = st.text_input("QPS")

            submit = st.form_submit_button("Submit Request")

            if submit:

                st.session_state.master_data.append({

                    "Vendor":vendor,
                    "Part":part,
                    "Description":desc,
                    "Price":price,
                    "QPS":qps,
                    "HOD_SIGN":"",
                    "GM_SIGN":"",
                    "STATUS":"PENDING AT HOD"

                })

                st.success("Request Submitted")

        if st.session_state.master_data:

            df = pd.DataFrame(st.session_state.master_data)

            st.dataframe(df.style.applymap(style_status,subset=["STATUS"]),use_container_width=True)

# ---------------------------------------------------------
# HOD / GM APPROVALS
# ---------------------------------------------------------

    elif menu == "PENDING APPROVALS":

        st.header("Approval Queue")

        for i,row in enumerate(st.session_state.master_data):

            show=False

            if st.session_state.role=="HOD" and row["STATUS"]=="PENDING AT HOD":
                show=True

            if st.session_state.role=="GM_OFFICE" and row["STATUS"]=="PENDING AT GM":
                show=True

            if show:

                st.container()

                st.write(f"{row['Vendor']} | {row['Part']} | {row['Price']}")

                c1,c2 = st.columns(2)

                if c1.button("APPROVE",key=f"a{i}"):

                    sig = get_signature()

                    if st.session_state.role=="HOD":
                        st.session_state.master_data[i]["HOD_SIGN"]=sig
                        st.session_state.master_data[i]["STATUS"]="PENDING AT GM"

                    else:
                        st.session_state.master_data[i]["GM_SIGN"]=sig
                        st.session_state.master_data[i]["STATUS"]="APPROVED"

                    st.rerun()

                if c2.button("REJECT",key=f"r{i}"):

                    st.session_state.master_data[i]["STATUS"]=f"REJECTED BY {st.session_state.role}"
                    st.rerun()

# ---------------------------------------------------------
# NON BOM TEAM
# ---------------------------------------------------------

    elif st.session_state.role == "NONBOMTEAM":

        tab1,tab2,tab3 = st.tabs(["DAILY TRACKER","ADVANCE PAYMENT REQUEST","MIS TRACKER"])

# DAILY TRACKER

        with tab1:

            with st.form("daily_form"):

                date = st.date_input("Date")
                plant = st.text_input("Plant")
                pr = st.number_input("PR Received")
                po = st.number_input("PO Done")

                if st.form_submit_button("Submit"):

                    st.session_state.daily_tracker.append({

                        "Date":date,
                        "Plant":plant,
                        "PR":pr,
                        "PO":po,
                        "Balance":pr-po

                    })

            if st.session_state.daily_tracker:

                df = pd.DataFrame(st.session_state.daily_tracker)
                st.dataframe(df,use_container_width=True)

# ADVANCE PAYMENT

        with tab2:

            with st.form("advance_form"):

                vendor = st.text_input("Vendor")
                type = st.selectbox("Type",["Advance","Final","Part Payment"])
                po = st.text_input("PO No")
                amount = st.number_input("Amount")

                status = st.selectbox("Payment Status",["PENDING","DONE","HOLD"])

                submit = st.form_submit_button("Submit")

                if submit:

                    st.session_state.advance_payments.append({

                        "Vendor":vendor,
                        "Type":type,
                        "PO":po,
                        "Amount":amount,
                        "Status":status

                    })

            if st.session_state.advance_payments:

                df = pd.DataFrame(st.session_state.advance_payments)

                st.dataframe(df,use_container_width=True)

                excel = export_excel(df)

                st.download_button(
                    "Download Excel",
                    excel,
                    "advance_payments.xlsx"
                )

# MIS TRACKER

        with tab3:

            with st.form("mis_form"):

                supplier = st.text_input("Supplier")
                po = st.text_input("PO No")
                qty = st.number_input("Qty")
                received = st.number_input("Received Qty")
                amount = st.number_input("Amount")

                submit = st.form_submit_button("Submit")

                if submit:

                    st.session_state.mis_data.append({

                        "Supplier":supplier,
                        "PO":po,
                        "Qty":qty,
                        "Received":received,
                        "Pending":qty-received,
                        "Amount":amount

                    })

            if st.session_state.mis_data:

                df = pd.DataFrame(st.session_state.mis_data)

                st.dataframe(df,use_container_width=True)

                st.subheader("MIS Chart")

                chart = df.groupby("Supplier")["Amount"].sum()

                st.bar_chart(chart)

                excel = export_excel(df)

                st.download_button(
                    "Download MIS Excel",
                    excel,
                    "mis_tracker.xlsx"
                )

# ---------------------------------------------------------
# GM PROFESSIONAL DASHBOARD
# ---------------------------------------------------------

    elif menu == "GM DASHBOARD":

        st.header("GM PROCUREMENT DASHBOARD")

        col1,col2,col3 = st.columns(3)

        total_po = len(st.session_state.mis_data)
        total_pay = sum([x["Amount"] for x in st.session_state.advance_payments]) if st.session_state.advance_payments else 0
        total_bom = len(st.session_state.master_data)

        col1.metric("Total MIS Entries",total_po)
        col2.metric("Total Advance Payments",total_pay)
        col3.metric("BOM Requests",total_bom)

        if st.session_state.mis_data:

            df = pd.DataFrame(st.session_state.mis_data)

            st.subheader("Supplier Wise Amount")

            chart = df.groupby("Supplier")["Amount"].sum()

            st.bar_chart(chart)

# ---------------------------------------------------------
# NON BOM REVIEW
# ---------------------------------------------------------

    elif menu=="NON-BOM REVIEW":

        st.header("Non BOM Review")

        if st.session_state.daily_tracker:
            st.write("Daily Tracker")
            st.dataframe(pd.DataFrame(st.session_state.daily_tracker))

        if st.session_state.advance_payments:
            st.write("Advance Payments")
            st.dataframe(pd.DataFrame(st.session_state.advance_payments))

        if st.session_state.mis_data:
            st.write("MIS Tracker")
            st.dataframe(pd.DataFrame(st.session_state.mis_data))

# ---------------------------------------------------------
# AUDIT LOGS
# ---------------------------------------------------------

    elif menu=="AUDIT LOGS":

        st.header("Audit Logs")

        if st.session_state.master_data:

            df = pd.DataFrame(st.session_state.master_data)

            st.dataframe(df.style.applymap(style_status,subset=["STATUS"]),use_container_width=True)
