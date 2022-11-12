"""
Function for sending email
using SendGrid's Python Library
https://github.com/sendgrid/sendgrid-python
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(from_email, to_email, subject, html_content):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return {
            "status_code": response.status_code,
            "response_body": response.body,
            "headers": response.headers
        }
    except Exception as e:
        return {
            "error": str(e)
        }
