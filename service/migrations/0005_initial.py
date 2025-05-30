# Generated by Django 5.2.1 on 2025-05-26 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("service", "0004_delete_merchant"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "channel",
                    models.CharField(
                        choices=[
                            ("email", "Email"),
                            ("sms", "SMS"),
                            ("push", "Push"),
                            ("whatsapp", "WhatsApp"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("scheduled", "Scheduled"),
                            ("processing", "Processing"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("scheduled_time", models.DateTimeField(blank=True, null=True)),
                (
                    "idempotency_key",
                    models.CharField(blank=True, max_length=64, null=True, unique=True),
                ),
                (
                    "rule",
                    models.JSONField(
                        blank=True,
                        help_text="Optional audience filter rules",
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "beat_task_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
    ]
