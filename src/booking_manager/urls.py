"""booking_manager URL Configuration"""

from django.urls import path

from . import views

app_name = "booking_manager"

urlpatterns = [
    path("", views.index, name="index"),
    path("slots/", views.slot_list, name="slot_list")
]