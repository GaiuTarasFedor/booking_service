from django.contrib import admin

from account.models import Barber, Client, User
from booking_manager.models import Comment


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["client", "text", "rating", "is_published"]
    extra = 0

    def has_add_permission(self, request, obj):
        return False


class BarberAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(User)
admin.site.register(Client)
admin.site.register(Barber, BarberAdmin)
