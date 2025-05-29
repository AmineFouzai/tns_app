from django.db import models
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from datetime import datetime

from service.models.recipient import Recipient
from service.models.template import Template
from service.tasks import process_campaign

# from service.models.merchant import Merchant
# from service.models.recipient import Recipient
# from service.models.template import Template


class Campaign(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("scheduled", "Scheduled"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("failed", "Failed"),
    ]

    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("push", "Push"),
        ("whatsapp", "WhatsApp"),
    ]

    # merchant = models.ForeignKey(
    #     Merchant, on_delete=models.CASCADE, related_name="campaigns"
    # )
    name = models.CharField(max_length=255)
    channel = models.CharField(max_length=50, choices=CHANNEL_CHOICES)
    templates = models.ManyToManyField(
        Template, related_name="campaigns"
    )  # A/B testing
    recipients = models.ManyToManyField(Recipient)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    scheduled_time = models.DateTimeField(null=True, blank=True)
    idempotency_key = models.CharField(
        max_length=64, blank=True, null=True, unique=True 
    )

    # Segmentation rule in JSON format (e.g., {"last_login_days_gt": 30})
    rule = models.JSONField(
        blank=True, null=True, help_text="Optional audience filter rules"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    beat_task_name = models.CharField(
        max_length=255, null=True, blank=True
    )  # to track Celery Beat task name

    def schedule_task(self):
        if not self.scheduled_time:
            return

        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=str(self.scheduled_time.minute),
            hour=str(self.scheduled_time.hour),
            day_of_month=str(self.scheduled_time.day),
            month_of_year=str(self.scheduled_time.month),
        )

        task_name = f"campaign-{self.id}-schedule"

        task = PeriodicTask.objects.create(
            crontab=schedule,
            name=task_name,
            task="service.process_campaign.process_campaign",  # use your app.task path
            args=json.dumps([self.id]),
            one_off=True,
        )

        self.beat_task_name = task_name
        self.save()

    def cancel_scheduled_task(self):
        if self.beat_task_name:
            PeriodicTask.objects.filter(name=self.beat_task_name).delete()
            self.beat_task_name = None
            self.save()

    def trigger_immediate(self):

        process_campaign.delay(self.id)

    def __str__(self):
        return f"{self.name} ({self.channel})"
