import streamlit as st
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. CONFIGURATION & EMAILS ---
st.set_page_config(page_title="Resolute Approval System", layout="wide")

# Email Configuration
SENDER_EMAIL = "jampina.balanaresh@gmail.com" # Your Gmail
EMAIL_PASS = "YOUR_APP_PASSWORD_HERE"        # Replace with your 16-digit App Password

MAIL_IDS = {
    "BOMTEAM": "jampina.balanaresh@gmail.com",
    "HOD": "Balanareshbalu@gmail.com",
    "GM": "purchase@resoluteelectronics.com"
}

WEB_LINK = "https://your-app-link.streamlit.app" # Replace with your actual URL
DB_FILE = "resolute_db.csv"

# User Passwords
USERS = {
    "BOMTEAM": "BOM123",
    "NONBOMTEAM": "NONBOM123",
    "HOD": "HOD789",
    "GM": "GM123"
}

# --- 2. EMAIL ENGINE ---
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
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

# Session State
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user' not in st.session_state: st.session_state.user = None

# --- 3. CUSTOM CSS FOR SIDE-BY-SIDE LOGIN ---
st.markdown("""
    <style>
    .login-container {
        background-color: #f0f2f6;
        padding: 30px;
        border-radius: 10px;
        border-right: 5px solid #004b93;
    }
    .main-title {
        color: #004b93;
        font-family: 'Arial';
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN PAGE (LEFT SIDE DESIGN) ---
if not st.session_state.auth:
    col1, col2 = st.columns([1, 2]) # 1 part left (Login), 2 parts right (Visuals)
    
    with col1:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="main-title">RESOLUTE LOGIN</h2>', unsafe_allow_html=True)
        u_sel = st.selectbox("Select Role", list(USERS.keys()))
        p_sel = st.text_input("Password", type="password")
        if st.button("SIGN IN", use_container_width=True):
            if p_sel == USERS[u_sel]:
                st.session_state.auth = True
                st.session_state.user = u_sel
                st.rerun()
            else:
                st.error("Incorrect Password")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.image("https://img.freelancer.com/flux/8/1/81442490-674b-449e-8c33-a3bc531d0446.jpg") # Industrial Visual
        st.markdown("### Price Approval Management System")
        st.write("Streamlined Procurement & SMT Reel Management Workflow.")
    st.stop()

# --- 5. DATA HELPERS ---
def get_data(): return pd.read_csv(DB_FILE)
def save_data(df): df.to_csv(DB_FILE, index=False)

# Sidebar Logic
st.sidebar.title(f"👤 {st.session_state.user}")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 6. WORKFLOW LOGIC ---
menu_options = {
    "BOMTEAM": ["Data Entry", "Status Board"],
    "NONBOMTEAM": ["Data Entry", "Status Board"],
    "HOD": ["BOM Team Requests", "Dashboard", "Audit Logs"],
    "GM": ["BOM Team Requests", "Dashboard", "Audit Logs"]
}
menu = st.sidebar.radio("Navigate", menu_options[st.session_state.user])

# A. DATA ENTRY (BOM/NONBOM)
if menu == "Data Entry":
    st.header("Price Approval Request Form")
    with st.form("entry_form"):
        c1, c2 = st.columns(2)
        with c1:
            proj = st.text_input("Project Name")
            part = st.text_input("Part Number")
            desc = st.text_area("Description")
        with c2:
            bom = st.number_input("BOM Qty", min_value=1)
            uom = st.selectbox("UOM", ["Nos", "Mtrs", "Sets", "Kgs"])
            supp = st.text_input("Supplier")
            price = st.number_input("Unit Price", min_value=0.0)
        rem = st.text_input("Remarks")
        
        if st.form_submit_button("Submit to HOD"):
            req_id = f"REQ-{datetime.now().strftime('%y%m%d%H%M')}"
            new_row = {
                "Request ID": req_id, "Project": proj, "Part Number": part, "Description": desc,
                "BOM": bom, "UOM": uom, "Supplier": supp, "Price": price, "Remarks": rem,
                "HOD Approval": "Pending", "HOD Comments": "-", "GM Approval": "Pending",
                "GM Comments": "-", "Status": "Pending HOD", "Timestamp": datetime.now(),
                "Raised By": st.session_state.user
            }
            df = get_data()
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            
            # EMAIL TO HOD
            mail_body = f"""<h3>Price Approval Request Received: {req_id}</h3>
            <p>New request raised by {st.session_state.user}.<br>Project: {proj}<br>Price: {price}</p>
            <a href='{WEB_LINK}'>Click here to login and approve</a>"""
            send_email(MAIL_IDS["HOD"], f"Price approval request received - {req_id}", mail_body)
            st.success(f"Request {req_id} Sent to HOD!")

# B. HOD APPROVAL
elif menu == "BOM Team Requests" and st.session_state.user == "HOD":
    st.header("HOD Approval Panel")
    df = get_data()
    pending = df[df["Status"] == "Pending HOD"]
    for i, row in pending.iterrows():
        with st.expander(f"Review {row['Request ID']}"):
            st.write(row)
            dec = st.selectbox("Action", ["Pending", "Approved", "Rejected"], key=f"h{i}")
            comm = st.text_input("HOD Comments", key=f"hc{i}")
            if st.button("Submit Decision", key=f"hb{i}"):
                df.at[i, "HOD Approval"] = dec
                df.at[i, "HOD Comments"] = comm
                if dec == "Approved":
                    df.at[i, "Status"] = "Pending GM"
                    mail_gm = f"<h3>HOD Approved: {row['Request ID']}</h3><p>HOD Remarks: {comm}</p><a href='{WEB_LINK}'>Login to Approve</a>"
                    send_email(MAIL_IDS["GM"], f"Price approval request received - {row['Request ID']}", mail_gm)
                else:
                    df.at[i, "Status"] = f"Rejected by HOD ({comm})"
                save_data(df)
                st.rerun()

# C. GM APPROVAL
elif menu == "BOM Team Requests" and st.session_state.user == "GM":
    st.header("GM Final Approval")
    df = get_data()
    pending = df[df["Status"] == "Pending GM"]
    for i, row in pending.iterrows():
        with st.expander(f"Final Review {row['Request ID']}"):
            st.info(f"HOD Comments: {row['HOD Comments']}")
            st.write(row)
            dec = st.selectbox("Action", ["Pending", "Approved", "Rejected"], key=f"g{i}")
            comm = st.text_input("GM Comments", key=f"gc{i}")
            if st.button("Final Approval", key=f"gb{i}"):
                df.at[i, "GM Approval"] = dec
                df.at[i, "GM Comments"] = comm
                if dec == "Approved":
                    df.at[i, "Status"] = "Approved Successfully"
                    final_mail = f"<h3>SUCCESS: Price Approval Done</h3><p>Part {row['Part Number']} has been fully approved.</p>"
                    send_email(MAIL_IDS["BOMTEAM"], "Price Approval Success", final_mail)
                    send_email(MAIL_IDS["HOD"], "Price Approval Success", final_mail)
                else:
                    df.at[i, "Status"] = f"Rejected by GM ({comm})"
                save_data(df)
                st.rerun()

# D. AUDIT LOGS
elif menu in ["Audit Logs", "Dashboard", "Status Board"]:
    st.header("System Audit Logs")
    st.dataframe(get_data())
