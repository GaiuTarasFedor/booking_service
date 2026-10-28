from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from account.constants import ClientStatusChoices
from account.models import Barber, Client, User
from booking_manager.models import Barbershop


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - клиент/барбер."""

    help = "Генерация тестовых данных для приложения booking_manager - клиент/барбер."

    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        fake.seed_instance(2026)

        with transaction.atomic():
            users = User.objects.filter(email__startswith="gen_user").order_by("id")[:95]
            qs_barber = users[:15]
            qs_client = users[15:95]
            list_barbershops = list(Barbershop.objects.all())
            list_status = list(ClientStatusChoices)
            count_created = 0
            for user in qs_barber:
                _, created = Barber.objects.get_or_create(
                    user=user,
                    defaults={
                        "experience_year": fake.pyint(min_value=0, max_value=20),
                        "barbershop": fake.random_element(elements=list_barbershops),
                    },
                )
                if created:
                    count_created += 1
            for user in qs_client:
                _, created = Client.objects.get_or_create(
                    user=user,
                    defaults={
                        "status": fake.random_element(elements=list_status),
                        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70),
                    },
                )
                if created:
                    count_created += 1
            if count_created == 0:
                self.stdout.write(
                    "Клиенты и барберы уже существуют в базе данных, новые не создавались."
                )
            else:
                self.stdout.write(f"Создано {count_created} клиентов и барберов.")
            self.stdout.write(
                f"В базе данных находится {Client.objects.count()} клиентов "
                f"и {Barber.objects.count()} барберов."
            )
