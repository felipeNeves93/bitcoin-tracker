import os
import unittest
from email.mime.text import MIMEText

from app.integration.email_sender_integration import EmailSenderIntegration


class TestEmailSenderIntegration(unittest.TestCase):

    def setUp(self):
        os.environ["SENDER_EMAIL"] = "test_sender@example.com"
        os.environ["SENDER_EMAIL_PASSWORD"] = "test_password"
        os.environ["SMTP_ADDRESS"] = "smtp.test.com"
        os.environ["SMTP_PORT"] = "587"

        self.email_sender = EmailSenderIntegration()

    def test_create_email_message(self):
        message = "Test content"
        subject = "Test Subject"
        destination = "test_recipient@example.com"

        email_message = self.email_sender._create_email_message(message, subject, destination)

        # Assert
        self.assertIsInstance(email_message, MIMEText)
        self.assertEqual(email_message["Subject"], subject)
        self.assertEqual(email_message["From"], "test_sender@example.com")
        self.assertEqual(email_message["To"], destination)
        self.assertEqual(email_message.get_payload(), message)
