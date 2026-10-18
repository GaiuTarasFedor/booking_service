# Booking service

Учебный проект на Django: сервис бронирования услуг барбершопа.

Модель `booking.py`, миграции и работа с PostgreSQL реализованы: данные наполняются командой
`seed_bookings`, запросы к БД демонстрирует команда `booking_queries`, мутации покрыты тестами.
Веб-страницы пока работают на демонстрационных данных из `data.py` и с базой не связаны —
их перевод на QuerySet запланирован отдельно.

## Стек

Python 3.14, Django 6.1.1, PostgreSQL 18, Poetry, django-environ, psycopg 3,
django-extensions, `django.contrib.postgres`, Bootstrap 5 (CDN).

## Модель данных

`booking_manager.Booking` → таблица `booking`.

| Поле | Тип | Колонка в PostgreSQL | Примечание |
|---|---|---|---|
| `id` | `BigAutoField` | `bigint`, primary key | создаётся Django автоматически |
| `name` | `CharField(max_length=50)` | `varchar(50)` | `unique=True`, наименование позиции прайса |
| `description` | `TextField(blank=True)` | `text` | `NOT NULL`, без ограничения длины |
| `price` | `DecimalField(8, 2)` | `numeric(8,2)` | `MinValueValidator(0)` + `CheckConstraint` |
| `category` | `CharField(max_length=10, choices=CategoryChoices)` | `varchar(10)` | 8 значений, по умолчанию `haircut` |
| `is_active` | `BooleanField(default=True)` | `boolean` | |
| `visit_time` | `DateTimeField(null=True, blank=True)` | `timestamp with time zone` | единственное поле с `NULL` |
| `created_at` | `DateTimeField(auto_now_add=True)` | `timestamp with time zone` | только при вставке |
| `updated_at` | `DateTimeField(auto_now=True)` | `timestamp with time zone` | при каждом сохранении |

Целостность на уровне БД:

- `CHECK (price >= 0)` — ограничение `price_non_negative`;
- `UNIQUE (name)`;
- индекс `varchar_pattern_ops` на `name` — Django добавляет его сам для `unique`-поля типа `varchar`.

Категории (`booking_manager/constants.py`, `CategoryChoices`): `kids`, `moustache`, `beard`,
`haircut`, `camouflage`, `royal`, `shave`, `combo`. В БД хранится `value`, в интерфейсе
показывается `label`.

`Meta`: `db_table = "booking"`, `ordering = ["-created_at", "id"]` (детерминированный порядок —
`id` как тай-брейкер), `verbose_name` / `verbose_name_plural` на русском.

## Страницы

Данные для страниц берутся из `data.py`, а не из БД.

| Адрес | Имя маршрута | Назначение |
|---|---|---|
| `/` | `booking_manager:home` | Главная: hero-блок, описание, кнопка Book Now |
| `/services/` | `booking_manager:services` | Услуги (Bootstrap-карточки) |
| `/specialists/` | `booking_manager:specialists` | Специалисты (карточки) |
| `/bookings/` | `booking_manager:bookings` | Бронирования: badge статусов, кнопки View/Cancel |
| `/bookings/new/` | `booking_manager:booking_new` | Форма нового бронирования (только разметка) |
| `/admin/` | `admin:index` | Админка Django, модель `booking.py` зарегистрирована |

## Структура

