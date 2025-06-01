from django.core.management.base import BaseCommand
from service.models.recipient import Recipient
from service.models.merchant import Merchant  # Adjust to your app structure
from faker import Faker
import random
from django.utils import timezone

fake = Faker()


class Command(BaseCommand):


    def handle(self, *args, **options):
        count = 5
        created = 0

        merchants = list(Merchant.objects.all())

        if not merchants:
            self.stdout.write(
                self.style.ERROR("No merchants found. Seed merchants first.")
            )
            return

        for _ in range(count):
            merchant = random.choice(merchants)

            recipient = Recipient.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number(),
                device_token=fake.uuid4(),
                last_login=timezone.make_aware(
                    fake.date_time_between(start_date="-30d", end_date="now")
                ),
                is_active_user=random.choice([True, False]),
                custom_tags={"interests": fake.words(nb=random.randint(1, 3))},
                merchant=merchant,  # Assumes Recipient has a FK to User/Merchant
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created} recipients.")
        )
