# Booking service
Сервис бронирования свободных временных слотов.

## Стек
Python 3.14, Django 6.1, PostgreSQL 18, Poetry, django-environ, psycopg 3.

## Структура
src/                — точка импорта (sys.path), а не корень репозитория
    manage.py
    core/            — конфигурация проекта (settings/urls/wsgi/asgi)
    booking_manager/  — приложение: маршруты, представления, шаблоны

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
