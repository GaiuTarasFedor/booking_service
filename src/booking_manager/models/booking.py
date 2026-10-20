from django.db import models
from django.db.models.deletion import SET_DEFAULT

from core.models import BaseModel
from booking_manager.constants import CategoryChoices

class Booking(BaseModel):
    """Класс (таблица) бронирования услуг."""

    id = models.BigAutoField(
        verbose_name="Id",
        primary_key=True,
    )

    name = models.CharField(
        max_length=30,
        verbose_name="наименование",
        unique=True,
    )

    visit_time = models.DateTimeField(
        verbose_name="время визита",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="активна",
    )

    booking_service = models.ForeignKey(
        to="BookingService",
        verbose_name="услуга",
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    barber = models.ForeignKey(
        to="account.Barber",
        verbose_name="Барбер",
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    barbershop = models.ForeignKey(
        to="BarberShop",
        verbose_name="Офис",
        on_delete=models.SET_NULL,
        related_name="bookings",
        null=True,
    )

    client = models.ForeignKey(
        to="account.Client",
        verbose_name="клиент",
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "bookings"
        verbose_name = "Бронирование мастера"
        ordering = ["-created_at", "name"]
