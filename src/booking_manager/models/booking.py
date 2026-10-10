from django.db import models
from django.core.validators import MinValueValidator

from ..constants import CategoryChoices


class Booking(models.Model):
    """Создаем таблицу бронирований мастеров в БД"""
    name = models.CharField(
        max_length=50,
        verbose_name="наименование",
        unique=True,
    )

    # не поставил max_length - по документации он игнорируется если TextField (если я правильно понял)
    description = models.TextField(
        verbose_name="описание",
        blank=True,
    )

    # использовал Decimal в связи со спецификой округлений и расчетов в Float
    price = models.DecimalField(
        verbose_name="цена",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    category = models.CharField(
        max_length=10,
        choices=CategoryChoices,
        verbose_name="категория",
        default=CategoryChoices.SERVICE_HAIRCUT,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="активна"
    )

    visit_time = models.DateTimeField(
        verbose_name="время визита",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Время создания записи",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Время изменения записи",
        auto_now=True,
    )

    class Meta:
        db_table = "booking"
        verbose_name = "бронирование мастера"
        verbose_name_plural = "бронирования мастеров"
        # В дополнение к валидации Python добил валидацию в БД
        constraints = [models.CheckConstraint(
            condition=models.Q(price__gte=0),
            name="price_non_negative",
            violation_error_message="Цена не может быть меньше 0."
        )]
        # как я понял запись должна идти по уникальным позициям таблицы:
        ordering = ["-created_at", "id"]

    def __str__(self):
        return self.name