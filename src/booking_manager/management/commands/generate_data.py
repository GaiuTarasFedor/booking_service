from datetime import UTC, datetime, time, timedelta
from random import choice

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from account.constants import ClientStatusChoices
from account.models import Barber, Client, User
from booking_manager.models import (
    Barbershop,
    Booking,
    BookingService,
    Comment,
    Product,
    ProductBooking,
    Promotion,
)

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

from decimal import Decimal

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
    """Команда для генерации тестовых данных в БД."""

    help = "Генерация тестовых данных для приложения booking_manager"

    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        fake.seed_instance(2026)
        with transaction.atomic():
            count_created = 0
            for data in BARBERSHOPS:
                _, created = Barbershop.objects.get_or_create(
                        name=data["name"],
                        defaults=data
                    )
                if created:
                    count_created += 1
        
        if count_created == 0:
            self.stdout.write("Барбершопы уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} барбершопов.")
        self.stdout.write(f"В базе данных находится {Barbershop.objects.count()} барбершопов.")

        with transaction.atomic():
            count_created = 0
            for data in BOOKINGSERVICE:
                _, created = BookingService.objects.get_or_create(
                        name=data["name"],
                        defaults=data
                    )
                if created:
                    count_created += 1
        
        if count_created == 0:
            self.stdout.write("Услуги уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} услуг.")
        self.stdout.write(f"В базе данных находится {BookingService.objects.count()} услуг.")

        with transaction.atomic():
            count_created = 0
            for i in range(1, 51):
                _, created = Product.objects.update_or_create(
                    name = f"Товар gen {i:02d}", 
                    defaults = {
                        "price": fake.pydecimal(
                            left_digits=2, 
                            right_digits=2, 
                            min_value=2,
                            positive=True
                            ),
                        "amount": fake.pyint(min_value=1, max_value=20),
                        "description": fake.text(max_nb_chars=30)
                    }
                )
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Продукты уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} продуктов.")
        self.stdout.write(f"В базе данных находится {Product.objects.count()} продуктов.")

        with transaction.atomic():
            list_servace = list(BookingService.objects.all())
            count_created = 0
            for i in range(1, 11):
                random_services = fake.random_elements(elements=list_servace, length=3)
                description = fake.text(max_nb_chars=30)
                discount_percent = fake.pyint(min_value=0, max_value=20)
                start_date = fake.date_between(start_date='-1w')
                end_date = start_date + timedelta(days=fake.pyint(min_value=2, max_value=7))
                is_active = True
                promo, created = Promotion.objects.get_or_create(
                    name=f"Акция № {i:02d}",
                    defaults={
                    "description":description,
                    "discount_percent":discount_percent,
                    "start_date":start_date,
                    "end_date":end_date,
                    "is_active":is_active,
                    }
                )
                promo.services.set(random_services)
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Акции уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} акций.")
        self.stdout.write(f"В базе данных находится {Promotion.objects.count()} акций.")
            
        with transaction.atomic():
            password ="password123"
            count_created = 0
            for i in range(1, 101):
                if User.objects.filter(email=f"gen_user{i:03d}@example.com").exists():
                    continue
                else:
                    other_fields={
                        "username": f"gen_user{i:03d}.@example.com",
                        "first_name": fake.first_name(),
                        "last_name": fake.last_name(),
                        "phone": fake.phone_number(),
                        "is_staff": False,
                    }
                    User.objects.create_user(
                        email=f"gen_user{i:03d}@example.com",
                        password=password,
                        **other_fields)
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Пользователи уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} пользователей.")
        self.stdout.write(f"В базе данных находится {User.objects.count()} пользователей.")
            
        with transaction.atomic():
            users = User.objects.filter(email__startswith="gen_user").order_by("id")[:95]
            qs_barber = users[:15]
            qs_client = users[15:95]
            list_barbershops = list(Barbershop.objects.all())
            list_status = list(ClientStatusChoices)
            count_created = 0
            for user in qs_barber:
                _, created = Barber.objects.get_or_create(
                        user=user,
                        defaults={
                            "experience_year": fake.pyint(min_value=0, max_value=20),
                            "barbershop": fake.random_element(elements=list_barbershops)
                        }
                    )   
                if created:
                    count_created += 1
            for user in qs_client:
                _, created = Client.objects.get_or_create(
                        user=user,
                        defaults={
                            "status": fake.random_element(elements=list_status),
                            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70)
                        }
                    )   
                if created:
                    count_created += 1
            if count_created == 0:
                self.stdout.write("Клиенты и барберы уже существуют в базе данных, новые не создавались.")
            else:
                self.stdout.write(f"Создано {count_created} клиентов и барберов.")
            self.stdout.write(
                f"В базе данных находится {Client.objects.count()} клиентов и {Barber.objects.count()} барберов."
            )

        with transaction.atomic():
            list_clients = list(Client.objects.filter(
                user__email__startswith="gen_user").select_related("user").order_by("id")
                )
            list_barbers = list(Barber.objects.filter(
                user__email__startswith="gen_user"
                ).select_related("barbershop", "user").order_by('id')
                )
            list_services = list(BookingService.objects.all())
            count_created = 0
            for i in range(1, 501):
                barber = choice(list_barbers)
                client = choice(list_clients)
                service = choice(list_services)
                _, created = Booking.objects.get_or_create(
                    name=f"Бронь gen {i:04d}",
                    defaults={
                        "visit_time": fake.date_time_between(start_date='-30d', end_date='+30d', tzinfo=UTC),
                        "is_active": fake.boolean(chance_of_getting_true=80),
                        "booking_service": service,
                        "barber": barber,
                        "client": client,
                        "barbershop": barber.barbershop,
                    }
                )
                if created:
                    count_created += 1

        if count_created == 0:
            self.stdout.write("Брони уже существуют в базе данных, новые не создавались.")
        else:
            self.stdout.write(f"Создано {count_created} записей о бронировании.")
        self.stdout.write(f"В базе данных находится {Booking.objects.count()} записей о брони.")

        with transaction.atomic():
            list_bookings = list(
                Booking.objects.select_related("barber", "client").filter(
                    name__startswith="Бронь gen", visit_time__lte=datetime.now(UTC)
                    ).order_by("id")[:200]
                )
            count_created = 0
            for booking in list_bookings:
                _, created = Comment.objects.get_or_create(
                    booking = booking,
                    defaults={
                        "text": fake.text(max_nb_chars=100),
                        "is_published": fake.boolean(chance_of_getting_true=80),
                        "barber": booking.barber,
                        "client": booking.client,
                        "rating": fake.pyint(min_value=0, max_value=5),
                    }
                )
                if created:
                    count_created += 1
 
        if count_created == 0:
             self.stdout.write("Комментарии уже существуют в базе данных, новые не создавались.")
        else:
             self.stdout.write(f"Создано {count_created} комментариев.")
        self.stdout.write(f"В базе данных находится {Comment.objects.count()} комментариев.")

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
                    booking = booking,
                    defaults={
                        "product": product,
                        "total_price": (product.price or Decimal(0)) * quantity,
                        "quantity": quantity,
                    }
                )
                if created:
                    count_created += 1
 
        if count_created == 0:
             self.stdout.write("Связи 'бронирование - продукт' уже существуют в базе данных, новые не создавались.")
        else:
             self.stdout.write(f"Создано {count_created} связей 'бронирование - продукт'.")
        self.stdout.write(f"В базе данных находится {ProductBooking.objects.count()} связей 'бронирование - продукт'.")

        