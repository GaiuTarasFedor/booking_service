"""
Представления сервиса бронирования.

Каждое представление принимает HttpRequest и возвращает HttpResponse.
"""
from django.db.models.query import Prefetch
from django.shortcuts import render

from account.models import Barber
from .data import SERVICES
from booking_manager.models import Booking, Comment


def home(request):
    """Главная страница: что это за сервис и какую задачу он решает."""
    return render(request, "booking_manager/home.html")


def service_list(request):
    """Список доступных услуг."""
    return render(request, "booking_manager/services.html", {"services": SERVICES})


def specialist_list(request):
    """Список специалистов, их рейтинг и комментаррии."""
    barbers = Barber.objects.select_related("user").prefetch_related(
        Prefetch(
        "comments", queryset=Comment.objects.select_related("client__user"))
    )
    return render(
        request, "booking_manager/specialists.html", {"barbers": barbers}
    )


def booking_list(request):
    """Список бронирований, осуществленных клиентами."""
    bookings = Booking.objects.select_related("client__user", "barber__user", "booking_service")
    return render(request, "booking_manager/bookings.html", {"bookings": bookings})


def booking_new(request):
    """Страница создания нового бронирования."""
    return render(
        request,
        "booking_manager/booking_new.html",
    )
