from datetime import time

from django.core.management.base import BaseCommand
from django.db import transaction

from booking_manager.models import Barbershop

BARBERSHOPS = [
    {
        "name": "БОРОДАЧ",
        "phone": "84953124567",
        "address": "Москва, ул. Озерная, д. 100",
        "description": "Лучшая стрижка сезона - котелок - только у нас!",
        "opening_time": time(8, 0),
        "closing_time": time(23, 0),
        "is_active": True,
    },
    {
        "name": "ВОЛОСЫ и УСЫ",
        "phone": "84957834154",
        "address": "Москва, ул. Бауманская, д. 7",
        "description": "Усы и борода - украшение лица!",
        "opening_time": time(8, 0),
        "closing_time": time(20, 0),
        "is_active": True,
    },
    {
        "name": "СТАЛЬНАЯ БРИТВА",
        "phone": "84951112233",
        "address": "Москва, ул. Тверская, д. 12",
        "description": "Классические стрижки и королевское бритье опасной бритвой.",
        "opening_time": time(9, 0),
        "closing_time": time(21, 0),
        "is_active": True,
    },
    {
        "name": "ГРАФ И БРИТВА",
        "phone": "84952223344",
        "address": "Москва, пр-т Мира, д. 45",
        "description": "Стрижка под винтаж и уход за бородой в атмосфере старого города.",
        "opening_time": time(10, 0),
        "closing_time": time(22, 0),
        "is_active": True,
    },
    {
        "name": "СЕВЕРНЫЙ ЦИРЮЛЬНИК",
        "phone": "84953334455",
        "address": "Москва, ул. Арбат, д. 21",
        "description": "Современные мужские стрижки, бритье и стайлинг для любого случая.",
        "opening_time": time(7, 30),
        "closing_time": time(22, 30),
        "is_active": True,
    },
]


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - барбешопов."""

    help = "Генерация тестовых данных для приложения booking_manager - барбершопы."

    def handle(self, *args, **options):
        with transaction.atomic():
            count_created = 0
            for data in BARBERSHOPS:
                # при необходимости можно заменить метод создания на update_or_create,
                # чтобы обновлять значения
                _, created = Barbershop.objects.get_or_create(name=data["name"], defaults=data)
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Барбершопы уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} барбершопов.")
        self.stdout.write(f"В базе данных находится {Barbershop.objects.count()} барбершопов.")
