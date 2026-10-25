
# from .models import Booking
# from .management.commands.seed_bookings import BOOKINGS

#
# class BookingUpdateDeleteTest(TestCase):
#     """Тесты update() и delete() на QuerySet."""
#
#     def setUp(self):
#         """Создаёт чистые 10 записей перед каждым тестом."""
#         for data in BOOKINGS:
#             Booking.objects.create(**data)
#
#     def test_update_price_by_category(self):
#         """Пункт 11: filter(category='haircut').update(price=120)."""
#         before_count = Booking.objects.filter(category="haircut").count()
#         self.assertGreater(before_count, 0, "Нет записей с category=haircut")
#
#         updated_rows = Booking.objects.filter(category="haircut").update(price=120)
#
#         self.assertEqual(updated_rows, before_count, "update затронул не все haircut")
#
#         for b in Booking.objects.filter(category="haircut"):
#             self.assertEqual(b.price, Decimal("120"), f"Цена {b.name} не обновилась")
#
#     def test_deactivate_expensive(self):
#         """Пункт 12: filter(price__gt=200).update(is_active=False)."""
#         expensive = Booking.objects.get(name="Полный уход")
#         self.assertTrue(expensive.is_active, "Дорогая запись должна быть активна до update")
#
#         updated_rows = Booking.objects.filter(price__gt=200).update(is_active=False)
#         self.assertGreater(updated_rows, 0, "update не затронул ни одной записи")
#
#         expensive.refresh_from_db()
#         self.assertFalse(expensive.is_active, "Дорогая запись не стала неактивной")
#
#     def test_deactivate_no_visit_time(self):
#         """Пункт 13: filter(visit_time__isnull=True).update(is_active=False)."""
#         null_with_active = Booking.objects.filter(
#             visit_time__isnull=True, is_active=True
#         )
#         self.assertTrue(
#             null_with_active.exists(),
#             "Нет записей без visit_time и с is_active=True",
#         )
#
#         Booking.objects.filter(visit_time__isnull=True).update(is_active=False)
#
#         remaining = Booking.objects.filter(visit_time__isnull=True, is_active=True).count()
#         self.assertEqual(remaining, 0, "Остались активные записи без visit_time")
#
#     def test_delete_inactive_cheap(self):
#         """Пункт 14: filter(is_active=False, price__lt=20).delete()."""
#         target = Booking.objects.get(name="Бритье на лысо")
#         self.assertFalse(target.is_active, "Целевая запись должна быть неактивна")
#         self.assertLess(target.price, Decimal("20"), "Целевая запись должна быть дешёвой")
#
#         deleted_count, _ = Booking.objects.filter(
#             is_active=False, price__lt=20
#         ).delete()
#
#         self.assertGreater(deleted_count, 0, "delete не удалил ни одной записи")
#
#         self.assertFalse(
#             Booking.objects.filter(name="Бритье на лысо").exists(),
#             "Запись «Бритье на лысо» не удалена",
#         )
