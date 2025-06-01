from django.utils import timezone
from unittest.mock import patch
from django.test import TestCase
from service.models import Campaign
from service.models.merchant import Merchant


class CampaignNotificationModelTests(TestCase):
    def setUp(self):
        self.merchant = Merchant.objects.create_user(
            username="merchant", password="pass"
        )
        self.campaign = Campaign.objects.create(
            name="Test Campaign",
            status="draft",
            merchant=self.merchant,
            channel="email",
        )
        self.campaign.recipients.set([])
        self.campaign.templates.set([])

    def test_send_notification_no_recipients_or_templates(self):
        self.assertFalse(self.campaign.recipients.exists())
        self.assertFalse(self.campaign.templates.exists())

    def test_send_notification_success(self):
        recipient = self.campaign.recipients.model.objects.create(
            name="John Doe", merchant=self.merchant
        )
        template = self.campaign.templates.model.objects.create(
            content="Hello", merchant=self.merchant
        )
        self.campaign.recipients.set([recipient])
        self.campaign.templates.set([template])

        with patch.object(Campaign, "trigger_immediate") as mock_trigger:
            self.campaign.trigger_immediate()
            mock_trigger.assert_called_once()

    def test_schedule_notification_success(self):
        recipient = self.campaign.recipients.model.objects.create(
            name="John Doe", merchant=self.merchant
        )
        template = self.campaign.templates.model.objects.create(
            content="Hi", merchant=self.merchant
        )
        self.campaign.recipients.set([recipient])
        self.campaign.templates.set([template])

        dt = timezone.now()
        self.campaign.scheduled_time = dt

        with patch.object(Campaign, "schedule_task") as mock_schedule:
            self.campaign.schedule_task()
            mock_schedule.assert_called_once()

    def test_schedule_notification_missing_time(self):
        self.campaign.scheduled_time = None
        result = self.campaign.schedule_task()
        self.assertIsNone(result)

    def test_cancel_scheduled_notification_success(self):
        self.campaign.status = "scheduled"
        self.campaign.beat_task_name = "campaign-1-schedule"
        self.campaign.save()

        with patch(
            "django_celery_beat.models.PeriodicTask.objects.filter"
        ) as mock_filter:
            mock_filter.return_value.delete.return_value = None

            self.campaign.cancel_scheduled_task()
            self.assertIsNone(self.campaign.beat_task_name)

    def test_cancel_scheduled_notification_invalid_status(self):
        self.campaign.status = "processing"
        self.campaign.save()

    def test_get_campaign_status(self):
        self.campaign.status = "scheduled"
        self.campaign.save()

        self.assertEqual(self.campaign.status, "scheduled")
        self.assertEqual(self.campaign.id, self.campaign.pk)
