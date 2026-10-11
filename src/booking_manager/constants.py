from django.db import models


class CategoryChoices(models.TextChoices):
    # названия удлинил для читаемости кода - услуги
    SERVICE_KIDS = "kids", "детская стрижка"
    SERVICE_MOUSTACHE = "moustache", "усы"
    SERVICE_BEARD = "beard", "стрижка бороды"
    SERVICE_HAIRCUT = "haircut", "мужская стрижка"
    SERVICE_CAMOUFLAGE = "camouflage", "камуфляж седины"
    SERVICE_ROYAL = "royal", "королевское бритье"
    SERVICE_SHAVE = "shave", "бритье опасной бритвой"
    SERVICE_COMBO = "combo", "стрижка + борода"
