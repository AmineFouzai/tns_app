from django.core.management.base import BaseCommand
from service.models.template import Template
from service.models.merchant import Merchant
import random


class Command(BaseCommand):
    help = "Seed the database with sample templates"

    def handle(self, *args, **kwargs):
        merchants = list(Merchant.objects.all())

        if not merchants:
            self.stdout.write(
                self.style.ERROR("No merchants found. Seed merchants first.")
            )
            return

        sample_templates = [
            {
                "name": "Welcome Email A",
                "channel": "email",
                "content": "Hello {{name}}, welcome to our service!",
                "variant": "A",
            },
            {
                "name": "Welcome Email B",
                "channel": "email",
                "content": "Hey {{name}}, glad to have you here!",
                "variant": "B",
            },
            {
                "name": "Promo SMS",
                "channel": "sms",
                "content": "Get 20% off on your next purchase. Use code: SAVE20",
                "variant": None,
            },
            {
                "name": "Push Alert",
                "channel": "push",
                "content": "Don't miss our latest updates!",
                "variant": None,
            },
            {
                "name": "WhatsApp Reminder",
                "channel": "whatsapp",
                "content": "Your appointment is scheduled for tomorrow at 3 PM.",
                "variant": None,
            },
        ]

        for template_data in sample_templates:
            merchant = random.choice(merchants)

            template, created = Template.objects.get_or_create(
                name=template_data["name"],
                defaults={
                    "channel": template_data["channel"],
                    "content": template_data["content"],
                    "variant": template_data["variant"],
                    "merchant": merchant,
                },
            )

            action = "Created" if created else "Skipped (exists)"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{action}: {template.name} (Merchant: {merchant.username})"
                )
            )
