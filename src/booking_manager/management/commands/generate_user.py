from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from account.models import User


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - пользователи."""

    help = "Генерация тестовых данных для приложения booking_manager - пользователи."

    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        fake.seed_instance(2026)

        with transaction.atomic():
            password = "password123"
            count_created = 0
            for i in range(1, 101):
                email = f"gen_user{i:03d}@example.com"
                other_fields = {
                    "username": f"gen_user{i:03d}.@example.com",
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "phone": fake.phone_number(),
                    "is_staff": False,
                }
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults=other_fields,
                )
                if password and created:
                    user.set_password(password)
                    user.save(update_fields=["password"])
                if created:
                    count_created += 1
        if count_created == 0:
            self.stdout.write("Пользователи уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} пользователей.")
        self.stdout.write(f"В базе данных находится {User.objects.count()} пользователей.")
