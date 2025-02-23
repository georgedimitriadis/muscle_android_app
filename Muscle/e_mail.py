
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


class EMail:
    def __init__(self, attachment):

        self.sender_email = 'george.dimitriadis.android@gmail.com'
        self.password = 'uqcz fxpu gxvm ldit'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = '587'
        self.receiver_email = self.sender_email

        self.subject = f'Muscle schedule completed on {str(datetime.now().date())}'
        self.body = ''

    def send_email(self):

        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = self.subject

        # Attach the email body to the message
        message.attach(MIMEText(self.body, "plain"))

        # Attach a file
        filename = "./assets/data/schedule.json"  # Replace with your file path
        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )
                message.attach(part)
        except FileNotFoundError:
            print(f"File {filename} not found. No attachment will be sent.")

        # Establish a connection to the SMTP server and send the email
        try:
            # Connect to the SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.password)  # Log in to the SMTP server
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())  # Send the email
            print("Email sent successfully")
        except Exception as e:
            print(f"Error: {e}")

