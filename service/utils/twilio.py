# service/utils/twilio_api.py
import os
from twilio.rest import Client


class TwilioAPI:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_phone = os.getenv("TWILIO_PHONE_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, to_phone: str, message: str) -> dict:

        message = self.client.messages.create(
            body=message, from_=self.from_phone, to=to_phone
        )
        return {
            "sid": message.sid,
            "status": message.status,
            "to": message.to,
            "from": message.from_,
            "date_created": str(message.date_created),
        }


# def send_template_sms(template, recipient_phone):
#     if template.channel == "sms":
#         twilio_api = TwilioAPI()
#         return twilio_api.send_sms(recipient_phone, template.content)
#     else:
#         raise ValueError("Template channel is not SMS")