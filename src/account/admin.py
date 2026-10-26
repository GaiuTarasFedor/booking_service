from django.contrib import admin

from account.models import Barber, Client, User

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Barber)
