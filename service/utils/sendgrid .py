import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


class SendGridEmailSender:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SENDGRID_API_KEY")
        if not self.api_key:
            raise ValueError("SendGrid API key must be provided")

    def send_email(self, subject, content, from_email, to_emails):

        if isinstance(to_emails, str):
            to_emails = [to_emails]

        message = Mail(
            from_email=Email(from_email),
            to_emails=[To(email) for email in to_emails],
            subject=subject,
            plain_text_content=Content("text/plain", content),
        )

        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            return response.status_code, response.body, response.headers
        except Exception as e:
            print(f"Error sending email: {e}")
            return None

# sender = SendGridEmailSender(api_key="your_sendgrid_api_key_here")
# status, body, headers = sender.send_email(
#     subject="Welcome!",
#     content="Hello from SendGrid and Django.",
#     from_email="you@yourdomain.com",
#     to_emails=["recipient@example.com"],
# )

# print(f"SendGrid response status: {status}")