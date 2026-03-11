import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import io

st.set_page_config(page_title="Factory Procurement Portal", layout="wide")

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
FACTORY PROCUREMENT APPROVAL

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

        st.title("LOGIN")

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
        use_container_width=True)


# ---------------- MAIN SYSTEM ---------------- #

else:

    role = st.session_state.role
    st.sidebar.write("Logged in:", role)


# ---------------- BOM TEAM ---------------- #

    if role == "BOMTEAM":

        st.header("BOM Request Form")

        with st.form("bom_form"):

            vendor = st.text_input("Vendor")
            part = st.text_input("Part Number")
            desc = st.text_input("Description")
            price = st.number_input("Price")

            qps = st.text_input("QPS")

            bom_type = st.selectbox("BOM Type",
                ["Normal BOM","Alternate BOM","New Development"])

            additional = st.text_area("Additional Comments")

            if st.form_submit_button("Submit"):

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

                    "CREATED_TIME":datetime.now(),
                    "HOD_TIME":"",
                    "GM_TIME":"",

                    "STATUS":"PENDING HOD"
                })

                send_email(
                    EMAILS["HOD"],
                    "New BOM Request",
                    f"{vendor} request waiting approval"
                )

        if st.session_state.bom_data:

            df = pd.DataFrame(st.session_state.bom_data)
            st.dataframe(df)


# ---------------- HOD APPROVAL ---------------- #

    if role == "HOD":

        for i,row in enumerate(st.session_state.bom_data):

            if row["STATUS"]=="PENDING HOD":

                st.write(row["Vendor"],row["Part"])

                comment = st.text_input("HOD Comment",key=i)

                if st.button("Approve",key=f"a{i}"):

                    st.session_state.bom_data[i]["HOD_COMMENTS"]=comment
                    st.session_state.bom_data[i]["HOD_TIME"]=datetime.now()
                    st.session_state.bom_data[i]["STATUS"]="PENDING GM"

                    send_email(
                        EMAILS["GM_OFFICE"],
                        "Waiting GM Approval",
                        row["Vendor"]
                    )

                if st.button("Reject",key=f"r{i}"):

                    st.session_state.bom_data[i]["STATUS"]="REJECTED"

                    send_email(
                        EMAILS["BOMTEAM"],
                        "Request Rejected",
                        row["Vendor"]
                    )


# ---------------- GM APPROVAL ---------------- #

    if role == "GM_OFFICE":

        st.header("GM Dashboard")

        for i,row in enumerate(st.session_state.bom_data):

            if row["STATUS"]=="PENDING GM":

                st.write(row["Vendor"],row["Part"])

                comment = st.text_input("GM Comment",key=f"g{i}")

                if st.button("Approve",key=f"ga{i}"):

                    st.session_state.bom_data[i]["GM_COMMENTS"]=comment
                    st.session_state.bom_data[i]["GM_TIME"]=datetime.now()
                    st.session_state.bom_data[i]["STATUS"]="APPROVED"

                    send_email(
                        EMAILS["BOMTEAM"],
                        "Request Approved",
                        row["Vendor"]
                    )

        approved = [r for r in st.session_state.bom_data if r["STATUS"]=="APPROVED"]

        if approved:

            st.subheader("Approved Requests")

            df = pd.DataFrame(approved)
            st.dataframe(df)

            for r in approved:

                file_data = generate_approval_file(r)

                st.download_button(
                    "Download Approval File",
                    file_data,
                    file_name=f"BOM_APPROVAL_{r['Vendor']}.txt"
                )


# ---------------- NON BOM TEAM ---------------- #

    if role == "NONBOMTEAM":

        tab1,tab2,tab3 = st.tabs(
            ["Daily Tracker","Advance Payment","MIS Tracker"]
        )


# DAILY TRACKER

        with tab1:

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


# ADVANCE PAYMENT

        with tab2:

            with st.form("advance"):

                vendor = st.text_input("Vendor")
                type = st.selectbox(
                    "Type",
                    ["Advance","Final","Part Payment"]
                )

                po = st.text_input("PO Number")
                amount = st.number_input("Amount")

                if st.form_submit_button("Submit"):

                    st.session_state.advance_data.append({

                        "Vendor":vendor,
                        "Type":type,
                        "PO":po,
                        "Amount":amount
                    })

            if st.session_state.advance_data:

                df = pd.DataFrame(st.session_state.advance_data)
                st.dataframe(df)


# MIS TRACKER

        with tab3:

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

                st.subheader("Vendor Spend Chart")

                chart = df.groupby("Supplier")["Amount"].sum()

                st.bar_chart(chart)
