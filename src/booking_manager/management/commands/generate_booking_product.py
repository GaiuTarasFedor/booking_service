from decimal import Decimal
from random import choice

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from booking_manager.models import Booking, Product, ProductBooking


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - связь бронирование продуктов."""

    help = """
    Генерация тестовых данных для приложения booking_manager - связь 
    бронирование продуктов.
    """

    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        fake.seed_instance(2026)

        with transaction.atomic():
            list_bookings = list(
                Booking.objects.filter(name__startswith="Бронь gen").order_by("id")[100:300]
            )
            list_product = list(Product.objects.all())
            count_created = 0
            for booking in list_bookings:
                product = choice(list_product)
                quantity = fake.pyint(min_value=1, max_value=5)
                _, created = ProductBooking.objects.get_or_create(
                    booking=booking,
                    defaults={
                        "product": product,
                        "total_price": (product.price or Decimal(0)) * quantity,
                        "quantity": quantity,
                    },
                )
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write(
                "Связи 'бронирование - продукт' уже существуют в базе данных, новые не создавались."
            )
        else:
            self.stdout.write(f"Создано {count_created} связей 'бронирование - продукт'.")
        self.stdout.write(
            f"В базе данных находится {ProductBooking.objects.count()} "
            f"связей 'бронирование - продукт'."
        )
