from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="дата обновления",
    )

    class Meta:
        abstract = True


class RatingMixin(models.Model):
    rating = models.PositiveSmallIntegerField(
        verbose_name="рейтинг",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
