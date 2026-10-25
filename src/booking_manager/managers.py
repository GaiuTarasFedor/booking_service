from django.db import models
from django.utils import timezone


class BookingManager(models.Manager):
    """Расширяем базовый object queryset Django."""

    def upcoming_active(self):
        return self.get_queryset().filter(is_active=True, visit_time__gt=timezone.now())