from django.db import models

from core.models import BaseModel
from account.constants import ClientStatusChoices


class Client(BaseModel):
    """Класс (таблица) клиента."""

    name = models.CharField(
        choices=ClientStatusChoices.choices,
        default=ClientStatusChoices.NOOB,
        verbose_name="статус",
    )

    date_of_birth = models.DateField(
        verbose_name="дата рождения",
    )

    user_id = models.OneToOneField(
        to="User",
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="client",
        unique=True,
    )

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        db_table = "clients"
        ordering = ["-id", "-created_at"]
