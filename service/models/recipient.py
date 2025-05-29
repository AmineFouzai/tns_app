from django.db import models

# from service.models.merchant import Merchant


class Recipient(models.Model):
    # merchant = models.ForeignKey(
    #     Merchant, on_delete=models.CASCADE, related_name="recipients"
    # )
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    device_token = models.CharField(max_length=255, blank=True, null=True)

    # Segmentation Fields
    last_login = models.DateTimeField(blank=True, null=True)
    is_active_user = models.BooleanField(default=True)
    custom_tags = models.JSONField(
        blank=True, null=True, help_text="Optional tag-based segmentation"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email or self.phone or "Recipient"
