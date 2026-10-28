from django.contrib import admin

from booking_manager.models import Booking


@admin.register(Booking)
class AuthorAdmin(admin.ModelAdmin):
    
    list_display = ["name", "is_active", "visit_time", "created_at", "barber_email"]
    fields = ["name", "is_active", "visit_time", "booking_service", ("barber", "client")]
    list_filter = ["name", "is_active", "visit_time", "created_at"]
    list_per_page = 11

    @admin.display()
    def barber_email(self, obj):
        if obj.barber:
            return obj.barber.user. email

