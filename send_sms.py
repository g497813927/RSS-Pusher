"""
Function for sending email
using Twilio's Python Library
https://www.twilio.com/docs/sms/quickstart/python
"""
from twilio.rest import Client
import os


def send_sms(to_phone, from_phone, body):
    try:
        client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
        message = client.messages.create(
            to=to_phone,
            from_=from_phone,
            body=body)
        return {
            "status_code": message.status,
            "sid": message.sid
        }
    except Exception as e:
        return {
            "error": str(e)
        }