```
src/                          — точка импорта (sys.path), а не корень репозитория
    manage.py
    core/                     — конфигурация проекта
        settings.py  urls.py  wsgi.py  asgi.py
    booking_manager/          — приложение
        constants.py          — CategoryChoices (TextChoices, 8 значений)
        models/
            __init__.py       — from .booking import Booking
            booking.py        — модель Booking
        migrations/
            0001_initial.py   — создана Django, вручную не правится
        admin.py              — BookingAdmin: list_display, list_filter, search_fields
        management/commands/
            seed_bookings.py    — наполняет таблицу 10 записями (идемпотентно)
            booking_queries.py  — демонстрация запросов, пункты 2–10
        tests.py              — пункты 11–14: update() и delete()
        data.py               — демонстрационные данные для страниц (SERVICES, SPECIALISTS,
                                BOOKINGS, TIME_SLOTS); с БД не связаны
        urls.py               — маршруты приложения (app_name = booking_manager)
        views.py              — home, service_list, specialist_list, booking_list, booking_new
        templates/booking_manager/
            base.html          — общий каркас: Bootstrap 5, {% block %}
            navbar.html        — навигация ({% include %})
            footer.html        — футер: {% now "Y" %}, Contacts/About/Admin
            home.html          — главная страница
            services.html      — список услуг
            specialists.html   — список специалистов
            bookings.html      — список бронирований
            booking_new.html   — форма нового бронирования
```

## Запуск с нуля

1. `git clone <repo> && cd booking_service`
2. `poetry install`
3. `cp .env.example .env` и заполнить значения. Переменные: `SECRET_KEY`, `PG_NAME`, `PG_USER`,
   `PG_PASS`, `PG_HOST`, `PG_PORT`, `DEBUG`, `ALLOWED_HOSTS`.

   Сгенерировать `SECRET_KEY`:
   ```bash
   poetry run python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
   ```
4. Создать роль и базу PostgreSQL:
   ```sql
   CREATE ROLE booking_service_user LOGIN PASSWORD '...';
   CREATE DATABASE booking_service_db OWNER booking_service_user;
   ```
   Для запуска тестов роли нужно право `CREATEDB` — Django создаёт отдельную базу
   `test_booking_service_db`:
   ```bash
   sudo -u postgres psql -c "ALTER ROLE booking_service_user CREATEDB;"
   ```
5. `poetry run python src/manage.py migrate`
6. Наполнить таблицу: `poetry run python src/manage.py seed_bookings`
7. `poetry run python src/manage.py createsuperuser`
8. `poetry run python src/manage.py runserver` → http://127.0.0.1:8000/ и `/admin/`

## Команды проекта

| Команда | Что делает |
|---|---|
| `manage.py seed_bookings` | Создаёт 10 записей через `get_or_create` по `name`. Идемпотентна: повторный запуск не создаёт дубликатов |
| `manage.py booking_queries` | Печатает пункты 2–10: заголовок, записи, количество и SQL каждого запроса |
| `manage.py test booking_manager` | Пункты 11–14 (`update` / `delete`). Идёт против отдельной тестовой БД, рабочая не затрагивается |

Мутации намеренно вынесены в тесты, а не в management-команду: каждый тест-метод выполняется
в откатываемой транзакции, поэтому операции не мешают друг другу. При последовательном
выполнении в одной базе пункт 11 меняет цены категории `haircut`, после чего пункт 14
находит не те записи.

## Полезные команды Django

`check`, `check --deploy`, `makemigrations --dry-run`, `sqlmigrate`, `showmigrations`,
`dbshell`, `diffsettings`, `changepassword`, `show_urls` (django-extensions).

## Проверка состояния

```bash
poetry run python src/manage.py check                     # 0 issues
poetry run python src/manage.py makemigrations --dry-run  # No changes detected
poetry run python src/manage.py test booking_manager -v 2 # Ran 4 tests ... OK
poetry run python src/manage.py dbshell                   # \d booking
```

## Примечания

- `TIME_ZONE = "UTC"` при `USE_TZ = True`. В коде используются только `timezone.localdate()`
  и `timezone.now()`; `date.today()` и `datetime.now()` дают расхождение с локальной датой.
- Повторный запуск `seed_bookings` на следующий день не обновляет `created_at` у существующих
  записей (`get_or_create` их только находит, а `auto_now_add` срабатывает при вставке).
  На чистой базе команда отрабатывает корректно.
- Тесты с кириллицей в `icontains` / `istartswith` должны идти против PostgreSQL: в SQLite
  приведение регистра работает только для ASCII.
