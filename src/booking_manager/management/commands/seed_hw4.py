from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from account.constants import ClientStatusChoices
from account.models.barber import Barber
from account.models.client import Client
from account.models.user import User

from ...models import (
    Barbershop,
    Booking,
    BookingService,
    Comment,
    Product,
    ProductBooking,
    Promotion,
)

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

BOOKINGS = [
    {
        "name": "Бронь client2-1",
        "client_email": "client2@example.com",
        "barber_email": "barber1@example.com",
        "service_name": "Супермодель",
        "barbershop": "ДРОВОСЕК",
        "visit_time": datetime(2026, 11, 1, 10, 0, tzinfo=timezone.UTC),
        "is_active": True,
    },
    {
        "name": "Бронь client2-2",
        "client_email": "client2@example.com",
        "barber_email": "barber2@example.com",
        "service_name": "Бородач",
        "barbershop": "ДРОВОСЕК",
        "visit_time": datetime(2026, 11, 5, 14, 0, tzinfo=timezone.UTC),
        "is_active": True,
    },
    {
        "name": "Бронь client3-1",
        "client_email": "client3@example.com",
        "barber_email": "barber3@example.com",
        "service_name": "Супермодель",
        "barbershop": "ДРОВОСЕК",
        "visit_time": datetime(2026, 11, 10, 11, 0, tzinfo=timezone.UTC),
        "is_active": True,
    },
    {
        "name": "Бронь client3-2",
        "client_email": "client3@example.com",
        "barber_email": "barber4@example.com",
        "service_name": "Мистер мускул",
        "barbershop": "ДРОВОСЕК",
        "visit_time": None,
        "is_active": True,
    },
    {
        "name": "Бронь client1",
        "client_email": "client1@example.com",
        "barber_email": "barber5@example.com",
        "service_name": "Корона",
        "barbershop": "ДРОВОСЕК",
        "visit_time": datetime(2026, 11, 15, 9, 0, tzinfo=timezone.UTC),
        "is_active": True,
    },
    {
        "name": "Бронь client4",
        "client_email": "client4@example.com",
        "barber_email": "barber1@example.com",
        "service_name": "Серебро",
        "barbershop": "ДРОВОСЕК",
        "visit_time": datetime(2026, 11, 20, 16, 0, tzinfo=timezone.UTC),
        "is_active": True,
    },
    {
        "name": "Бронь client5",
        "client_email": "client5@example.com",
        "barber_email": "barber6@example.com",
        "service_name": "Слалом",
        "barbershop": "ДРОВОСЕК",
        "visit_time": datetime(2026, 11, 25, 12, 0, tzinfo=timezone.UTC),
        "is_active": True,
    },
    {
        "name": "Бронь client6",
        "client_email": "client6@example.com",
        "barber_email": "barber7@example.com",
        "service_name": "Юниверсал",
        "barbershop": "ДРОВОСЕК",
        "visit_time": None,
        "is_active": True,
    },
]

COMMENTS = [
    {
        "booking_name": "Бронь client2-1",
        "client_email": "client2@example.com",
        "barber_email": "barber1@example.com",
        "text": "Отличный мастер, рекомендую!",
        "rating": 5,
        "is_published": True,
    },
    {
        "booking_name": "Бронь client2-2",
        "client_email": "client2@example.com",
        "barber_email": "barber2@example.com",
        "text": "Хорошая стрижка",
        "rating": 4,
        "is_published": True,
    },
    {
        "booking_name": "Бронь client3-1",
        "client_email": "client3@example.com",
        "barber_email": "barber3@example.com",
        "text": "Нормально",
        "rating": 3,
        "is_published": True,
    },
    {
        "booking_name": "Бронь client3-2",
        "client_email": "client3@example.com",
        "barber_email": "barber4@example.com",
        "text": "Не очень понравилось",
        "rating": 2,
        "is_published": True,
    },
    {
        "booking_name": "Бронь client1",
        "client_email": "client1@example.com",
        "barber_email": "barber5@example.com",
        "text": "Превосходно!",
        "rating": 5,
        "is_published": True,
    },
    {
        "booking_name": "Бронь client4",
        "client_email": "client4@example.com",
        "barber_email": "barber1@example.com",
        "text": "Быстро и качественно",
        "rating": 4,
        "is_published": False,
    },
    {
        "booking_name": "Бронь client5",
        "client_email": "client5@example.com",
        "barber_email": "barber6@example.com",
        "text": "Средне",
        "rating": 3,
        "is_published": True,
    },
    {
        "booking_name": "Бронь client6",
        "client_email": "client6@example.com",
        "barber_email": "barber7@example.com",
        "text": "Отлично!",
        "rating": 5,
        "is_published": True,
    },
]

