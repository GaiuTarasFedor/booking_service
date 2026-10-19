from django.db import models

from core.models import BaseModel


class Promotion(BaseModel):
    """Класс для хранения акций."""

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

    discount_percent = models.PositiveSmallIntegerField(
        verbose_name="размер скидки",
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        verbose_name="дата начала",
    )

    end_date = models.DateField(
        verbose_name="дата окончания",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="активная",
    )

    services = models.ManyToManyField(
        to="BookingService",
        verbose_name="скидка",
        related_name="promotions",
    )

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name = "акция"
        verbose_name_plural = "акции"
        db_table = "promotions"
        ordering = ["-id", "name"]