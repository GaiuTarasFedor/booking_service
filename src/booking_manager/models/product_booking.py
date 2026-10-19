import uuid

from django.db import models
from django.core.validators import MinValueValidator

from core.models import BaseModel


class ProductBooking(BaseModel):
    """Класс (таблица) для хранения информации о продуктах, используемых в определенном бронировании."""

    # решил создать свой id, не по умолчанию
    id = models.UUIDField(
        verbose_name="id", default=uuid.uuid4, primary_key=True, editable=False
    )

    product = models.ForeignKey(
        to="Product",
        verbose_name="используемые товары",
        on_delete=models.CASCADE,
        related_name="product_bookings",
        null=True,
    )

    booking = models.ForeignKey(
        to="Booking",
        verbose_name="Бронирование",
        on_delete=models.CASCADE,
        related_name="product_bookings",
        null=True,
    )

    quantity = models.PositiveIntegerField(
        verbose_name="количество",
    )

    total_price = models.DecimalField(
        verbose_name="итоговая цена",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        default=0,
    )

    class Meta:
        db_table = "product_bookings"
        verbose_name = "товары в бронировании"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_price__gte=0),
                name="total_price_non_negative",
                violation_error_message="Итоговая цена не может быть меньше 0.",
            )
        ]

    def __str__(self):
        return f"{self.product_id} — {self.quantity} шт."
