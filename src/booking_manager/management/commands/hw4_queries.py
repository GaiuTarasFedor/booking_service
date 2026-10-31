from django.core.management.base import BaseCommand

from account.models import Barber
from booking_manager.models import (
    Barbershop,
    Booking,
    BookingService,
    Comment,
    Product,
)


class Command(BaseCommand):
    """Реализуем запросы ДЗ №4."""

    help = "Реализуем запросы ДЗ №4"

    def handle(self, *args, **options):

        # брони клиента `pk = 2`
        qs = Booking.objects.filter(client__id=2)
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # брони, у которых есть обратная связь с product_bookings (хоть одна)
        qs = Booking.objects.filter(product_bookings__isnull=False).distinct()
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # барберы, у которых есть обратная связь `comments`
        qs = Barber.objects.filter(comments__isnull=False).distinct()
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # комментарии клиента `pk=3`
        qs = Comment.objects.filter(client__id=3)
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # барбершопы, у которых есть обратная связь `barbers`
        qs = Barbershop.objects.filter(barbers__isnull=False).distinct()
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # услуги через `promotions` с `is_active=True`
        qs = BookingService.objects.filter(promotions__is_active=True).distinct()
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # брони, у которых `rating=5` (путь через клиента)
        qs = Booking.objects.filter(client__comments__rating=5).distinct()
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # товары через `product_bookings__booking__client__status="noob"`
        qs = Product.objects.filter(product_bookings__booking__client__status="noob").distinct()
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # услуги через `bookings__client__comments__rating__lt=3`
        qs = BookingService.objects.filter(bookings__client__comments__rating__lt=3).distinct()
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")

        # брони с `product_bookings__product__name="Шампунь"` __и__ `barber__experience_year__gt=3`
        qs = Booking.objects.filter(
            product_bookings__product__name="Шампунь", barber__experience_year__gt=3
        ).distinct()
        self.stdout.write(f"{qs.query}")
        self.stdout.write(f"{qs.count()}")
