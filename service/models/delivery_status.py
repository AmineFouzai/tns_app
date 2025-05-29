# from django.db import models

# from service.models.campaign import Campaign
# from service.models.recipient import Recipient
# from service.models.template import Template


# class DeliveryStatus(models.Model):
#     STATUS_CHOICES = [
#         ("queued", "Queued"),
#         ("sent", "Sent"),
#         ("delivered", "Delivered"),
#         ("failed", "Failed"),
#     ]

#     campaign = models.ForeignKey(
#         Campaign, on_delete=models.CASCADE, related_name="deliveries"
#     )
#     recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
#     template_used = models.ForeignKey(
#         Template, null=True, blank=True, on_delete=models.SET_NULL
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")
#     provider_response = models.TextField(blank=True, null=True)
#     sent_at = models.DateTimeField(blank=True, null=True)

#     # Optional hook to push via WebSocket
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("campaign", "recipient")

#     def __str__(self):
#         return f"{self.recipient} - {self.status}"
