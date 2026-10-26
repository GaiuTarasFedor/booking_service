from django.core.validators import MinValueValidator
from django.db import models

from booking_manager.constants import CategoryChoices
from core.models import BaseModel


class BookingService(BaseModel):
    """Класс для хранения информации о об услугах, доступных для бронирования."""

    # решил создать свой id, не по умолчанию
    id = models.BigAutoField(
        verbose_name="id",
        primary_key=True,
    )

    category = models.CharField(
        max_length=10,
        choices=CategoryChoices,
        verbose_name="категория",
        default=CategoryChoices.SERVICE_HAIRCUT,
    )

    name = models.CharField(
        max_length=30,
        verbose_name="наименование",
        unique=True,
    )

    description = models.TextField(
        max_length=255,
        verbose_name="описание",
        blank=True,
        default="",
    )

    price = models.DecimalField(
        verbose_name="цена",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    duration_minutes = models.PositiveIntegerField(
        verbose_name="продолжительность в минутах",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="активна",
    )

    class Meta:
        db_table = "booking_service"
        verbose_name = "услуга"
        # В дополнение к валидации Python добавил валидацию в БД
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="price",
                violation_error_message="Цена не может быть меньше 0.",
            )
        ]
        # как я понял запись должна идти по уникальным позициям таблицы:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name
