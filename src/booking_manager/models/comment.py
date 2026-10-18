from django.db import models

from core.models import BaseModel


class Comment(BaseModel):
    """Класс для хранения комментариев."""

    text = models.TextField(
        verbose_name="комментарий",
        null=True,
        blank=True,
    )

    rating = models.PositiveIntegerField(
        verbose_name="рейтинг",
        null=True,
        blank=True,
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="активный",
    )

    client_id = models.OneToOneField(
        to="account.Client",
        verbose_name="клиент",
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
    )

    barber_id = models.OneToOneField(
        to="account.Barber",
        verbose_name="Барбер",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    booking_id = models.OneToOneField(
        to="Booking",
        verbose_name="Бронирование",
        on_delete=models.CASCADE,
        related_name="comment",
        unique=True
    )

    def __str__(self):
        return f"{self.id} - {self.booking}"

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        db_table = "comments"
        ordering = ["-id", "rating"]