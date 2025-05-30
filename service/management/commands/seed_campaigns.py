from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from service.models.campaign import Campaign
from service.models.template import Template
from service.models.recipient import Recipient
import random
import string


class Command(BaseCommand):
    help = "Seed the database with sample campaigns"

    def handle(self, *args, **kwargs):
        templates = list(Template.objects.all())
        recipients = list(Recipient.objects.all())

        if not templates or not recipients:
            self.stdout.write(
                self.style.ERROR("Templates or Recipients not found. Seed them first.")
            )
            return

        def generate_idempotency_key():
            return "".join(random.choices(string.ascii_letters + string.digits, k=32))

        sample_campaigns = [
            {
                "name": "Welcome Campaign",
                "channel": "email",
                "template_variants": ["A", "B"],
                "rule": {"new_user": True},
                "scheduled_time": now() + timedelta(minutes=10),
            },
            {
                "name": "Promo Push",
                "channel": "push",
                "template_variants": [None],
                "rule": {"active_last_7_days": True},
                "scheduled_time": None,
            },
            {
                "name": "WhatsApp Reminder",
                "channel": "whatsapp",
                "template_variants": [None],
                "rule": {"pending_action": True},
                "scheduled_time": now() + timedelta(minutes=30),
            },
        ]

        for data in sample_campaigns:
            campaign, created = Campaign.objects.get_or_create(
                name=data["name"],
                defaults={
                    "channel": data["channel"],
                    "status": "pending",
                    "scheduled_time": data["scheduled_time"],
                    "rule": data["rule"],
                    "idempotency_key": generate_idempotency_key(),
                },
            )

            # Link recipients (first 5)
            campaign.recipients.set(recipients[:5])

            # Link templates matching channel and variant
            matched_templates = [
                t
                for t in templates
                if t.channel == data["channel"]
                and t.variant in data["template_variants"]
            ]
            campaign.templates.set(matched_templates)

            # Schedule task if scheduled_time is present
            if data["scheduled_time"]:
                campaign.schedule_task()

            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'} campaign: {campaign.name}"
                )
            )
