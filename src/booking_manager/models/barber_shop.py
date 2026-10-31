from django.db import models

from core.models import BaseModel


class Barbershop(BaseModel):
    """Класс для хранения информации о барбершопе и его местонахождении."""

    name = models.CharField(
        max_length=64,
        verbose_name="название",
        unique=True,
    )

    phone = models.CharField(
        max_length=255,
        verbose_name="телефон",
        blank=True,
        default="",
    )

    address = models.CharField(
        max_length=64,
        verbose_name="адрес",
        blank=True,
        default="",
    )

    description = models.TextField(
        max_length=255,
        verbose_name="описание",
        blank=True,
        default="",
    )

    opening_time = models.TimeField(
        verbose_name="время открытия",
    )

    closing_time = models.TimeField(
        verbose_name="время закрытия",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="активный",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "офис"
        verbose_name_plural = "офисы"
        db_table = "barbershops"
        ordering = ["-id", "name"]
