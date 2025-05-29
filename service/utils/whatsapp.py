from twilio.rest import Client
import os


class WhatsAppSender:
    def __init__(self, account_sid=None, auth_token=None, from_whatsapp_number=None):
        self.account_sid = account_sid or os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = auth_token or os.getenv("TWILIO_AUTH_TOKEN")
        self.from_whatsapp_number = from_whatsapp_number or os.getenv(
            "TWILIO_WHATSAPP_FROM"
        )

        if not all([self.account_sid, self.auth_token, self.from_whatsapp_number]):
            raise ValueError(
                "Twilio credentials and WhatsApp sender number must be provided"
            )

        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, to_whatsapp_number, body):

        try:
            message = self.client.messages.create(
                body=body, from_=self.from_whatsapp_number, to=to_whatsapp_number
            )
            return message.sid
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")
            return None


# whatsapp = WhatsAppSender(
#     account_sid='your_twilio_sid',
#     auth_token='your_twilio_auth_token',
#     from_whatsapp_number='whatsapp:+14155238886'  # Twilio Sandbox number or your registered WhatsApp number
# )

# message_sid = whatsapp.send_message(
#     to_whatsapp_number='whatsapp:+1234567890',
#     body='Hello from Django via WhatsApp!'
# )

# print(f"Message SID: {message_sid}")