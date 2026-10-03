"""
Представления сервиса бронирования.

Каждое представление принимает HttpRequest и возвращает HttpResponse.
"""
from django.shortcuts import render

from .data import SERVICES, SPECIALISTS, BOOKINGS, TIME_SLOTS


def home(request):
    """Главная страница: что это за сервис и какую задачу он решает."""
    return render(request, "booking_manager/home.html")


# def slot_list(request):
#     """Список доступных временных слотов.
#
#     Данные пока фиктивны: их источник заменится на модели в следующем шаге,
#       контракт контекста (ключи "slots" и "total") при этом не меняется.
#     """
#     slots = [
#         {"start": "09:00", "end": "10:00", "service": "Консультация", "is_free": True},
#         {"start": "10:00", "end": "11:00", "service": "Бронь стола", "is_free": False},
#         {"start": "11:00", "end": "12:00", "service": "Экскурсия", "is_free": True},
#     ]
#     return render(
#         request,
#         "booking_manager/slots.html",
#         {"slots": slots, "total": len(slots)},
#     )


def service_list(request):
    """Список доступных услуг."""
    return render(
        request,
        "booking_manager/services.html",
        {"services": SERVICES}
    )


def specialist_list(request):
    """Список специалистов."""
    return render(
        request,
        "booking_manager/specialists.html",
        {"specialists": SPECIALISTS}
    )


def booking_list(request):
    """Запись клиентов."""
    return render(
        request,
        "booking_manager/bookings.html",
        {"bookings": BOOKINGS}
    )


def booking_new(request):
    """Страница создания нового бронирования."""
    return render(
        request,
        "booking_manager/booking_new.html",
    )