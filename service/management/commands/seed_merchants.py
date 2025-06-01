from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from service.models.merchant import Merchant


class Command(BaseCommand):
    help = "Seed the database with Merchant users"

    def handle(self, *args, **options):
        Merchant = get_user_model()

        group_name = "Merchants"
        merchant_group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created group '{group_name}'"))

        for i in range(5):
            username = f"merchant{i}"
            email = f"merchant{i}@example.com"
            if not Merchant.objects.filter(username=username).exists():
                user = Merchant.objects.create_user(
                    username=username, email=email, password="password123"
                )
                user.groups.add(merchant_group)
                self.stdout.write(
                    self.style.SUCCESS(f"Created merchant user '{username}'")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"User '{username}' already exists")
                )
