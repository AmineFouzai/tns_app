from django.core.management.base import BaseCommand
from service.models.recipient import Recipient
from faker import Faker
import random
from django.utils import timezone

fake = Faker()


class Command(BaseCommand):
    help = "Seed the Recipient table with dummy data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of recipients to create"
        )

    def handle(self, *args, **options):
        count = options["count"]
        created = 0

        for _ in range(count):
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
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created} recipients.")
        )
