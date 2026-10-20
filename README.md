# Booking service — ДЗ №4 «Связи между моделями»

Учебный проект на Django: сервис барбершопа. В ветке `dev_1` реализовано ДЗ №4 — десять
моделей, связанных 1:1, 1:N и M:N, идемпотентное наполнение базы и десять запросов по связям.
ДЗ №1–№3 (страницы, модель `booking`, тесты) живут в ветках `dev` и `main`.

## Стек

Python 3.14, Django 6.1.1, PostgreSQL 18, Poetry, django-environ, psycopg 3,
django-extensions, `django.contrib.postgres`, Bootstrap 5 (CDN).

## Структура

```
src/
    manage.py
    core/                     — настройки, abstract BaseModel (created_at/updated_at)
    account/                  — User (AUTH_USER_MODEL), Client, Barber
    booking_manager/          — Barbershop, Booking, BookingService, Product,
                                ProductBooking, Comment, Promotion + команды
```

## Модели и таблицы

| Модель | Таблица | Назначение |
|---|---|---|
| `account.User` | `users` | `AbstractUser`, вход по email (`USERNAME_FIELD = "email"`, `REQUIRED_FIELDS = []`) |
| `account.Client` | `clients` | профиль клиента, 1:1 с пользователем; `status`, `date_of_birth` |
| `account.Barber` | `barbers` | профиль барбера, 1:1 с пользователем; филиал, опыт, рейтинг |
| `Barbershop` | `barbershops` | филиал: название, адрес, телефон, часы работы |
| `Booking` | `bookings` | бронь: клиент, барбер, услуга, филиал, время визита |
| `BookingService` | `booking_service` | услуга: категория, цена, длительность |
| `Product` | `product` | товар: название, цена, остаток |
| `ProductBooking` | `product_bookings` | строка «товар в брони», PK — UUID, `quantity`, `total_price` |
| `Comment` | `comments` | отзыв, 1:1 с бронью, автор-клиент и барбер, `rating` 1–5 |
| `Promotion` | `promotions` | акция: скидка, даты, M:N с услугами |

## Связи

| Связь | Тип | `on_delete` | Обращение |
|---|---|---|---|
| `User` – `Client` | 1:1 | CASCADE | `user.client` / `client.user` |
| `User` – `Barber` | 1:1 | CASCADE | `user.barber` / `barber.user` |
| `Barbershop` – `Barber` | 1:N | CASCADE | `barber.barbershop` / `shop.barbers` |
| `Client` – `Booking` | 1:N | CASCADE | `booking.client` / `client.bookings` |
| `Barber` – `Booking` | 1:N | CASCADE | `booking.barber` / `barber.bookings` |
| `BookingService` – `Booking` | 1:N | CASCADE | `booking.booking_service` / `service.bookings` |
| `Barbershop` – `Booking` | 1:N | CASCADE | `booking.barbershop` / `shop.bookings` |
| `Booking` – `Comment` | 1:1 | CASCADE | `comment.booking` / `booking.comment` |
| `Client` – `Comment` | 1:N | CASCADE | `comment.client` / `client.comments` |
| `Barber` – `Comment` | 1:N | CASCADE | `comment.barber` / `barber.comments` |
| `Booking` – `ProductBooking` | 1:N | CASCADE | `pb.booking` / `booking.product_bookings` |
| `Product` – `ProductBooking` | 1:N | CASCADE | `pb.product` / `product.product_bookings` |
| `Promotion` – `BookingService` | M:N | — | `promotion.services` / `service.promotions` |

Промежуточная таблица M:N — `promotions_services` (`promotion_id`, `bookingservice_id`).

## Миграции

| Файл | Что делает |
|---|---|
| `account/0001_initial` | `User`, `Client`, `Barber` без межприложенческих FK |
| `account/0002_initial` | FK `barbershop` у `Barber`, FK `user` у `Barber` и `Client` |
| `account/0003_rename_barber_shop_barber_barbershop` | переименование поля `barber_shop` → `barbershop` |
| `booking_manager/0001_initial` | семь моделей, M2M, `CHECK`-ограничения на цены |
| `0002_alter_booking_booking_service` | `booking_service` у брони обязателен (`NOT NULL`) |
| `0003_..._and_more` | `category` → `varchar(10)`, `rating` → `smallint`, `comment.client` → `NOT NULL`, удаление M2M `product.bookings`, `ALTER TABLE barber_shops RENAME TO barbershops` |
| `0004_alter_booking_barbershop` | `barbershop` у брони обязателен, `on_delete=CASCADE` |

## Данные

Наполнение — идемпотентная команда `seed_hw4` (`update_or_create` по естественным ключам,
всё внутри `transaction.atomic`): повторный запуск не создаёт дубликатов и приводит значения
к матрице. Текущее состояние (`manage.py report_state`):

| Таблица | Строк |
|---|---|
| `users` | 16 (15 из seed + суперпользователь `admin@admin.com`) |
| `clients` / `barbers` | 8 / 8 (один пользователь `barberclient@example.com` в обеих ролях) |
| `barbershops` | 2 (все барберы в «ДРОВОСЕК», «ОГОНЁК» без барберов) |
| `booking_service` / `product` / `promotions` | 8 / 8 / 3 |
| `promotions_services` | 4 |
| `bookings` / `comments` / `product_bookings` | 8 / 8 / 6 |

