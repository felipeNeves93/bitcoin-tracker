import os
import smtplib
from email.mime.text import MIMEText


class EmailSenderIntegration:

    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_email_password = os.getenv("SENDER_EMAIL_PASSWORD")
        self.smtp_address = os.getenv("SMTP_ADDRESS")
        self.smtp_port = os.getenv("SMTP_PORT")

    def send_email(self, message: str, subject: str, destination: str):
        try:
            email_message = self._create_email_message(message, subject, destination)
            with smtplib.SMTP(self.smtp_address, int(self.smtp_port)) as server:
                print("Log in into smtp server")
                server.starttls()
                server.login(self.sender_email, self.sender_email_password)
                print("Log in successfully!")

                server.send_message(email_message)
                print("Message sent successfully!")
        except Exception as e:
            print(f"An error happened when sending email {e}")

    def _create_email_message(self, message: str, subject: str, destination: str) -> MIMEText:
        email_message = MIMEText(message)
        email_message["Subject"] = subject
        email_message["From"] = self.sender_email
        email_message["To"] = destination

        return email_message
