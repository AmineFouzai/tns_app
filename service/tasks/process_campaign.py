from celery import shared_task


@shared_task(name="Process Campaign")
def process_campaign(campaign_id):
    from service.models import Campaign

    try:
        campaign = Campaign.objects.get(id=campaign_id)
    except Campaign.DoesNotExist:
        return f"Campaign {campaign_id} not found"

    # Update status
    campaign.status = "processing"
    campaign.save()

    # Simulate sending logic here
    # e.g., notify_via_email(template, recipient)

    campaign.status = "completed"
    campaign.save()

    return f"Processed Campaign {campaign_id}"


# from celery import shared_task
# from django.conf import settings


# @shared_task
# def process_campaign(campaign_id):
#     from service.models import Campaign
#     from service.utils.twilio import TwilioAPI
#     from service.utils.sendgrid import SendGridEmailSender
#     from service.utils.whatsapp import WhatsAppSender

#     try:
#         campaign = Campaign.objects.get(id=campaign_id)
#     except Campaign.DoesNotExist:
#         return f"Campaign {campaign_id} not found"

#     campaign.status = "processing"
#     campaign.save()

#     twilio_api = None
#     email_sender = None
#     whatsapp_sender = None

#     if campaign.channel == "sms":
#         twilio_api = TwilioAPI()
#     elif campaign.channel == "email":
#         email_sender = SendGridEmailSender()
#     elif campaign.channel == "whatsapp":
#         whatsapp_sender = WhatsAppSender()

#     errors = []

#     for recipient in campaign.recipients.all():
#         for template in campaign.templates.all():
#             try:
#                 if campaign.channel == "email":
#                     subject = (
#                         template.subject
#                         if hasattr(template, "subject")
#                         else campaign.name
#                     )
#                     content = template.content
#                     from_email = settings.DEFAULT_FROM_EMAIL
#                     to_email = recipient.email
#                     response = email_sender.send_email(
#                         subject, content, from_email, to_email
#                     )
#                     if response is None:
#                         errors.append(f"Email to {to_email} failed")

#                 elif campaign.channel == "sms":
#                     message_info = twilio_api.send_sms(
#                         recipient.phone_number, template.content
#                     )
#                     if not message_info.get("sid"):
#                         errors.append(f"SMS to {recipient.phone_number} failed")

#                 elif campaign.channel == "whatsapp":
#                     to_whatsapp = f"whatsapp:{recipient.phone_number}"
#                     sid = whatsapp_sender.send_message(to_whatsapp, template.content)
#                     if sid is None:
#                         errors.append(f"WhatsApp to {to_whatsapp} failed")

#                 else:
#                     errors.append(f"Unsupported channel: {campaign.channel}")

#             except Exception as e:
#                 errors.append(
#                     f"Error sending to {recipient.id} with template {template.id}: {e}"
#                 )

#     if len(errors) > 0:
#         campaign.status = "failed"
#         campaign.save()
#         print(f"Processed with errors: {errors}")
#         return f"Processed with errors: {errors}"
#     else:
#         campaign.status = "completed"
#         campaign.save()
#         print( f"Processed Campaign {campaign_id} successfully")
#         return f"Processed Campaign {campaign_id} successfully"
