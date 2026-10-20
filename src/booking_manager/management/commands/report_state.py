from django.core.management.base import BaseCommand

from account.models import User, Client, Barber
from booking_manager.models import Barbershop, BookingService, Product, Promotion, Booking, Comment, ProductBooking


class Command(BaseCommand):
    """Получаем количество строк в таблицах."""

    help = "Получаем количество строк в таблицах."

    def handle(self, *args, **options):

        user_count = User.objects.count()
        self.stdout.write(f"{user_count=}")

        client_count = Client.objects.count()
        self.stdout.write(f"{client_count=}")

        barber_count = Barber.objects.count()
        self.stdout.write(f"{barber_count=}")

        barbershop_count = Barbershop.objects.count()
        self.stdout.write(f"{barbershop_count=}")

        book_service_count = BookingService.objects.count()
        self.stdout.write(f"{book_service_count=}")

        promotion_count = Promotion.objects.count()
        self.stdout.write(f"{promotion_count=}")

        booking_count = Booking.objects.count()
        self.stdout.write(f"{booking_count=}")

        comment_count = Comment.objects.count()
        self.stdout.write(f"{comment_count=}")

        product_count = Product.objects.count()
        self.stdout.write(f"{product_count=}")

        product_booking_count = ProductBooking.objects.count()
        self.stdout.write(f"{product_booking_count=}")
