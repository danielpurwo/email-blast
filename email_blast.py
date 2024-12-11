import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Configuration
csv_file = "leads.csv"  # Your CSV file name
pdf_file = "attachment.pdf"  # PDF file to attach
email_sender = "your_email@gmail.com"
email_password = "your_password"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Read the CSV file
leads = pd.read_csv(csv_file)

# Email setup
def send_email(recipient_email, subject, body, attachment=None):
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Email body
    msg.attach(MIMEText(body, "plain"))

    # Attach PDF if provided
    if attachment:
        with open(attachment, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment)}",
        )
        msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_email, msg.as_string())
            print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")

# Send emails to all leads
for _, row in leads.iterrows():
    recipient_name = row["name"]
    recipient_email = row["email"]
    recipient_type = row["type"]

    # Customize the email content
    subject = f"Hello {recipient_name}!"
    body = f"""
    Hi {recipient_name},

    We have exciting updates for the {recipient_type} industry. 
    Please find the attached document for more details.

    Best regards,
    Your Company
    """

    # Send the email with the PDF attachment
    send_email(recipient_email, subject, body, pdf_file)
