# Booking service

Учебный проект на Django: сервис бронирования услуг (барбершоп).
Данные пока демонстрационные (в `data.py`), модели и работу с БД добавим позже.

## Стек
Python 3.14, Django 6.1, PostgreSQL 18, Poetry, django-environ, psycopg 3, Bootstrap 5 (CDN).

## Страницы
| Адрес | Имя маршрута | Назначение |
|---|---|---|
| `/` | `booking_manager:home` | Главная: hero-блок, описание, кнопка Book Now |
| `/services/` | `booking_manager:services` | Услуги (Bootstrap-карточки) |
| `/specialists/` | `booking_manager:specialists` | Специалисты (карточки) |
| `/bookings/` | `booking_manager:bookings` | Бронирования: badge статусов, кнопки View/Cancel |
| `/bookings/new/` | `booking_manager:booking_new` | Форма нового бронирования + карточка Booking Information |
| `/admin/` | `admin:index` | Админка Django |

## Структура
src/                — точка импорта (sys.path), а не корень репозитория
    manage.py
    core/            — конфигурация проекта (settings/urls/wsgi/asgi)
    booking_manager/  — приложение
        data.py       — демонстрационные данные: SERVICES, SPECIALISTS, BOOKINGS, TIME_SLOTS
        urls.py       — маршруты приложения (app_name = booking_manager)
        views.py      — представления (home, service_list, specialist_list, booking_list, booking_new)
        templates/booking_manager/
            base.html          — общий каркас: Bootstrap 5, {% block %}
            navbar.html        — навигация (подключён через {% include %})
            footer.html        — футер: проект, {% now "Y" %}, Contacts/About/Admin
            home.html          — главная страница
            services.html      — список услуг
            specialists.html   — список специалистов
            bookings.html      — список бронирований
            booking_new.html   — форма нового бронирования

## Запуск с нуля
1. git clone ... && cd booking_service
2. poetry install
3. cp .env.example .env  и заполнить значения
SECRET_KEY: poetry run python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
4. создать роль и базу PostgreSQL (команды CREATE ROLE / CREATE DATABASE)
5. poetry run python src/manage.py migrate
6. poetry run python src/manage.py createsuperuser
7. poetry run python src/manage.py runserver
   → http://127.0.0.1:8000/  и  /admin/

## Полезные команды
check, check --deploy, showmigrations, dbshell, diffsettings, changepassword
