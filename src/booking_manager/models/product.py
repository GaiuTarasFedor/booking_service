from django.db import models
from django.core.validators import MinValueValidator

from core.models import BaseModel


class Product(BaseModel):
    """Класс (таблица) для хранения информации о продуктах, доступных для бронирования."""

    id = models.AutoField(
        verbose_name="id",
        primary_key=True,
    )

    name = models.CharField(
        max_length=30,
        verbose_name="наименование",
        unique=True,
    )

    description = models.TextField(
        max_length=255,
        verbose_name="описание",
        null=True,
        blank=True,
    )

    amount = models.PositiveIntegerField(
        verbose_name="количество",
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        verbose_name="цена",
        validators=[MinValueValidator(0)],
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
    )

    bookings = models.ManyToManyField(
        to="Booking",
        verbose_name="бронирования",
        related_name="products",
        through="ProductBooking",
    )

    class Meta:
        db_table = "product"
        verbose_name = "товар"
        # В дополнение к валидации Python добил валидацию в БД
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="price_non_negative",
                violation_error_message="Цена не может быть меньше 0.",
            )
        ]
        ordering = ["created_at", "id", "-amount"]

    def __str__(self):
        return self.name
