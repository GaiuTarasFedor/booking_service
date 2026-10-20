from django.db import models


class ClientStatusChoices(models.TextChoices):
    NOOB = "noob", "новичок"
    MIDL = "midl", "ученик"
    EXPERT = "expert", "експерт"
    LEGENDA = "legenda", "легенда"

