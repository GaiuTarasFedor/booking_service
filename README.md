# Booking service — ДЗ №5 «Наследование моделей, оптимизация запросов, генерация данных»

Учебный проект на Django: сервис барбершопа. В ветке `dev_1` последовательно сделаны ДЗ №4 и №5.

Что добавлено в ДЗ №5:

- абстрактная модель `RatingMixin` в `core` — одно поле `rating` для `Barber` и `Comment`;
- `django-debug-toolbar`: SQL-панель и `EXPLAIN` для разбора запросов;
- три страницы на ORM: список броней, список барберов с отзывами, детали брони по ID;
- оптимизация запросов: `select_related`, `prefetch_related`, `Prefetch` с вложенным `select_related`;
- кастомный менеджер `Booking` с методом `upcoming_active()` — активные брони с будущим визитом;
- команда `generate_data` на `faker`: 100 пользователей, 15 барберов, 80 клиентов, 5 барбершопов,
  20 услуг, 50 товаров, 500 броней, 200 отзывов, 10 акций и товары в части броней.

ДЗ №4: десять моделей, связи 1:1, 1:N и M:N, идемпотентный seed и десять запросов по связям.
ДЗ №1–№3 (страницы, модель `booking`, тесты) живут в ветках `dev` и `main`.

## Стек

Python 3.14, Django 6.1.1, PostgreSQL 18, Poetry, django-environ, psycopg 3,
django-extensions, `django.contrib.postgres`, `faker` (локаль `ru_RU`), `django-debug-toolbar`,
`ruff`, Bootstrap 5 (CDN).

## Структура

```
src/
    manage.py
    core/                     — настройки, abstract BaseModel (created_at/updated_at),
                                abstract RatingMixin (rating)
    account/                  — User (AUTH_USER_MODEL), Client, Barber
    booking_manager/          — Barbershop, Booking, BookingService, Product,
                                ProductBooking, Comment, Promotion
                                managers.py  — BookingManager.upcoming_active()
                                management/commands/  — seed_hw4, generate_data,
                                                        report_state, hw4_queries
                                templates/booking_manager/  — base, home, services, specialists,
                                                              bookings, booking_detail, booking_new
```

## Модели и таблицы

| Модель | Таблица | Назначение |
|---|---|---|
| `account.User` | `users` | `AbstractUser`, вход по email (`USERNAME_FIELD = "email"`, `REQUIRED_FIELDS = []`) |
| `account.Client` | `clients` | профиль клиента, 1:1 с пользователем; `status`, `date_of_birth` |
| `account.Barber` | `barbers` | профиль барбера, 1:1 с пользователем; филиал, опыт, `rating` из `RatingMixin` |
| `Barbershop` | `barbershops` | филиал: название, адрес, телефон, часы работы |
| `Booking` | `bookings` | бронь: клиент, барбер, услуга, филиал, время визита |
| `BookingService` | `booking_service` | услуга: категория, цена, длительность |
| `Product` | `product` | товар: название, цена, остаток |
| `ProductBooking` | `product_bookings` | строка «товар в брони», PK — UUID, `quantity`, `total_price` |
| `Comment` | `comments` | отзыв, 1:1 с бронью, автор-клиент и барбер, `rating` из `RatingMixin` |
| `Promotion` | `promotions` | акция: скидка, даты, M:N с услугами |

Рейтинг приходит из абстрактной модели `core.RatingMixin` (`PositiveSmallIntegerField`,
`null=True`): в таблицах `barbers` и `comments` это `smallint`, отдельного поля в моделях нет.

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
| `account/0004_alter_barber_rating` | `rating` у `Barber` стал `smallint` после перехода на `RatingMixin` |

## Данные

Две идемпотентные команды, у них разные задачи.

**`seed_hw4`** — небольшие данные, спроектированные под границы запросов З1–З10
(`update_or_create` по естественным ключам, всё внутри `transaction.atomic`): 8 клиентов,
8 барберов, 8 броней, 8 отзывов, 8 товаров, 3 акции (в `promotions_services` 4 строки),
2 барбершопа. Один пользователь `barberclient@example.com` состоит в обеих ролях; одна услуга
входит только в неактивную акцию; у одного барбера нет отзывов; у двух броней нет товаров.
Именно это обеспечивает ожидаемые числа З1–З10.

**`generate_data`** — объёмы из ДЗ №5, собранные из констант и `faker` с фиксированным seed:
5 барбершопов, 20 услуг, 50 товаров, 10 акций, 100 пользователей, 15 барберов, 80 клиентов,
500 броней, 200 отзывов и 200 позиций товаров. Ключи идемпотентности: `name` у справочников,
`email` у пользователей, `user` у барберов и клиентов, `booking` у отзывов, пара
«бронь + товар» у позиций. Повторный прогон ничего не создаёт.

Текущее состояние после `seed_hw4` и `generate_data` (`manage.py report_state`):

| Таблица | Строк |
|---|---|
| `users` | 116 (15 из seed + 100 сгенерированных + суперпользователь) |
| `clients` / `barbers` | 88 / 23 |
| `barbershops` | 7 |
| `booking_service` / `product` / `promotions` | 28 / 58 / 13 |
| `bookings` / `comments` / `product_bookings` | 508 / 208 / 206 |

Числа зависят от того, какие команды запускались: `generate_data` добавляет к тому, что уже есть.
На чистой базе после одного `seed_hw4` состояние соответствует таблице из ДЗ №4:
16 / 8 / 8 / 2 / 8 / 3 / 8 / 8 / 8 / 6.

## Команды

