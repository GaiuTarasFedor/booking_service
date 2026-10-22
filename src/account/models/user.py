from django.contrib.auth.models import AbstractUser
from django.db import models

from account.management.commands.managers import UserManager
from core.models import BaseModel


class User(AbstractUser, BaseModel):
    """Клас (таблица) пользователей."""

    username = models.CharField(
        max_length=64,
        verbose_name="имя пользователя",
        # unique=True,
        null=True,
        blank=True,
    )

    phone = models.CharField(
        max_length=64,
        verbose_name="телефон",
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=64,
        verbose_name="имя",
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=64,
        verbose_name="фамилия",
        null=True,
        blank=True,
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="администратор",
    )

    email = models.EmailField(
        verbose_name="email",
        unique=True,
    )

    REQUIRED_FIELDS = []

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        db_table = "users"
        ordering = ["-id"]