PRODUCT_BOOKINGS = [
    {
        "booking_name": "Бронь client2-1",
        "product_name": "Шампунь",
        "quantity": 2,
        "total_price": Decimal("20.00"),
    },
    {
        "booking_name": "Бронь client2-2",
        "product_name": "Шампунь",
        "quantity": 1,
        "total_price": Decimal("10.00"),
    },
    {
        "booking_name": "Бронь client4",
        "product_name": "Шампунь",
        "quantity": 3,
        "total_price": Decimal("30.00"),
    },
    {
        "booking_name": "Бронь client4",
        "product_name": "Лак для волос",
        "quantity": 1,
        "total_price": Decimal("10.00"),
    },
    {
        "booking_name": "Бронь client1",
        "product_name": "Крем после бритья",
        "quantity": 2,
        "total_price": Decimal("20.00"),
    },
    {
        "booking_name": "Бронь client3-1",
        "product_name": "Скраб ромашка",
        "quantity": 1,
        "total_price": Decimal("10.00"),
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

            for data in BOOKINGS:
                client_user = User.objects.filter(email=data["client_email"]).first()
                barber_user = User.objects.filter(email=data["barber_email"]).first()
                if client_user and barber_user:
                    client = Client.objects.filter(user=client_user).first()
                    barber = Barber.objects.filter(user=barber_user).first()
                    if client and barber:
                        service = BookingService.objects.filter(name=data["service_name"]).first()
                        bs = Barbershop.objects.filter(name=data["barbershop"]).first()
                        if service and bs:
                            booking_fields = {
                                "name": data["name"],
                                "client": client,
                                "barber": barber,
                                "booking_service": service,
                                "barbershop": bs,
                                "visit_time": data.get("visit_time"),
                                "is_active": data.get("is_active", True),
                            }
                            _, created = Booking.objects.update_or_create(
                                name=data["name"],
                                defaults=booking_fields,
                            )
                            if created:
                                created_count += 1

            for data in COMMENTS:
                booking = Booking.objects.filter(name=data["booking_name"]).first()
                if booking:
                    client_user = User.objects.filter(email=data["client_email"]).first()
                    barber_user = User.objects.filter(email=data["barber_email"]).first()
                    if client_user and barber_user:
                        client = Client.objects.filter(user=client_user).first()
                        barber = Barber.objects.filter(user=barber_user).first()
                        if client and barber:
                            comment_fields = {
                                "booking": booking,
                                "client": client,
                                "barber": barber,
                                "text": data["text"],
                                "rating": data["rating"],
                                "is_published": data["is_published"],
                            }
                            _, created = Comment.objects.update_or_create(
                                booking=booking,
                                defaults=comment_fields,
                            )
                            if created:
                                created_count += 1

            for data in PRODUCT_BOOKINGS:
                booking = Booking.objects.filter(name=data["booking_name"]).first()
                if booking:
                    product = Product.objects.filter(name=data["product_name"]).first()
                    if product:
                        pb_fields = {
                            "booking": booking,
                            "product": product,
                            "quantity": data["quantity"],
                            "total_price": data["total_price"],
                        }
                        _, created = ProductBooking.objects.update_or_create(
                            booking=booking,
                            product=product,
                            defaults=pb_fields,
                        )
                        if created:
                            created_count += 1

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Готово: создано {created_count} записей."),
            )
        else:
            self.stdout.write("Записи уже существуют.")
