from django.core.management.base import BaseCommand
from django.db import transaction

from decimal import Decimal

from ...models import Barbershop, BookingService, Product, Promotion


BARBERSHOP = [
    {
        "name": "ДРОВОСЕК",
        "phone": "84954258955",
        "address": "Москва, ул. Мичуринская, д. 55",
        "description": "Лучшие бороды города по низкой цене!",
        "opening_time": "09:00",
        "closing_time": "21:00",
        "is_active": True,
    },
    {
        "name": "ОГОНЕК",
        "phone": "84956842154",
        "address": "Москва, ул. Новогодняя, д. 7",
        "description": "Усы и борода - украшение лица!",
        "opening_time": "08:00",
        "closing_time": "20:00",
        "is_active": True,
    },
]

BOOKINGSERVICE = [
    {
        "category": "haircut",
        "name": "Супермодель",
        "description": "мойка головы, стрижка, укладка",
        "price": Decimal("75"),
        "duration_minutes": 30,
        "is_active": True,
    },
    {
        "category": "moustache",
        "name": "Мистер мускул",
        "description": "мойка усов, стрижка, мелирование",
        "price": Decimal("120.5"),
        "duration_minutes": 15,
        "is_active": True,
    },
    {
        "category": "beard",
        "name": "Бородач",
        "description": "мойка головы, стрижка, сушка и укладка",
        "price": Decimal("15"),
        "duration_minutes": 25,
        "is_active": True,
    },
    {
        "category": "kids",
        "name": "Младенец",
        "description": "мойка головы, стрижка, укладка",
        "price": Decimal("101"),
        "duration_minutes": 20,
        "is_active": True,
    },
    {
        "category": "camouflage",
        "name": "Серебро",
        "description": "мойка головы, укладка",
        "price": Decimal("75"),
        "duration_minutes": 40,
        "is_active": True,
    },
    {
        "category": "royal",
        "name": "Корона",
        "description": "мойка головы, стрижка, укладка",
        "price": Decimal("99"),
        "duration_minutes": 50,
        "is_active": True,
    },
    {
        "category": "shave",
        "name": "Слалом",
        "description": "мойка головы, стрижка",
        "price": Decimal("10"),
        "duration_minutes": 45,
        "is_active": True,
    },
    {
        "category": "combo",
        "name": "Юниверсал",
        "description": "мойка головы, бритье, укладка",
        "price": Decimal("75"),
        "duration_minutes": 40,
        "is_active": True,
    },
]

PRODUCT = [
    {
        "name": "Скраб ромашка",
        "description": "увлажняет и придает блеск",
        "amount": 5,
        "price": Decimal("10"),
    },
    {
        "name": "Тройной одеколон",
        "description": "сушит и защищает",
        "amount": 10,
        "price": Decimal("10"),
    },
    {
        "name": "Сухая присыпка",
        "description": "сушит кожу",
        "amount": 3,
        "price": Decimal("10"),
    },
    {
        "name": "Крем после бритья",
        "description": "очень хорошо защищает кожу",
        "amount": 20,
        "price": Decimal("10"),
    },
    {
        "name": "Пудра",
        "description": "увлажняет и придает блеск",
        "amount": 1,
        "price": Decimal("10"),
    },
    {
        "name": "Шампунь",
        "description": "увлажняет",
        "amount": 0,
        "price": Decimal("10"),
    },
    {
        "name": "Отдушка",
        "description": "увлажняет и не придает блеск",
        "amount": 5,
        "price": Decimal("10"),
    },
    {
        "name": "Лак для волос",
        "description": "увлажняет и придает блеск",
        "amount": 17,
        "price": Decimal("10"),
    },

]

PROMOTION = [
    {
        "name": "23 февраля",
        "description": "Всем служившим - скидка 15%",
        "discount_percent": 15,
        "start_date": "2026-10-15",
        "end_date": "2026-11-01",
        "is_active": True,
    },
    {
        "name": "4 ноября",
        "description": "скидка 10%",
        "discount_percent": 10,
        "start_date": "2026-10-15",
        "end_date": "2026-11-11",
        "is_active": True,
        "services": ["Супермодель", "Мистер мускул"],
    },
    {
        "name": "01 января",
        "description": "для самых стойких скидка 50%",
        "discount_percent": 50,
        "start_date": "2026-12-31",
        "end_date": "2027-01-02",
        "is_active": False,
        "services": ["Мистер мускул", "Бородач"],
    },
]


class Command(BaseCommand):
    """Создаёт записи для ДЗ №4 (идемпотентно)."""

    help = "Создаёт записи для ДЗ №4 (идемпотентно)."

    def handle(self, *args, **options):
        with transaction.atomic():
            created_count = 0
            for data in BARBERSHOP:
                _, created = Barbershop.objects.update_or_create(
                    name=data["name"],
                    defaults=data,
                )
                if created:
                    created_count += 1

            for data in BOOKINGSERVICE:
                _, created = BookingService.objects.update_or_create(
                    name=data["name"],
                    defaults=data,
                )
                if created:
                    created_count += 1

            for data in PRODUCT:
                _, created = Product.objects.update_or_create(
                    name=data["name"],
                    defaults=data,
                )
                if created:
                    created_count += 1

            for data in PROMOTION:
                services_names = data.get("services", [])
                promotion_fields = {k: v for k, v in data.items() if k not in ("name", "services")}
                promotion, created = Promotion.objects.update_or_create(
                    name=data["name"],
                    defaults=promotion_fields,
                )
                if created:
                    created_count += 1
                # Устанавливаем связи ManyToMany после создания/обновления

                service_objs = BookingService.objects.filter(name__in=services_names)
                promotion.services.set(service_objs)

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Готово: создано {created_count} записей."),
            )
        else:
            self.stdout.write("Записи уже существуют.")