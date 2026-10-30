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
    """Описывает бронирование в админке."""

    list_display = [
        "name",
        "visit_time",
        "is_active",
        "barber",
        "client",
        "booking_service",
        "castom_booking",
    ]
    list_select_related = ("barber__user", "client", "booking_service")
    list_display_links = ["name", "visit_time"]
    list_editable = ["is_active"]

    @admin.display(description="Барбер на бронировании", ordering="barber__user__first_name")
    def castom_booking(self, obj):
        return f"{obj.name}: {obj.barber.user.get_full_name() or obj.barber.user.email}"


@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Barbershop)
class BarbershopAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "amount", "description"]
    list_editable = ["price", "amount"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductBooking)
class ProductBookingAdmin(admin.ModelAdmin):
    pass
