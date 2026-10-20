from django.core.management.base import BaseCommand
from django.db import transaction

from decimal import Decimal

from account.models.user import User
from account.constants import ClientStatusChoices
from account.models.client import Client
from account.models.barber import Barber
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

USERS = [
    {
        "email": "barberclient@example.com",
        "username": "admin",
        "first_name": "Админ",
        "last_name": "Админов",
        "phone": "84951234567",
        "is_staff": False,
        "password": "client",
    },
    {
        "email": "client@example.com",
        "username": "client",
        "first_name": "Иван",
        "last_name": "Иванов",
        "phone": "84957654321",
        "is_staff": False,
        "password": "client123",
    },
    {
        "email": "client1@example.com",
        "username": "barber",
        "first_name": "Петр",
        "last_name": "Петров",
        "phone": "84959876543",
        "is_staff": False,
        "password": "barber123",
    },
    {
        "email": "client2@example.com",
        "username": "client2",
        "first_name": "Алексей",
        "last_name": "Сидоров",
        "phone": "84951112233",
        "is_staff": False,
        "password": "client2pass",
    },
    {
        "email": "client3@example.com",
        "username": "client3",
        "first_name": "Дмитрий",
        "last_name": "Козлов",
        "phone": "84952223344",
        "is_staff": False,
        "password": "client3pass",
    },
    {
        "email": "client4@example.com",
        "username": "client4",
        "first_name": "Сергей",
        "last_name": "Новиков",
        "phone": "84953334455",
        "is_staff": False,
        "password": "client4pass",
    },
    {
        "email": "client5@example.com",
        "username": "client5",
        "first_name": "Андрей",
        "last_name": "Морозов",
        "phone": "84954445566",
        "is_staff": False,
        "password": "client5pass",
    },
    {
        "email": "client6@example.com",
        "username": "client6",
        "first_name": "Николай",
        "last_name": "Волков",
        "phone": "84955556677",
        "is_staff": False,
        "password": "client6pass",
    },
    {
        "email": "barber1@example.com",
        "username": "client7",
        "first_name": "Владимир",
        "last_name": "Соколов",
        "phone": "84956667788",
        "is_staff": False,
        "password": "client7pass",
    },
    {
        "email": "barber2@example.com",
        "username": "client8",
        "first_name": "Михаил",
        "last_name": "Лебедев",
        "phone": "84957778899",
        "is_staff": False,
        "password": "client8pass",
    },
    {
        "email": "barber3@example.com",
        "username": "client9",
        "first_name": "Артём",
        "last_name": "Кузнецов",
        "phone": "84958889900",
        "is_staff": False,
        "password": "client9pass",
    },
    {
        "email": "barber4@example.com",
        "username": "client10",
        "first_name": "Елена",
        "last_name": "Попова",
        "phone": "84959990011",
        "is_staff": False,
        "password": "client10pass",
    },
    {
        "email": "barber5@example.com",
        "username": "client11",
        "first_name": "Ольга",
        "last_name": "Федорова",
        "phone": "84950001122",
        "is_staff": False,
        "password": "client11pass",
    },
    {
        "email": "barber6@example.com",
        "username": "manager",
        "first_name": "Мария",
        "last_name": "Смирнова",
        "phone": "84951110022",
        "is_staff": False,
        "password": "manager123",
    },
    {
        "email": "barber7@example.com",
        "username": "manager",
        "first_name": "Мария",
        "last_name": "Смирнова",
        "phone": "84951110022",
        "is_staff": False,
        "password": "manager123",
    },
]

CLIENTS = [
    {
        "email": "client1@example.com",
        "status": ClientStatusChoices.MIDL,
        "date_of_birth": "1985-08-22",
    },
    {
        "email": "client2@example.com",
        "status": ClientStatusChoices.EXPERT,
        "date_of_birth": "1992-03-10",
    },
    {
        "email": "client3@example.com",
        "status": ClientStatusChoices.LEGENDA,
        "date_of_birth": "1988-11-30",
    },
    {
        "email": "client4@example.com",
        "status": ClientStatusChoices.NOOB,
        "date_of_birth": "1995-01-25",
    },
    {
        "email": "client5@example.com",
        "status": ClientStatusChoices.MIDL,
        "date_of_birth": "1991-07-18",
    },
    {
        "email": "client6@example.com",
        "status": ClientStatusChoices.EXPERT,
        "date_of_birth": "1987-12-05",
    },
    {
        "email": "barberclient@example.com",
        "status": ClientStatusChoices.LEGENDA,
        "date_of_birth": "1980-04-12",
    },
    {
        "email": "client@example.com",
        "status": ClientStatusChoices.NOOB,
        "date_of_birth": "1990-05-15",
    },
]

BARBERS = [
    {
        "email": "barber1@example.com",
        "barbershop": "ДРОВОСЕК",
        "experience_year": 5,
    },
    {
        "email": "barber2@example.com",
        "barbershop": "ДРОВОСЕК",
        "experience_year": 3,
    },
    {
        "email": "barber3@example.com",
        "barbershop": "ДРОВОСЕК",
        "experience_year": None,
    },
    {
        "email": "barber4@example.com",
        "barbershop": "ДРОВОСЕК",
        "experience_year": 1,
    },
    {
        "email": "barber5@example.com",
        "barbershop": "ДРОВОСЕК",
        "experience_year": 7,
    },
    {
        "email": "barber6@example.com",
        "barbershop": "ДРОВОСЕК",
        "experience_year": 2,
    },
    {
        "email": "barber7@example.com",
        "barbershop": "ДРОВОСЕК",
        "experience_year": 4,
    },
    {
        "email": "barberclient@example.com",
        "barbershop": "ДРОВОСЕК",
        "experience_year": 5,
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

            for data in USERS:
                password = data.get("password")
                user_fields = {k: v for k, v in data.items() if k != "password"}
                user, created = User.objects.update_or_create(
                    email=data["email"],
                    defaults=user_fields,
                )
                if password and created:
                    user.set_password(password)
                    user.save()
                if created:
                    created_count += 1

            for data in CLIENTS:
                user = User.objects.filter(email=data["email"]).first()
                if user:
                    client_fields = {k: v for k, v in data.items() if k != "email"}
                    client, created = Client.objects.get_or_create(
                        user=user,
                        defaults=client_fields,
                    )
                    if created:
                        created_count += 1

            for data in BARBERS:
                user = User.objects.filter(email=data["email"]).first()
                if user:
                    barbershop = Barbershop.objects.filter(name=data["barbershop"]).first()
                    if barbershop:
                        barber_fields = {
                            "barbershop": barbershop,
                            "experience_year": data.get("experience_year"),
                        }
                        barber, created = Barber.objects.get_or_create(
                            user=user,
                            defaults=barber_fields,
                        )
                        if created:
                            created_count += 1

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Готово: создано {created_count} записей."),
            )
        else:
            self.stdout.write("Записи уже существуют.")