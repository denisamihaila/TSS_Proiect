"""AI-generated statement, decision and condition coverage tests."""

import unittest

from teste_ai.fitness_class_booking import FitnessClassBooking


def make_booking(max_spots: int = 5, price: float = 10.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "Instructor", max_spots, price)


class TestAIStatementCoverage(unittest.TestCase):
    def test_ai_sc_init_invalid_class_name(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("boxing", "Instructor", 5, 10.0)

    def test_ai_sc_init_empty_instructor(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "", 5, 10.0)

    def test_ai_sc_init_invalid_max_spots(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 31, 10.0)

    def test_ai_sc_init_invalid_price(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, 0.0)

    def test_ai_sc_book_spot_invalid_name_raises(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().book_spot("   ")

    def test_ai_sc_book_spot_confirmed(self) -> None:
        booking = make_booking()
        self.assertEqual(booking.book_spot("Alice"), "confirmed")

    def test_ai_sc_book_spot_waitlist(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        self.assertEqual(booking.book_spot("Bob"), "waitlist")

    def test_ai_sc_book_spot_rejected(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        for idx in range(5):
            booking.book_spot(f"W{idx}")
        self.assertEqual(booking.book_spot("Overflow"), "rejected")

    def test_ai_sc_cancel_confirmed_without_waitlist(self) -> None:
        booking = make_booking()
        booking.book_spot("Alice")
        self.assertTrue(booking.cancel_booking("Alice"))

    def test_ai_sc_cancel_confirmed_with_waitlist_promotion(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        booking.book_spot("Bob")
        self.assertTrue(booking.cancel_booking("Alice"))
        self.assertEqual(booking._confirmed, ["Bob"])

    def test_ai_sc_cancel_waitlist_client(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        booking.book_spot("Bob")
        self.assertTrue(booking.cancel_booking("Bob"))

    def test_ai_sc_cancel_not_found(self) -> None:
        self.assertFalse(make_booking().cancel_booking("Ghost"))

    def test_ai_sc_calculate_cost_invalid_sessions(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().calculate_cost(0, False)

    def test_ai_sc_calculate_cost_no_discount(self) -> None:
        self.assertEqual(make_booking().calculate_cost(3, False), 30.0)

    def test_ai_sc_calculate_cost_membership_discount(self) -> None:
        self.assertEqual(make_booking().calculate_cost(3, True), 24.0)

    def test_ai_sc_calculate_cost_volume_discount(self) -> None:
        self.assertEqual(make_booking().calculate_cost(10, False), 90.0)

    def test_ai_sc_calculate_cost_both_discounts(self) -> None:
        self.assertEqual(make_booking().calculate_cost(10, True), 70.0)


class TestAIDecisionCoverage(unittest.TestCase):
    def test_ai_dc_init_class_name_decision_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("spin", "Instructor", 5, 10.0)

    def test_ai_dc_init_class_name_decision_false(self) -> None:
        self.assertEqual(make_booking().class_name, "yoga")

    def test_ai_dc_init_instructor_decision_true_non_string(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", None, 5, 10.0)

    def test_ai_dc_init_instructor_decision_false(self) -> None:
        self.assertEqual(FitnessClassBooking("yoga", " Ana ", 5, 10.0).instructor, "Ana")

    def test_ai_dc_init_max_spots_decision_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", True, 10.0)

    def test_ai_dc_init_max_spots_decision_false(self) -> None:
        self.assertEqual(make_booking(max_spots=30).max_spots, 30)

    def test_ai_dc_init_price_decision_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, True)

    def test_ai_dc_init_price_decision_false(self) -> None:
        self.assertEqual(make_booking(price=0.5).price_per_session, 0.5)

    def test_ai_dc_book_spot_D1_true_invalid_name(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().book_spot(None)

    def test_ai_dc_book_spot_D1_false_valid_name_continues(self) -> None:
        self.assertEqual(make_booking().book_spot("Alice"), "confirmed")

    def test_ai_dc_book_spot_D2_true_free_spot(self) -> None:
        self.assertEqual(make_booking(max_spots=1).book_spot("Alice"), "confirmed")

    def test_ai_dc_book_spot_D2_false_class_full(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        self.assertEqual(booking.book_spot("Bob"), "waitlist")

    def test_ai_dc_book_spot_D3_true_waitlist_available(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        self.assertEqual(booking.book_spot("Bob"), "waitlist")

    def test_ai_dc_book_spot_D3_false_waitlist_full(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        for idx in range(5):
            booking.book_spot(f"W{idx}")
        self.assertEqual(booking.book_spot("Overflow"), "rejected")

    def test_ai_dc_cancel_D4_true_confirmed_client(self) -> None:
        booking = make_booking()
        booking.book_spot("Alice")
        self.assertTrue(booking.cancel_booking("Alice"))

    def test_ai_dc_cancel_D4_false_not_confirmed(self) -> None:
        self.assertFalse(make_booking().cancel_booking("Alice"))

    def test_ai_dc_cancel_D5_true_waitlist_promoted(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        booking.book_spot("Bob")
        booking.cancel_booking("Alice")
        self.assertEqual(booking._confirmed, ["Bob"])

    def test_ai_dc_cancel_D5_false_no_waitlist(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        booking.cancel_booking("Alice")
        self.assertEqual(booking._confirmed, [])

    def test_ai_dc_cancel_D6_true_waitlist_client(self) -> None:
        booking = make_booking(max_spots=1)
        booking.book_spot("Alice")
        booking.book_spot("Bob")
        self.assertTrue(booking.cancel_booking("Bob"))

    def test_ai_dc_cancel_D6_false_missing_client(self) -> None:
        self.assertFalse(make_booking().cancel_booking("Missing"))

    def test_ai_dc_calculate_guard_true_invalid_sessions(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().calculate_cost(False, False)

    def test_ai_dc_calculate_guard_false_valid_sessions(self) -> None:
        self.assertEqual(make_booking().calculate_cost(1, False), 10.0)

    def test_ai_dc_calculate_membership_true(self) -> None:
        self.assertEqual(make_booking().calculate_cost(5, True), 40.0)

    def test_ai_dc_calculate_membership_false(self) -> None:
        self.assertEqual(make_booking().calculate_cost(5, False), 50.0)

    def test_ai_dc_calculate_volume_true(self) -> None:
        self.assertEqual(make_booking().calculate_cost(10, False), 90.0)

    def test_ai_dc_calculate_volume_false(self) -> None:
        self.assertEqual(make_booking().calculate_cost(9, False), 90.0)


class TestAIConditionCoverage(unittest.TestCase):
    def test_ai_cc_init_max_bool_condition_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", True, 10.0)

    def test_ai_cc_init_max_bool_condition_false(self) -> None:
        self.assertEqual(make_booking(max_spots=5).max_spots, 5)

    def test_ai_cc_init_max_int_condition_false_for_float(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5.0, 10.0)

    def test_ai_cc_init_max_int_condition_true_for_int(self) -> None:
        self.assertEqual(make_booking(max_spots=6).max_spots, 6)

    def test_ai_cc_init_price_bool_condition_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, True)

    def test_ai_cc_init_price_numeric_condition_false_for_string(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, "10")

    def test_ai_cc_book_client_isinstance_condition_true_for_int(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().book_spot(99)

    def test_ai_cc_book_client_empty_condition_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().book_spot("")

    def test_ai_cc_book_client_strip_condition_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().book_spot("   ")

    def test_ai_cc_book_client_strip_condition_false(self) -> None:
        self.assertEqual(make_booking().book_spot(" Alice "), "confirmed")

    def test_ai_cc_calculate_sessions_isinstance_condition_false_for_float(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().calculate_cost(1.0, False)

    def test_ai_cc_calculate_sessions_bool_condition_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().calculate_cost(True, False)

    def test_ai_cc_calculate_sessions_lower_bound_condition_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().calculate_cost(-1, False)

    def test_ai_cc_calculate_sessions_upper_bound_condition_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().calculate_cost(99, False)

    def test_ai_cc_no_membership_below_volume_threshold(self) -> None:
        self.assertEqual(make_booking().calculate_cost(9, False), 90.0)

    def test_ai_cc_membership_below_volume_threshold(self) -> None:
        self.assertEqual(make_booking().calculate_cost(9, True), 72.0)

    def test_ai_cc_no_membership_at_volume_threshold(self) -> None:
        self.assertEqual(make_booking().calculate_cost(10, False), 90.0)

    def test_ai_cc_membership_at_volume_threshold(self) -> None:
        self.assertEqual(make_booking().calculate_cost(10, True), 70.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
