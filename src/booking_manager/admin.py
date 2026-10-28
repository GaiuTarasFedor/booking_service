from django.contrib import admin

from booking_manager.models import (
    Barbershop,
    Booking,
    BookingService,
    Comment,
    Product,
    ProductBooking,
    Promotion,
)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "visit_time", "created_at", "barber_email"]
    fields = ["name", "is_active", "visit_time", "booking_service", ("barber", "client")]
    list_filter = ["name", "is_active", "visit_time", "created_at"]
    list_per_page = 11

    @admin.display()
    def barber_email(self, obj):
        if obj.barber:
            return obj.barber.user.email


@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Barbershop)
class BarbershopAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductBooking)
class ProductBookingAdmin(admin.ModelAdmin):
    pass
