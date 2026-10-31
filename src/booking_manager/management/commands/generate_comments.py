from datetime import UTC, datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from booking_manager.models import Booking, Comment


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - комментарии."""

    help = "Генерация тестовых данных для приложения booking_manager - комментарии."

    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        fake.seed_instance(2026)

        with transaction.atomic():
            list_bookings = list(
                Booking.objects.select_related("barber", "client")
                .filter(name__startswith="Бронь gen", visit_time__lte=datetime.now(UTC))
                .order_by("id")[:200]
            )
            count_created = 0
            for booking in list_bookings:
                _, created = Comment.objects.get_or_create(
                    booking=booking,
                    defaults={
                        "text": fake.text(max_nb_chars=100),
                        "is_published": fake.boolean(chance_of_getting_true=80),
                        "barber": booking.barber,
                        "client": booking.client,
                        "rating": fake.pyint(min_value=0, max_value=5),
                    },
                )
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Комментарии уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} комментариев.")
        self.stdout.write(f"В базе данных находится {Comment.objects.count()} комментариев.")
