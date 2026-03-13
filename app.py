import streamlit as st
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Resolute Approval System", layout="wide")

# Replace st.secrets with "your_password" ONLY if you are not worried about security
SENDER_EMAIL = "balanareshbalu@gmail.com" 
EMAIL_PASS = st.secrets["17ME1A0126@balu"] 

MAIL_IDS = {
    "BOMTEAM": "balanareshbalu@gmail.com",
    "HOD": "purchase@resoluteelectronics.com",
    "GM": "purchase@resoluteelectronics.com"
}

WEB_LINK = "https://your-app-link.streamlit.app"
DB_FILE = "resolute_db.csv"

USERS = {
    "BOMTEAM": "BOM123",
    "NONBOMTEAM": "NONBOM123",
    "HOD": "HOD789",
    "GM": "GM123"
}

# --- 2. ADVANCED EMAIL ENGINE (With HTML Table & Buttons) ---
def send_approval_email(to_email, subject, request_data):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = f"Price approval request - {request_data['Request ID']}"
        
        # Create HTML Table for Email body
        html_table = f"""
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #004b93; color: white;">
                <th>Field</th><th>Value</th>
            </tr>
            <tr><td><b>Project</b></td><td>{request_data['Project']}</td></tr>
            <tr><td><b>Part Number</b></td><td>{request_data['Part Number']}</td></tr>
            <tr><td><b>Description</b></td><td>{request_data['Description']}</td></tr>
            <tr><td><b>BOM Qty</b></td><td>{request_data['BOM']}</td></tr>
            <tr><td><b>UOM</b></td><td>{request_data['UOM']}</td></tr>
            <tr><td><b>Supplier</b></td><td>{request_data['Supplier']}</td></tr>
            <tr><td><b>Unit Price</b></td><td>{request_data['Price']}</td></tr>
            <tr><td><b>Remarks</b></td><td>{request_data['Remarks']}</td></tr>
        </table>
        """

        body = f"""
        <html>
        <body>
            <p>Dear Sir,</p>
            <p>Please find the attached link and kindly waiting for your approval for that BOM item along with prices are attached for your reference. We are waiting for your reply.</p>
            {html_table}
            <br>
            <div style="text-align: center;">
                <a href="{WEB_LINK}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-right: 10px;">APPROVE VIA PORTAL</a>
                <a href="{WEB_LINK}" style="background-color: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">REJECT VIA PORTAL</a>
            </div>
            <p>Regards,<br>BOM Team</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

# Database Init
if not os.path.exists(DB_FILE):
    cols = ["Request ID", "Project", "Part Number", "Description", "BOM", "UOM", 
            "Supplier", "Price", "Remarks", "HOD Approval", "HOD Comments", 
            "GM Approval", "GM Comments", "Status", "Timestamp", "Raised By"]
    pd.DataFrame(columns=cols).to_csv(DB_FILE, index=False)

# Session Management
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None

# --- 3. LOGIN PAGE ---
if not st.session_state.auth:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("RESOLUTE LOGIN")
        u_sel = st.selectbox("Select Role", list(USERS.keys()))
        p_sel = st.text_input("Password", type="password")
        if st.button("SIGN IN", use_container_width=True):
            if p_sel == USERS[u_sel]:
                st.session_state.auth = True
                st.session_state.user = u_sel
                st.rerun()
            else: st.error("Wrong Password")
    with col2:
        st.info("### Price Approval Management System")
        st.image("https://img.freelancer.com/flux/8/1/81442490-674b-449e-8c33-a3bc531d0446.jpg")
    st.stop()

# --- 4. DATA HELPERS ---
def get_data(): return pd.read_csv(DB_FILE)
def save_data(df): df.to_csv(DB_FILE, index=False)

# --- 5. WORKFLOW ---
menu_options = {
    "BOMTEAM": ["Data Entry", "Audit Logs"],
    "NONBOMTEAM": ["Data Entry", "Audit Logs"],
    "HOD": ["BOM Team Requests", "Audit Logs"],
    "GM": ["BOM Team Requests", "Audit Logs"]
}
menu = st.sidebar.radio("Navigate", menu_options[st.session_state.user])
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

if menu == "Data Entry":
    st.header("BOM Price Approval Form")
    with st.form("bom_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            proj = st.text_input("Project")
            part = st.text_input("Part Number")
            desc = st.text_area("Description")
        with c2:
            bom = st.number_input("BOM Qty", min_value=1)
            uom = st.selectbox("UOM", ["Nos", "Mtrs", "Sets", "Kgs"])
            supp = st.text_input("Supplier")
            price = st.number_input("Unit Price", min_value=0.0)
        rem = st.text_input("Remarks")
        
        if st.form_submit_button("Submit & Send Email"):
            req_id = f"REQ-{datetime.now().strftime('%y%m%d%H%M')}"
            data_to_save = {
                "Request ID": req_id, "Project": proj, "Part Number": part, "Description": desc,
                "BOM": bom, "UOM": uom, "Supplier": supp, "Price": price, "Remarks": rem,
                "HOD Approval": "Pending", "HOD Comments": "-", "GM Approval": "Pending",
                "GM Comments": "-", "Status": "Pending HOD", "Timestamp": datetime.now(),
                "Raised By": st.session_state.user
            }
            df = get_data()
            df = pd.concat([df, pd.DataFrame([data_to_save])], ignore_index=True)
            save_data(df)
            
            # TRIGGER THE EMAIL WITH TABLE
            send_approval_email(MAIL_IDS["HOD"], "", data_to_save)
            st.success(f"Submitted! Email sent to HOD with ID: {req_id}")

elif menu == "BOM Team Requests":
    st.header(f"Approval Dashboard - {st.session_state.user}")
    df = get_data()
    status_filter = "Pending HOD" if st.session_state.user == "HOD" else "Pending GM"
    pending = df[df["Status"] == status_filter]
    
    for i, row in pending.iterrows():
        with st.expander(f"Review Request: {row['Request ID']}"):
            st.table(pd.DataFrame([row]).T)
            dec = st.selectbox("Action", ["Pending", "Approved", "Rejected"], key=f"d{i}")
            comm = st.text_input("Comments", key=f"c{i}")
            if st.button("Confirm Decision", key=f"b{i}"):
                df.at[i, f"{st.session_state.user} Approval"] = dec
                df.at[i, f"{st.session_state.user} Comments"] = comm
                if dec == "Approved":
                    df.at[i, "Status"] = "Pending GM" if st.session_state.user == "HOD" else "Approved Successfully"
                else:
                    df.at[i, "Status"] = f"Rejected by {st.session_state.user}"
                save_data(df)
                st.rerun()

elif menu == "Audit Logs":
    st.dataframe(get_data())
