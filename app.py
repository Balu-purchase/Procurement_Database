import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Resolute Procurement Portal", layout="wide")

# ---------------- COMPANY HEADER ---------------- #

LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/3/3a/Logo_placeholder.png"

col1, col2, col3 = st.columns([1,4,1])

with col1:
    st.image(LOGO_URL, width=110)

with col2:
    st.markdown(
        "<h1 style='text-align:center;color:#0B5ED7;'>Resolute Electronics Procurement Portal</h1>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------- EMAIL SETTINGS ---------------- #

EMAIL_ADDRESS = "jampina.balanaresh@gmail.com"
EMAIL_PASSWORD = "YOUR_APP_PASSWORD"

EMAILS = {
    "BOMTEAM": "jampina.balanaresh@gmail.com",
    "HOD": "balanareshbalu@gmail.com",
    "GM_OFFICE": "purchase@resoluteelectronics.com"
}

def send_email(to_email, subject, message):

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

    except:
        pass


# ---------------- APPROVAL FILE GENERATOR ---------------- #

def generate_approval_file(row):

    text = f"""
RESOLUTE ELECTRONICS PROCUREMENT APPROVAL

Vendor : {row['Vendor']}
Part Number : {row['Part']}
Description : {row['Description']}
Price : {row['Price']}
QPS : {row['QPS']}
BOM Type : {row['BOM']}

Additional Comments :
{row['Additional']}

HOD Comments :
{row['HOD_COMMENTS']}

GM Comments :
{row['GM_COMMENTS']}

Status : {row['STATUS']}
"""

    return text


# ---------------- SESSION STORAGE ---------------- #

if "bom_data" not in st.session_state:
    st.session_state.bom_data = []

if "mis_data" not in st.session_state:
    st.session_state.mis_data = []

if "advance_data" not in st.session_state:
    st.session_state.advance_data = []

if "daily_data" not in st.session_state:
    st.session_state.daily_data = []

if "auth" not in st.session_state:
    st.session_state.auth = False


# ---------------- LOGIN PAGE ---------------- #

if not st.session_state.auth:

    col1, col2 = st.columns([1,2])

    with col1:

        st.subheader("User Login")

        uid = st.text_input("Username").upper()
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):

            users = {
                "BOMTEAM":"BOM123",
                "NONBOMTEAM":"NON123",
                "HOD":"HOD123",
                "GM_OFFICE":"GM123"
            }

            if uid in users and users[uid]==pwd:

                st.session_state.auth=True
                st.session_state.role=uid
                st.rerun()

    with col2:

        st.image(
            "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d",
            use_container_width=True
        )


# ---------------- MAIN SYSTEM ---------------- #

else:

    role = st.session_state.role

    st.sidebar.image(LOGO_URL, width=120)
    st.sidebar.write("Logged in as:", role)

# ---------------- BOM TEAM MODULE ---------------- #

    if role == "BOMTEAM":

        st.header("BOM Request Form")

        with st.form("bom_form"):

            vendor = st.text_input("Vendor")
            part = st.text_input("Part Number")
            desc = st.text_input("Description")
            price = st.number_input("Price")

            qps = st.text_input("QPS")

            bom_type = st.selectbox(
                "BOM Type",
                ["Normal BOM","Alternate BOM","New Development"]
            )

            additional = st.text_area("Additional Comments")

            if st.form_submit_button("Submit Request"):

                st.session_state.bom_data.append({

                    "Vendor":vendor,
                    "Part":part,
                    "Description":desc,
                    "Price":price,
                    "QPS":qps,
                    "BOM":bom_type,
                    "Additional":additional,

                    "HOD_COMMENTS":"",
                    "GM_COMMENTS":"",
                    "STATUS":"PENDING HOD"
                })

                send_email(
                    EMAILS["HOD"],
                    "New BOM Request Waiting Approval",
                    vendor
                )

        if st.session_state.bom_data:

            st.subheader("Submitted Requests")

            df = pd.DataFrame(st.session_state.bom_data)
            st.dataframe(df)


# ---------------- HOD APPROVAL ---------------- #

    if role == "HOD":

        st.header("HOD Approval Panel")

        for i,row in enumerate(st.session_state.bom_data):

            if row["STATUS"]=="PENDING HOD":

                st.write(row["Vendor"], row["Part"])

                comment = st.text_input("HOD Comment", key=i)

                if st.button("Approve", key=f"a{i}"):

                    st.session_state.bom_data[i]["HOD_COMMENTS"]=comment
                    st.session_state.bom_data[i]["STATUS"]="PENDING GM"

                if st.button("Reject", key=f"r{i}"):

                    st.session_state.bom_data[i]["STATUS"]="REJECTED"


# ---------------- GM DASHBOARD ---------------- #

    if role == "GM_OFFICE":

        st.header("GM Approval Dashboard")

        for i,row in enumerate(st.session_state.bom_data):

            if row["STATUS"]=="PENDING GM":

                st.write(row["Vendor"], row["Part"])

                comment = st.text_input("GM Comment", key=f"g{i}")

                if st.button("Approve", key=f"ga{i}"):

                    st.session_state.bom_data[i]["GM_COMMENTS"]=comment
                    st.session_state.bom_data[i]["STATUS"]="APPROVED"

        approved = [
            r for r in st.session_state.bom_data
            if r["STATUS"]=="APPROVED"
        ]

        if approved:

            st.subheader("Approved BOM Requests")

            df = pd.DataFrame(approved)
            st.dataframe(df)

            for r in approved:

                file_data = generate_approval_file(r)

                st.download_button(
                    "Download Approval File",
                    file_data,
                    file_name=f"BOM_APPROVAL_{r['Vendor']}.txt"
                )


# ---------------- NON BOM MODULE ---------------- #

    if role == "NONBOMTEAM":

        tab1,tab2,tab3 = st.tabs(
            ["Daily Tracker","Advance Payment","MIS Tracker"]
        )

        with tab1:

            st.subheader("Daily Purchase Tracker")

            with st.form("daily"):

                plant = st.text_input("Plant")
                pr = st.number_input("PR Received")
                po = st.number_input("PO Created")

                if st.form_submit_button("Submit"):

                    st.session_state.daily_data.append({

                        "Plant":plant,
                        "PR":pr,
                        "PO":po,
                        "Balance":pr-po
                    })

            if st.session_state.daily_data:
                st.dataframe(pd.DataFrame(st.session_state.daily_data))


        with tab2:

            st.subheader("Advance Payment Request")

            with st.form("advance"):

                vendor = st.text_input("Vendor")
                payment_type = st.selectbox(
                    "Payment Type",
                    ["Advance","Final","Part Payment"]
                )

                po = st.text_input("PO Number")
                amount = st.number_input("Amount")

                if st.form_submit_button("Submit"):

                    st.session_state.advance_data.append({

                        "Vendor":vendor,
                        "Type":payment_type,
                        "PO":po,
                        "Amount":amount
                    })

            if st.session_state.advance_data:
                st.dataframe(pd.DataFrame(st.session_state.advance_data))


        with tab3:

            st.subheader("Monthly MIS Tracker")

            with st.form("mis"):

                supplier = st.text_input("Supplier")
                po = st.text_input("PO No")
                qty = st.number_input("Qty")
                received = st.number_input("Received Qty")
                amount = st.number_input("Amount")

                if st.form_submit_button("Submit"):

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

                st.dataframe(df)

                st.subheader("Vendor Spend Analytics")

                chart = df.groupby("Supplier")["Amount"].sum()

                st.bar_chart(chart)