| Команда | Что делает |
|---|---|
| `manage.py seed_hw4` | Наполняет базу справочниками, пользователями, клиентами, барберами, бронями, комментариями и товарами в бронях. Идемпотентна |
| `manage.py report_state` | Печатает количество строк по десяти моделям |
| `manage.py hw4_queries` | Печатает З1–З10: SQL запроса и количество строк |
| `manage.py generate_data` | Наполняет базу объёмами ДЗ №5: 100 пользователей, 15 барберов, 80 клиентов, 5 барбершопов, 20 услуг, 50 товаров, 500 броней, 200 отзывов, 10 акций, товары в части броней. Идемпотентна |

## Страницы

| URL | Что показывает | Запросы |
|---|---|---|
| `/` | главная | шаблон |
| `/services/` | список услуг | демонстрационный `data.py` |
| `/specialists/` | барберы: имя, опыт, отзывы с авторами | `select_related("user")` + `Prefetch("comments", queryset=Comment.objects.select_related("client__user"))` |
| `/bookings/` | брони: клиент, барбер, услуга, время | `select_related("client__user", "barber__user", "booking_service")` |
| `/bookings/<id>/` | детали брони и товары с количеством | `select_related(...)` + `Prefetch("product_bookings", queryset=ProductBooking.objects.select_related("product"))` |
| `/bookings/new/` | форма новой брони (заглушка) | шаблон |

На будущие визиты ссылается кнопка `View` в списке броней: адрес строится тегом `{% url %}` с `pk`
текущей карточки. Несуществующий id даёт 404.

## Оптимизация запросов

- `select_related` — для однозначных связей (FK и `OneToOne`, включая обратный `OneToOne`):
  `Booking.client__user`, `Barber.user`, `ProductBooking.product`. Один запрос с `JOIN`.
- `prefetch_related` — для коллекций (`Barber.comments`, `Booking.product_bookings`):
  отдельный запрос `WHERE ... IN (...)`, склейка в Python.
- `Prefetch(queryset=...)` — когда внутри коллекции нужны ещё связи:
  `Prefetch("comments", queryset=Comment.objects.select_related("client__user"))`.
- Без `select_related` те же страницы дают N+1: один запрос на список плюс запросы на каждую строку.

## Менеджер `Booking`

```python
Booking.objects.upcoming_active()
```

Возвращает активные брони, время визита которых ещё не наступило: `is_active=True` и
`visit_time > now`. Метод лежит в `booking_manager/managers.py`, менеджер подключён в модели
строкой `objects = BookingManager()`. Пустое `visit_time` отсекается самим сравнением, поэтому
отдельное условие `isnull=False` не нужно.

## Debug toolbar

`django-debug-toolbar` подключён в `INSTALLED_APPS`, `MIDDLEWARE`, `core/urls.py`; в настройках
`INTERNAL_IPS = ["127.0.0.1"]`, `DEBUG=True` в `.env`. Панель видна только с локального адреса.
Вкладка `SQL` показывает запросы страницы и помечает дубликаты и «similar» (это профиль N+1);
кнопка `Expl` выполняет `EXPLAIN ANALYZE` выбранного запроса и показывает план.

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
7. `poetry run python src/manage.py generate_data` — объёмы ДЗ №5. Первый прогон занимает около двух
   минут: сто паролей хешируются намеренно медленно
8. `poetry run python src/manage.py createsuperuser`
9. `poetry run python src/manage.py runserver` → http://127.0.0.1:8000/ и `/admin/`

## Проверка состояния

```bash
poetry run python src/manage.py check                     # System check identified no issues
poetry run python src/manage.py makemigrations --dry-run  # No changes detected
poetry run python src/manage.py report_state              # 116 / 88 / 23 / 7 / 28 / 13 / 508 / 208 / 58 / 206
poetry run python src/manage.py shell -c "from booking_manager.models import Booking; print(Booking.objects.upcoming_active().count())"
```

`hw4_queries` печатает SQL и количества З1–З10. Эталон из ДЗ №4 (`2, 5, 7, 2, 1, 2, 4, 2, 2, 2`)
относится к состоянию после одного `seed_hw4`; после `generate_data` числа будут другими — набор
данных вырос, это ожидаемо.

## Ограничения и примечания

- Тестов для ДЗ №4–№5 нет: задания их не требуют. Тесты ДЗ №3 остались в ветках `dev`/`main`.
- `/services/` и `/bookings/new/` по-прежнему демонстрационные: данные берутся из `data.py`.
  Остальные страницы работают с базой.
- `seed_hw4` передаёт `visit_time` строками, поэтому при прогоне Django пишет
  `RuntimeWarning: ... received a naive datetime while time zone support is active`. На данные не
  влияет; лечится передачей aware-datetime.
- Пароли seed- и generate-пользователей лежат в коде открытым текстом — это учебный стенд,
  не продакшен.
- `ProductBooking.id` — `UUIDField` вместо `BigAutoField` с диаграммы: сделано осознанно, чтобы
  отработать нестандартный первичный ключ.
- M2M `Product.bookings` не используется: связь товара и брони выражена через `ProductBooking`.
- `generate_data` добавляет данные к существующим. Абсолютные числа задания (100 пользователей,
  15 барберов, 80 клиентов, 5 барбершопов, 20 услуг, 50 товаров, 500 броней, 200 отзывов, 10 акций)
  проверяются на чистой базе; на заполненной — по приросту через `report_state` до и после.
- На машине может быть несколько кластеров PostgreSQL с одинаковым именем базы. Перед работой
  полезно проверить, к какому подключено приложение:
  `select version(), current_database();`.
