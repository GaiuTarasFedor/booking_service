from django.contrib import admin
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce

from booking_manager.models import (
    Barbershop,
    Booking,
    BookingService,
    Comment,
    Product,
    ProductBooking,
    Promotion,
)


class ProductBookingInline(admin.TabularInline):
    model = ProductBooking
    fields = ["product", "quantity", "total_price"]
    extra = 0


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
    inlines = [
        ProductBookingInline,
    ]
    list_select_related = ("barber__user", "client", "booking_service")
    list_display_links = ["name", "visit_time"]
    list_editable = ["is_active"]
    readonly_fields = ["created_at", "sum_products_booking"]
    search_fields = [
        "name",
        "client__user__email",
        "barber__user__first_name",
        "barber__user__last_name",
    ]
    list_filter = ["is_active", "visit_time", "barber", "booking_service"]

    @admin.display(description="Барбер на бронировании", ordering="barber__user__first_name")
    def castom_booking(self, obj):
        return f"{obj.name}: {obj.barber.user.get_full_name() or obj.barber.user.email}"

    @admin.display(description="Общая цена товаров в брони")
    def sum_products_booking(self, obj):
        total_price = obj.product_bookings.aggregate(total=Sum("total_price"))["total"] or 0
        return f"{total_price} ₽"


@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]


@admin.register(Barbershop)
class BarbershopAdmin(admin.ModelAdmin):
    list_display = ["name", "address"]
    search_fields = ["name", "address"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "amount", "description"]
    list_editable = ["price", "amount"]
    search_fields = [
        "name",
    ]
    actions = [
        "add_product_amount",
    ]

    @admin.action(description="увеличить количество на 10")
    def add_product_amount(self, request, queryset):
        queryset.update(amount=Coalesce(F("amount"), Value(0)) + 10)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ["rating", "is_published"]
    actions = ["comments_true", "comments_false"]

    @admin.action(description="опубликовать комментарии")
    def comments_true(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="скрыть комментарии")
    def comments_false(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "is_active"]
    actions = ["promo_true", "promo_false"]

    @admin.action(description="активировать акции")
    def promo_true(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="деактивировать акции")
    def promo_false(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(ProductBooking)
class ProductBookingAdmin(admin.ModelAdmin):
    pass
