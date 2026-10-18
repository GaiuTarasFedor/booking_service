from django.db import models

from core.models import BaseModel


class Barber(BaseModel):
    """Класс (таблица) барберов."""

    experience_years = models.PositiveIntegerField(
        verbose_name="опыт работы",
        null=True,
        blank=True,
    )

    rating = models.PositiveIntegerField(
        verbose_name="рейтинг",
        null=True,
        blank=True,
    )

    user_id = models.OneToOneField(
        to="User",
        on_delete=models.CASCADE,
        verbose_name="барбер",
        related_name="barber",
    )

    barber_shop_id = models.ForeignKey(
        to="barber_shop.BarberShop",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="барбершоп",
        related_name="barbers",
    )

    class Meta:
        verbose_name = "барбер"
        verbose_name_plural = "барберы"
        db_table = "barbers"
        ordering = ["-id"]
