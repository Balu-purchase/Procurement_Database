import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import io
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Procurement Portal",layout="wide")

EMAIL_ADDRESS="jampina.balanaresh@gmail.com"
EMAIL_PASSWORD="YOUR_APP_PASSWORD"

EMAILS={
"BOMTEAM":"jampina.balanaresh@gmail.com",
"HOD":"balanareshbalu@gmail.com",
"GM_OFFICE":"purchase@resoluteelectronics.com"
}

def send_email(to_email,subject,message):

    try:
        msg=MIMEText(message)
        msg["Subject"]=subject
        msg["From"]=EMAIL_ADDRESS
        msg["To"]=to_email

        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
    except:
        pass

def generate_pdf(row):

    buffer=io.BytesIO()

    data=[
    ["Vendor",row["Vendor"]],
    ["Part",row["Part"]],
    ["Price",row["Price"]],
    ["QPS",row["QPS"]],
    ["BOM",row["BOM"]],
    ["HOD Comments",row["HOD_COMMENTS"]],
    ["GM Comments",row["GM_COMMENTS"]],
    ["Status",row["STATUS"]]
    ]

    pdf=SimpleDocTemplate(buffer,pagesize=A4)
    table=Table(data)
    pdf.build([table])
    buffer.seek(0)

    return buffer

if "master_data" not in st.session_state:
    st.session_state.master_data=[]

if "mis_data" not in st.session_state:
    st.session_state.mis_data=[]

if "advance_payments" not in st.session_state:
    st.session_state.advance_payments=[]

if "auth" not in st.session_state:
    st.session_state.auth=False

if not st.session_state.auth:

    col1,col2=st.columns([1,2])

    with col1:

        st.title("Login")

        uid=st.text_input("Username").upper()
        pwd=st.text_input("Password",type="password")

        if st.button("Login"):

            users={
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

        st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d",use_container_width=True)

else:

    role=st.session_state.role

    st.sidebar.write(role)

    if role=="BOMTEAM":

        st.header("Create BOM Request")

        with st.form("bom"):

            vendor=st.text_input("Vendor")
            part=st.text_input("Part Number")
            desc=st.text_input("Description")
            price=st.number_input("Price")
            qps=st.text_input("QPS")
            bom=st.selectbox("BOM Type",["Normal","Alternate","New"])
            add=st.text_area("Additional Comments")

            if st.form_submit_button("Submit"):

                st.session_state.master_data.append({

                "Vendor":vendor,
                "Part":part,
                "Description":desc,
                "Price":price,
                "QPS":qps,
                "BOM":bom,
                "Additional":add,

                "HOD_COMMENTS":"",
                "GM_COMMENTS":"",

                "CREATED":datetime.now(),
                "HOD_TIME":"",
                "GM_TIME":"",

                "STATUS":"PENDING HOD"

                })

                send_email(EMAILS["HOD"],"New BOM Request",vendor)

        if st.session_state.master_data:

            df=pd.DataFrame(st.session_state.master_data)
            st.dataframe(df)

    if role=="HOD":

        for i,row in enumerate(st.session_state.master_data):

            if row["STATUS"]=="PENDING HOD":

                st.write(row["Vendor"],row["Part"])

                comment=st.text_input("HOD Comment",key=i)

                if st.button("Approve",key="a"+str(i)):

                    st.session_state.master_data[i]["HOD_COMMENTS"]=comment
                    st.session_state.master_data[i]["HOD_TIME"]=datetime.now()
                    st.session_state.master_data[i]["STATUS"]="PENDING GM"

                    send_email(EMAILS["GM_OFFICE"],"Waiting GM Approval",row["Vendor"])

                if st.button("Reject",key="r"+str(i)):

                    st.session_state.master_data[i]["STATUS"]="REJECTED"

                    send_email(EMAILS["BOMTEAM"],"Request Rejected",row["Vendor"])

    if role=="GM_OFFICE":

        for i,row in enumerate(st.session_state.master_data):

            if row["STATUS"]=="PENDING GM":

                st.write(row["Vendor"],row["Part"])

                comment=st.text_input("GM Comment",key="g"+str(i))

                if st.button("Approve",key="ga"+str(i)):

                    st.session_state.master_data[i]["GM_COMMENTS"]=comment
                    st.session_state.master_data[i]["GM_TIME"]=datetime.now()
                    st.session_state.master_data[i]["STATUS"]="APPROVED"

                    send_email(EMAILS["BOMTEAM"],"Request Approved",row["Vendor"])

        st.header("GM Dashboard")

        if st.session_state.mis_data:

            df=pd.DataFrame(st.session_state.mis_data)

            st.bar_chart(df.groupby("Supplier")["Amount"].sum())

    if role=="NONBOMTEAM":

        tab1,tab2=st.tabs(["Advance Payment","MIS"])

        with tab1:

            with st.form("adv"):

                vendor=st.text_input("Vendor")
                type=st.selectbox("Type",["Advance","Final","Part"])
                po=st.text_input("PO")
                amount=st.number_input("Amount")

                if st.form_submit_button("Add"):

                    st.session_state.advance_payments.append({

                    "Vendor":vendor,
                    "Type":type,
                    "PO":po,
                    "Amount":amount

                    })

            if st.session_state.advance_payments:

                st.dataframe(pd.DataFrame(st.session_state.advance_payments))

        with tab2:

            with st.form("mis"):

                sup=st.text_input("Supplier")
                po=st.text_input("PO")
                qty=st.number_input("Qty")
                rec=st.number_input("Received")
                amt=st.number_input("Amount")

                if st.form_submit_button("Submit"):

                    st.session_state.mis_data.append({

                    "Supplier":sup,
                    "PO":po,
                    "Qty":qty,
                    "Received":rec,
                    "Pending":qty-rec,
                    "Amount":amt

                    })

            if st.session_state.mis_data:

                df=pd.DataFrame(st.session_state.mis_data)

                st.dataframe(df)

                st.bar_chart(df.groupby("Supplier")["Amount"].sum())
