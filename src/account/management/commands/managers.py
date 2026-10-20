from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from django.contrib.auth.hashers import make_password


class UserQuerySet(models.QuerySet):
    pass


# class TaskManager(models.Manager):
#
#     def get_queryset(self):
#         return UserQuerySet(self.model, using=self._db)


class UserManager(BaseUserManager):
    """Создаем шаблон пользователя/суперпользователя."""

    def _create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    # def all_superuser(self):
    #     return self._create_user(is_superuser=True)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)  # только если ключа нет
        extra_fields.setdefault("is_superuser", True)  # только если ключа нет
        return self._create_user(email, password, **extra_fields)


