import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time
from dotenv import load_dotenv
load_dotenv()

# Configuration
excel_file = "leads.xlsx"  # Your Excel file name
pdf_file = os.getenv("pdf_file")  # PDF file to attach
email_sender = os.getenv("email_sender")
email_password = os.getenv("email_password")
smtp_server = os.getenv("smtp_server")
smtp_port = os.getenv("smtp_port")
batch_size = 50  # Number of emails to send per batch
delay_between_batches = 10  # Delay in seconds between batches

def read_excel_filtered(excel_file, start_no):
    """
    Reads the Excel file and filters rows based on the start_no parameter.
    """
    leads = pd.read_excel(excel_file)
    filtered_leads = leads[(leads["no"] >= start_no) & (leads["no"] <= end_no)]
    return filtered_leads

def send_email(recipient_email, subject, body, attachment=None):
    """
    Sends an email with an optional attachment.
    """
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

def process_email_blast(excel_file, start_no, pdf_file=None):
    """
    Processes the email blast by filtering rows and sending emails in batches.
    """
    leads = read_excel_filtered(excel_file, start_no)
    print(f"Starting email blast from 'no' {start_no}. Total leads: {len(leads)}")

    for i, row in leads.iterrows():
        recipient_name = row["name"]
        recipient_email = row["email"]

        # Customize the email content
        subject = f"Hello {recipient_name}!"
        body = f"""
        Hi {recipient_name},

        We have exciting updates for your industry. 
        Please find the attached document for more details.

        Best regards,
        Your Company
        """

        # Send the email with the PDF attachment
        send_email(recipient_email, subject, body, pdf_file)

        # Batch processing with delay
        if (i + 1) % batch_size == 0:
            print(f"Processed {i + 1} emails. Waiting for {delay_between_batches} seconds...")
            time.sleep(delay_between_batches)

# Start the process
if __name__ == "__main__":
    start_no = int(input("Enter the starting 'no' parameter: "))
    process_email_blast(excel_file, start_no, pdf_file)