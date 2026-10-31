from datetime import UTC
from random import choice

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from account.models import Barber, Client
from booking_manager.models import Booking, BookingService


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - информации о бронированнии."""

    help = "Генерация тестовых данных для приложения booking_manager - информация о бронировании."

    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        fake.seed_instance(2026)

        with transaction.atomic():
            list_clients = list(
                Client.objects.filter(user__email__startswith="gen_user")
                .select_related("user")
                .order_by("id")
            )
            list_barbers = list(
                Barber.objects.filter(user__email__startswith="gen_user")
                .select_related("barbershop", "user")
                .order_by("id")
            )
            list_services = list(BookingService.objects.all())
            count_created = 0
            for i in range(1, 501):
                barber = choice(list_barbers)
                client = choice(list_clients)
                service = choice(list_services)
                _, created = Booking.objects.get_or_create(
                    name=f"Бронь gen {i:04d}",
                    defaults={
                        "visit_time": fake.date_time_between(
                            start_date="-30d", end_date="+30d", tzinfo=UTC
                        ),
                        "is_active": fake.boolean(chance_of_getting_true=80),
                        "booking_service": service,
                        "barber": barber,
                        "client": client,
                        "barbershop": barber.barbershop,
                    },
                )
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Брони уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} записей о бронировании.")
        self.stdout.write(f"В базе данных находится {Booking.objects.count()} записей о брони.")
