import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time

# Configuration
csv_file = "compile for blast.csv"  # Your CSV file name
pdf_file = "Company Profile - GA - N.pdf"  # PDF file to attach
email_sender = "your_email@gmail.com"
email_password = "your_password"
smtp_server = "smtp.gmail.com"
smtp_port = 587
batch_size = 50  # Number of emails to send per batch
delay_between_batches = 10  # Delay in seconds between batches

def read_csv_filtered(csv_file, start_no):
    """
    Reads the CSV file and filters rows based on the start_no parameter.
    """
    leads = pd.read_csv(csv_file)
    filtered_leads = leads[leads["no"] >= start_no]
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

def process_email_blast(csv_file, start_no, pdf_file=None):
    """
    Processes the email blast by filtering rows and sending emails in batches.
    """
    leads = read_csv_filtered(csv_file, start_no)
    print(f"Starting email blast from 'no' {start_no}. Total leads: {len(leads)}")

    for i, row in leads.iterrows():
        recipient_name = row["name"]
        recipient_email = row["email"]

        # Customize the email content
        subject = f"Hello {recipient_name}!"
        body = f"""
        Kepada Yth. Bapak/Ibu,
        Dengan hormat,

        
        Perkenalkan kami Analyset, merupakan perusahaan Teknologi Informasi yang berfokus pada pengembangan Data Analytic, Machine Learning, Computer Vision dan AI. Analyset sudah membantu dan telah dipercaya oleh banyak Perusahaan di Indonesia sebagai penyedia layanan dan konsultan IT. 
        
        Bersama dengan email ini, kami bermaksud mengajukan kerjasama Pengembangan Produk IT kepada perusahaan Anda. Anda bisa lihat Proposal lengkap tentang layanan Analyset dengan melihat tautan company profile kami #BetterDecision
        
        Best regards,
        Analyset
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
    process_email_blast(csv_file, start_no, pdf_file)
