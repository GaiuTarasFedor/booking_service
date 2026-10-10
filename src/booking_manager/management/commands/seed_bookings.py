from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal

from booking_manager.models import Booking


BOOKINGS = [
    {
        "name": "Мужская стрижка",
        "price": Decimal("99"),
        "category": "haircut",
        "is_active": True,
        "visit_time": timezone.make_aware(datetime(2026, 10, 15, 17, 30)),
    },
    {
        "name": "СТРИЖКА детская",
        "price": Decimal("101.01"),
        "category": "kids",
        "is_active": True,
        "visit_time": timezone.make_aware(datetime(2026, 10, 11, 11, 30)),
    },
    {
        "name": "Стрижка под насадку",
        "price": Decimal("100"),
        "category": "haircut",
        "is_active": False,
        "visit_time": None,
    },
    {
        "name": "стрижка БОРОДЫ",
        "price": Decimal("50"),
        "category": "beard",
        "is_active": True,
        "visit_time": timezone.make_aware(datetime(2026, 10, 13, 12, 0)),
    },
    {
        "name": "Бритье бороды с бальзамом и массажем",
        "price": Decimal("157"),
        "category": "royal",
        "is_active": True,
        "visit_time": timezone.make_aware(datetime(2026, 10, 19, 9, 15)),
    },
    {
        "name": "Полный уход",
        "price": Decimal("2500"),
        "category": "combo",
        "is_active": True,
        "visit_time": None,
    },
    {
        "name": "Подровнять усы",
        "price": Decimal("147"),
        "category": "moustache",
        "is_active": True,
        "visit_time": None,
    },
    {
        "name": "Покраска волос",
        "price": Decimal("37"),
        "category": "camouflage",
        "is_active": True,
        "visit_time": timezone.make_aware(datetime(2026, 10, 13, 12, 0)),
    },
    {
        "name": "Бритье на лысо",
        "price": Decimal("0.5"),
        "category": "haircut",
        "is_active": False,
        "visit_time": timezone.make_aware(datetime(2026, 10, 13, 12, 30)),
    },
    {
        "name": "Экстремальное бритье",
        "price": Decimal("75"),
        "category": "shave",
        "is_active": True,
        "visit_time": None,
    },
]


class Command(BaseCommand):
    help = "Создаёт 10 записей Booking для ДЗ №3 (идемпотентно)"

    def handle(self, *args, **options):
        created_count = 0
        for data in BOOKINGS:
            _, created = Booking.objects.get_or_create(
                name=data["name"],
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Создана: {data['name']}"))

        # created_at «вчера» для строк 4 и 8 матрицы
        yesterday = timezone.localdate() - timedelta(days=1)
        Booking.objects.filter(
            name__in=["стрижка БОРОДЫ", "Покраска волос"],
        ).update(created_at=timezone.make_aware(
            datetime.combine(yesterday, datetime.min.time()),
        ))

        self.stdout.write(
            self.style.SUCCESS(f"Готово: создано {created_count} записей"),
        )