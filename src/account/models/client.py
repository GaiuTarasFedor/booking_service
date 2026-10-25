from django.db import models

from account.constants import ClientStatusChoices
from core.models import BaseModel


class Client(BaseModel):
    """Класс (таблица) клиента."""

    status = models.CharField(
        choices=ClientStatusChoices.choices,
        default=ClientStatusChoices.NOOB,
        verbose_name="статус",
    )

    date_of_birth = models.DateField(
        verbose_name="дата рождения",
    )

    user = models.OneToOneField(
        to="User",
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="client",
        unique=True,
    )

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        db_table = "clients"
        ordering = ["-id", "-created_at"]
