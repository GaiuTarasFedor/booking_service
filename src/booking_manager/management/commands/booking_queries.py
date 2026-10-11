"""В этом модуле собран класс демонстрирующий ORM-запросы к базе данных."""

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import Booking


class Command(BaseCommand):
    """Демонстрирует запросы к Booking."""

    help = "Демонстрирует запросы к Booking."

    def handle(self, *args, **options):

        # all() — все записи
        self.stdout.write("Задание №2: все записи:")
        qs = Booking.objects.all()
        for n, b in enumerate(qs, 1):
            self.stdout.write(f" {n}. id{b.id}: {b.name} — {b.price}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

        print("\n")
        # filter() — выборка по условию
        self.stdout.write("Задание №3: цена > 100:")
        qs = Booking.objects.filter(price__gt=100)
        for n, b in enumerate(qs, 1):
            self.stdout.write(f"  {n}. id{b.id}: {b.name} — {b.price}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

        print("\n")
        self.stdout.write("Задание №4: в названии есть «стрижка», без учёта регистра")
        qs = Booking.objects.filter(name__icontains="стрижка")
        for n, b in enumerate(qs, 1):
            self.stdout.write(f"  {n}. id{b.id}: {b.name}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

        print("\n")
        self.stdout.write("Задание №5: название начинается с «Муж», без учёта регистра")
        qs = Booking.objects.filter(name__istartswith="Муж")
        for n, b in enumerate(qs, 1):
            self.stdout.write(f"  {n}. id{b.id}: {b.name}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

        print("\n")
        self.stdout.write("Задание №6: не указано время визита")
        qs = Booking.objects.filter(visit_time__isnull=True)
        for n, b in enumerate(qs, 1):
            self.stdout.write(f"  {n}. id{b.id}: {b.name}, {b.visit_time}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

        print("\n")
        self.stdout.write("Задание №7: активные, категория HAIRCUT, цена ≤ 100")
        qs = Booking.objects.filter(is_active=True, category="haircut", price__lte=100)
        for n, b in enumerate(qs, 1):
            self.stdout.write(f"  {n}. id{b.id}: {b.name}, {b.category}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

        print("\n")
        self.stdout.write("Задание №8: категории HAIRCUT и MOUSTACHE")
        qs = Booking.objects.filter(category__in=["haircut", "moustache"])
        for n, b in enumerate(qs, 1):
            self.stdout.write(f"  {n}. id{b.id}: {b.name}, {b.category}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

        print("\n")
        self.stdout.write("Задание №9: всё, кроме «неактивные и дешёвые")
        qs = Booking.objects.exclude(is_active=False, price__lte=50)
        for n, b in enumerate(qs, 1):
            self.stdout.write(f"  {n}. id{b.id}: {b.name}, {b.price}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

        print("\n")
        self.stdout.write("Задание №10: созданные сегодня")
        # обновил дату для реализации запроса
        Booking.objects.exclude(
            name__in=["стрижка БОРОДЫ", "Покраска волос"],
        ).update(created_at=timezone.now()
        )
        qs = Booking.objects.filter(created_at__date=timezone.localdate())
        for n, b in enumerate(qs, 1):
            self.stdout.write(f"  {n}. id{b.id}: {b.name}, {b.category}")
        self.stdout.write(f"Найдено: {qs.count()}")
        self.stdout.write(f"Запрос: {str(qs.query)}\n")

