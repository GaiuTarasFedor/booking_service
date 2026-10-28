from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from booking_manager.models import BookingService, Promotion


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - акции."""

    help = "Генерация тестовых данных для приложения booking_manager - акции."

    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        fake.seed_instance(2026)

        with transaction.atomic():
            list_servace = list(BookingService.objects.all())
            count_created = 0
            for i in range(1, 11):
                random_services = fake.random_elements(elements=list_servace, length=3)
                description = fake.text(max_nb_chars=30)
                discount_percent = fake.pyint(min_value=0, max_value=20)
                start_date = fake.date_between(start_date="-1w")
                end_date = start_date + timedelta(days=fake.pyint(min_value=2, max_value=7))
                is_active = True
                promo, created = Promotion.objects.get_or_create(
                    name=f"Акция № {i:02d}",
                    defaults={
                        "description": description,
                        "discount_percent": discount_percent,
                        "start_date": start_date,
                        "end_date": end_date,
                        "is_active": is_active,
                    },
                )
                promo.services.set(random_services)
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Акции уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} акций.")
        self.stdout.write(f"В базе данных находится {Promotion.objects.count()} акций.")
