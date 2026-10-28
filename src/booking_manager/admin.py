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
    pass


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
