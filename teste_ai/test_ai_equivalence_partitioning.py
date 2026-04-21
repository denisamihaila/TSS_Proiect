"""AI-generated equivalence partitioning tests.

This file mirrors the manually written equivalence-partitioning suite, but it
targets the isolated AI copy from ``teste_ai/fitness_class_booking.py``.
"""

import unittest

from teste_ai.fitness_class_booking import FitnessClassBooking


class TestAIEquivalencePartitioning(unittest.TestCase):
    """Representative valid and invalid partitions for each public method."""

    def setUp(self) -> None:
        self.booking = FitnessClassBooking("yoga", "Ana Pop", 5, 10.0)

    def test_ai_init_valid_yoga_class_creates_object(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(b.class_name, "yoga")

    def test_ai_init_valid_dance_class_creates_object(self) -> None:
        b = FitnessClassBooking("dance", "Instructor", 5, 10.0)
        self.assertEqual(b.class_name, "dance")

    def test_ai_init_valid_pilates_class_creates_object(self) -> None:
        b = FitnessClassBooking("pilates", "Instructor", 5, 10.0)
        self.assertEqual(b.class_name, "pilates")

    def test_ai_init_valid_zumba_class_creates_object(self) -> None:
        b = FitnessClassBooking("zumba", "Instructor", 5, 10.0)
        self.assertEqual(b.class_name, "zumba")

    def test_ai_init_invalid_unknown_class_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("crossfit", "Instructor", 5, 10.0)

    def test_ai_init_invalid_empty_class_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("", "Instructor", 5, 10.0)

    def test_ai_init_invalid_uppercase_class_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("YOGA", "Instructor", 5, 10.0)

    def test_ai_init_valid_instructor_is_trimmed(self) -> None:
        b = FitnessClassBooking("yoga", "  Ana Pop  ", 5, 10.0)
        self.assertEqual(b.instructor, "Ana Pop")

    def test_ai_init_empty_instructor_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "", 5, 10.0)

    def test_ai_init_whitespace_instructor_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "   ", 5, 10.0)

    def test_ai_init_non_string_instructor_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", 123, 5, 10.0)

    def test_ai_init_valid_max_spots_mid_range(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 15, 10.0)
        self.assertEqual(b.max_spots, 15)

    def test_ai_init_max_spots_zero_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 0, 10.0)

    def test_ai_init_max_spots_over_limit_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 31, 10.0)

    def test_ai_init_max_spots_float_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 1.0, 10.0)

    def test_ai_init_max_spots_true_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", True, 10.0)

    def test_ai_init_max_spots_false_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", False, 10.0)

    def test_ai_init_valid_integer_price_is_converted_to_float(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 5, 12)
        self.assertEqual(b.price_per_session, 12.0)

    def test_ai_init_valid_float_price_is_kept(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 5, 12.5)
        self.assertEqual(b.price_per_session, 12.5)

    def test_ai_init_zero_price_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, 0.0)

    def test_ai_init_negative_price_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, -1.0)

    def test_ai_init_string_price_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, "10")

    def test_ai_init_true_price_raises_value_error_in_ai_copy(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, True)

    def test_ai_init_false_price_raises_value_error_in_ai_copy(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, False)

    def test_ai_book_spot_valid_client_is_confirmed(self) -> None:
        self.assertEqual(self.booking.book_spot("Alice"), "confirmed")
        self.assertEqual(self.booking._confirmed, ["Alice"])

    def test_ai_book_spot_strips_valid_client_name(self) -> None:
        self.assertEqual(self.booking.book_spot("  Alice  "), "confirmed")
        self.assertEqual(self.booking._confirmed, ["Alice"])

    def test_ai_book_spot_empty_client_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.book_spot("")

    def test_ai_book_spot_non_string_client_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.book_spot(123)

    def test_ai_book_spot_full_class_adds_to_waitlist(self) -> None:
        for idx in range(5):
            self.booking.book_spot(f"C{idx}")
        self.assertEqual(self.booking.book_spot("Waiting"), "waitlist")

    def test_ai_book_spot_full_waitlist_rejects_client(self) -> None:
        for idx in range(5):
            self.booking.book_spot(f"C{idx}")
        for idx in range(5):
            self.booking.book_spot(f"W{idx}")
        self.assertEqual(self.booking.book_spot("Overflow"), "rejected")

    def test_ai_cancel_confirmed_client_returns_true(self) -> None:
        self.booking.book_spot("Alice")
        self.assertTrue(self.booking.cancel_booking("Alice"))
        self.assertEqual(self.booking.booked_spots, 0)

    def test_ai_cancel_waitlist_client_returns_true(self) -> None:
        for idx in range(5):
            self.booking.book_spot(f"C{idx}")
        self.booking.book_spot("Waiting")
        self.assertTrue(self.booking.cancel_booking("Waiting"))
        self.assertNotIn("Waiting", self.booking.waitlist)

    def test_ai_cancel_unknown_client_returns_false(self) -> None:
        self.assertFalse(self.booking.cancel_booking("Ghost"))

    def test_ai_cancel_none_client_returns_false(self) -> None:
        self.assertFalse(self.booking.cancel_booking(None))

    def test_ai_calculate_cost_no_membership(self) -> None:
        self.assertEqual(self.booking.calculate_cost(5, False), 50.0)

    def test_ai_calculate_cost_membership_discount(self) -> None:
        self.assertEqual(self.booking.calculate_cost(5, True), 40.0)

    def test_ai_calculate_cost_volume_discount(self) -> None:
        self.assertEqual(self.booking.calculate_cost(10, False), 90.0)

    def test_ai_calculate_cost_both_discounts(self) -> None:
        self.assertEqual(self.booking.calculate_cost(10, True), 70.0)

    def test_ai_calculate_cost_zero_sessions_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.calculate_cost(0, False)

    def test_ai_calculate_cost_over_limit_sessions_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.calculate_cost(21, False)

    def test_ai_calculate_cost_string_sessions_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.calculate_cost("5", False)

    def test_ai_calculate_cost_bool_sessions_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.calculate_cost(True, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