Данные спроектированы под границы запросов, а не «просто чтобы были»:

- у клиента с `pk=2` две брони, у клиента с `pk=3` два комментария (З1, З4);
- один барбер без комментариев (З3 даёт 7 из 8), один филиал без барберов (З5 даёт 1 из 2);
- услуга «Бородач» входит только в неактивную акцию (З6), две брони вообще без товаров (З2);
- оценки 5, 4, 3 и 2; клиент с оценкой 5 имеет две брони (З7), оценка ровно 3 не проходит `__lt=3` (З9);
- клиенты со статусами `noob`, `midl`, `expert`, `legenda` (З8);
- товар «Шампунь» есть в бронях барберов с опытом 5 и ровно 3 — второе не проходит `__gt=3` (З10).

## Команды

| Команда | Что делает |
|---|---|
| `manage.py seed_hw4` | Наполняет базу справочниками, пользователями, клиентами, барберами, бронями, комментариями и товарами в бронях. Идемпотентна |
| `manage.py report_state` | Печатает количество строк по десяти моделям |
| `manage.py hw4_queries` | Печатает З1–З10: SQL запроса и количество строк |

## Запросы З1–З10

| № | Условие | Приём | Результат |
|---|---|---|---|
| З1 | брони клиента с ID = 2 | `filter(client_id=2)` | 2 |
| З2 | брони, у которых есть хотя бы один товар | `filter(product_bookings__isnull=False).distinct()` | 5 |
| З3 | барберы, у которых есть хотя бы один комментарий | `filter(comments__isnull=False).distinct()` | 7 |
| З4 | комментарии клиента с ID = 3 | `Comment.objects.filter(client_id=3)` | 2 |
| З5 | барбершопы, где работает хотя бы один барбер | `filter(barbers__isnull=False).distinct()` | 1 |
| З6 | услуги, на которые действует хотя бы одна активная акция | `filter(promotions__is_active=True).distinct()` | 2 |
| З7 | брони клиентов, оставивших комментарий с оценкой 5 | `filter(client__comments__rating=5).distinct()` | 4 |
| З8 | товары из броней клиентов со статусом `noob` | `filter(product_bookings__booking__client__status="noob").distinct()` | 2 |
| З9 | услуги, бронированные клиентами с оценкой ниже 3 | `filter(bookings__client__comments__rating__lt=3).distinct()` | 2 |
| З10 | брони с товаром «Шампунь» у барбера с опытом больше 3 лет | `filter(product_bookings__product__name="Шампунь", barber__experience_year__gt=3).distinct()` | 2 |

`distinct()` нужен там, где JOIN по обратной связи размножает строки: у барбера с двумя
комментариями без него получилось бы две одинаковые строки барбера.

## Запуск с нуля

1. `git clone <repo> && cd booking_service`
2. `poetry install`
3. `cp .env.example .env` и заполнить `SECRET_KEY`, `PG_NAME`, `PG_USER`, `PG_PASS`, `PG_HOST`,
   `PG_PORT`, `DEBUG`, `ALLOWED_HOSTS`.
4. Создать роль и базу PostgreSQL:
   ```sql
   CREATE ROLE booking_service_user LOGIN PASSWORD '...';
   CREATE DATABASE booking_service_db OWNER booking_service_user;
   ```
5. `poetry run python src/manage.py migrate`
6. `poetry run python src/manage.py seed_hw4`
7. `poetry run python src/manage.py createsuperuser`
8. `poetry run python src/manage.py runserver` → http://127.0.0.1:8000/ и `/admin/`

## Проверка состояния

```bash
poetry run python src/manage.py check                     # System check identified no issues
poetry run python src/manage.py makemigrations --dry-run  # No changes detected
poetry run python src/manage.py report_state              # 16 / 8 / 8 / 2 / 8 / 3 / 8 / 8 / 8 / 6
poetry run python src/manage.py hw4_queries               # 2, 5, 7, 2, 1, 2, 4, 2, 2, 2
```

## Ограничения и примечания

- Тестов для ДЗ №4 нет: задание их не требует. Тесты ДЗ №3 остались в ветках `dev`/`main`.
- Веб-страницы (`/`, `/services/`, `/specialists/`, `/bookings/`) работают на демонстрационных
  данных из `data.py` и с базой не связаны.
- `seed_hw4` передаёт `visit_time` строками, поэтому при каждом прогоне Django пишет
  `RuntimeWarning: ... received a naive datetime while time zone support is active`. На данные не
  влияет; лечится передачей aware-datetime (`timezone.make_aware`).
- Пароли seed-пользователей лежат в команде открытым текстом — это учебный стенд, не продакшен.
- `ProductBooking.id` — `UUIDField` вместо `BigAutoField` с диаграммы: сделано осознанно, чтобы
  отработать нестандартный первичный ключ.
- M2M `Product.bookings` не используется: связь товара и брони выражена через `ProductBooking`.
