from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "price", "visit_time", "created_at"]
    list_filter = ["category", "visit_time", "is_active", "created_at"]
    search_fields = ["name",]
