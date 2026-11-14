from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from booking_manager.models import Product


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - продукты."""

    help = "Генерация тестовых данных для приложения booking_manager - продукты."

    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        fake.seed_instance(2026)

        with transaction.atomic():
            count_created = 0
            for i in range(1, 51):
                _, created = Product.objects.update_or_create(
                    name=f"Товар gen {i:02d}",
                    defaults={
                        "price": fake.pydecimal(
                            left_digits=2, right_digits=2, min_value=2, positive=True
                        ),
                        "amount": fake.pyint(min_value=1, max_value=20),
                        "description": fake.text(max_nb_chars=30),
                    },
                )
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Продукты уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} продуктов.")
        self.stdout.write(f"В базе данных находится {Product.objects.count()} продуктов.")
