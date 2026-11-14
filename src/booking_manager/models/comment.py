from django.db import models

from core.models import BaseModel, RatingMixin


class Comment(BaseModel, RatingMixin):
    """Класс для хранения комментариев."""

    text = models.TextField(
        verbose_name="комментарий",
        blank=True,
        default="",
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="активный",
    )

    client = models.ForeignKey(
        to="account.Client",
        verbose_name="клиент",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    barber = models.ForeignKey(
        to="account.Barber",
        verbose_name="Барбер",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    booking = models.OneToOneField(
        to="Booking",
        verbose_name="Бронирование",
        on_delete=models.CASCADE,
        related_name="comment",
    )

    def __str__(self):
        return f"{self.barber} - {self.rating}"

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        db_table = "comments"
        ordering = ["-created_at", "-rating"]
