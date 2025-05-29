from django.db import models
# from service.models.merchant import Merchant


class Template(models.Model):
    # merchant = models.ForeignKey(
    #     Merchant, on_delete=models.CASCADE, related_name="templates"
    # )
    name = models.CharField(max_length=255)
    channel = models.CharField(
        max_length=50,
        choices=[
            ("email", "Email"),
            ("sms", "SMS"),
            ("push", "Push"),
            ("whatsapp", "WhatsApp"),
        ],
    )
    content = models.TextField()
    variant = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        help_text="A/B test variant label (e.g., A, B)",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.channel})"
