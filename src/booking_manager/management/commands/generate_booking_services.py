from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from booking_manager.models import BookingService

BOOKINGSERVICE = [
    {
        "category": "haircut",
        "name": "Классика",
        "description": "стрижка машинкой и ножницами, укладка",
        "price": Decimal("50.00"),
        "duration_minutes": 40,
        "is_active": True,
    },
    {
        "category": "haircut",
        "name": "Фейд",
        "description": "плавный переход от коротких волос к длинным",
        "price": Decimal("60.00"),
        "duration_minutes": 45,
        "is_active": True,
    },
    {
        "category": "haircut",
        "name": "Тейпер",
        "description": "стрижка машинкой с лёгким переходом, окантовка",
        "price": Decimal("55.00"),
        "duration_minutes": 40,
        "is_active": True,
    },
    {
        "category": "haircut",
        "name": "Полубокс",
        "description": "короткая стрижка с пробором, укладка",
        "price": Decimal("50.00"),
        "duration_minutes": 35,
        "is_active": True,
    },
    {
        "category": "haircut",
        "name": "Площадка",
        "description": "стрижка с ровной площадкой сверху",
        "price": Decimal("45.00"),
        "duration_minutes": 30,
        "is_active": True,
    },
    {
        "category": "haircut",
        "name": "Канадка",
        "description": "стрижка с удлинённой чёлкой и короткими висками",
        "price": Decimal("55.00"),
        "duration_minutes": 40,
        "is_active": True,
    },
    {
        "category": "beard",
        "name": "Окладистая",
        "description": "моделирование бороды, триммер, бритва",
        "price": Decimal("40.00"),
        "duration_minutes": 30,
        "is_active": True,
    },
    {
        "category": "moustache",
        "name": "Подкова",
        "description": "стрижка и укладка усов в форме подковы",
        "price": Decimal("25.00"),
        "duration_minutes": 20,
        "is_active": True,
    },
    {
        "category": "moustache",
        "name": "Английская",
        "description": "тонкая работа с усами, воск, укладка",
        "price": Decimal("30.00"),
        "duration_minutes": 25,
        "is_active": True,
    },
    {
        "category": "shave",
        "name": "Классическое бритьё",
        "description": "опасная бритва, горячее полотенце, лосьон",
        "price": Decimal("70.00"),
        "duration_minutes": 40,
        "is_active": True,
    },
    {
        "category": "shave",
        "name": "Бритьё головы",
        "description": "бритьё головы опасной бритвой или машинкой",
        "price": Decimal("45.00"),
        "duration_minutes": 30,
        "is_active": True,
    },
    {
        "category": "royal",
        "name": "Королевское",
        "description": "стрижка, борода, бритьё, уход, массаж лица",
        "price": Decimal("150.00"),
        "duration_minutes": 90,
        "is_active": True,
    },
    {
        "category": "camouflage",
        "name": "Камуфляж седины",
        "description": "тонирование седых волос, без аммиака",
        "price": Decimal("80.00"),
        "duration_minutes": 50,
        "is_active": True,
    },
    {
        "category": "camouflage",
        "name": "Тонирование",
        "description": "лёгкое тонирование волос или бороды",
        "price": Decimal("65.00"),
        "duration_minutes": 40,
        "is_active": True,
    },
    {
        "category": "kids",
        "name": "Детская стрижка",
        "description": "стрижка для детей до 12 лет, мультики",
        "price": Decimal("35.00"),
        "duration_minutes": 30,
        "is_active": True,
    },
    {
        "category": "kids",
        "name": "Первый раз",
        "description": "первая стрижка малыша, фото на память",
        "price": Decimal("40.00"),
        "duration_minutes": 35,
        "is_active": True,
    },
    {
        "category": "combo",
        "name": "Комбо: стрижка+борода",
        "description": "стрижка головы и моделирование бороды",
        "price": Decimal("100.00"),
        "duration_minutes": 70,
        "is_active": True,
    },
    {
        "category": "combo",
        "name": "Комбо: отец и сын",
        "description": "две стрижки по специальной цене",
        "price": Decimal("90.00"),
        "duration_minutes": 70,
        "is_active": True,
    },
    {
        "category": "combo",
        "name": "Стрижка+усы",
        "description": "стрижка головы и оформление усов",
        "price": Decimal("75.00"),
        "duration_minutes": 55,
        "is_active": True,
    },
    {
        "category": "combo",
        "name": "Борода+усы",
        "description": "полный уход за бородой и усами",
        "price": Decimal("55.00"),
        "duration_minutes": 45,
        "is_active": True,
    },
]


class Command(BaseCommand):
    """Команда для генерации тестовых данных в БД - услуг."""

    help = "Генерация тестовых данных для приложения booking_manager - услуг."

    def handle(self, *args, **options):
        with transaction.atomic():
            count_created = 0
            for data in BOOKINGSERVICE:
                _, created = BookingService.objects.get_or_create(name=data["name"], defaults=data)
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Услуги уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} услуг.")
        self.stdout.write(f"В базе данных находится {BookingService.objects.count()} услуг.")
