"""AI-generated independent-circuit tests for the CFG paths."""

import unittest

from teste_ai.fitness_class_booking import FitnessClassBooking


class TestAIIndependentCircuitsInit(unittest.TestCase):
    def test_ai_init_path1_invalid_class_name_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("boxing", "Instructor", 5, 10.0)

    def test_ai_init_path2_invalid_instructor_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "   ", 5, 10.0)

    def test_ai_init_path3_invalid_max_spots_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 31, 10.0)

    def test_ai_init_path4_invalid_price_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, 0.0)

    def test_ai_init_path5_all_valid_creates_object(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual((b.class_name, b.max_spots, b.price_per_session), ("yoga", 5, 10.0))


class TestAIIndependentCircuitsBookSpot(unittest.TestCase):
    def test_ai_bs_path1_invalid_client_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 1, 10.0).book_spot("")

    def test_ai_bs_path2_free_spot_returns_confirmed(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        self.assertEqual(booking.book_spot("Alice"), "confirmed")

    def test_ai_bs_path3_full_class_waitlist_available_returns_waitlist(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        booking.book_spot("Alice")
        self.assertEqual(booking.book_spot("Bob"), "waitlist")

    def test_ai_bs_path4_full_class_full_waitlist_returns_rejected(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        booking.book_spot("Alice")
        for idx in range(5):
            booking.book_spot(f"W{idx}")
        self.assertEqual(booking.book_spot("Overflow"), "rejected")


class TestAIIndependentCircuitsCancelBooking(unittest.TestCase):
    def test_ai_cb_path1_confirmed_no_waitlist_cancels_returns_true(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 2, 10.0)
        booking.book_spot("Alice")
        self.assertTrue(booking.cancel_booking("Alice"))

    def test_ai_cb_path2_confirmed_with_waitlist_promotes_returns_true(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        booking.book_spot("Alice")
        booking.book_spot("Bob")
        self.assertTrue(booking.cancel_booking("Alice"))
        self.assertEqual(booking._confirmed, ["Bob"])

    def test_ai_cb_path3_waitlist_client_removed_returns_true(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        booking.book_spot("Alice")
        booking.book_spot("Bob")
        self.assertTrue(booking.cancel_booking("Bob"))
        self.assertEqual(booking.waitlist, [])

    def test_ai_cb_path4_client_not_found_returns_false(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        self.assertFalse(booking.cancel_booking("Ghost"))


class TestAIIndependentCircuitsCalculateCost(unittest.TestCase):
    def test_ai_cc_path1_invalid_sessions_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, 10.0).calculate_cost(0, False)

    def test_ai_cc_path2_no_membership_below_10_sessions_base_cost(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(5, False), 50.0)

    def test_ai_cc_path3_with_membership_below_10_sessions_membership_discount(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(5, True), 40.0)

    def test_ai_cc_path4_no_membership_ten_sessions_volume_discount(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(10, False), 90.0)

    def test_ai_cc_path5_membership_ten_sessions_both_discounts(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(10, True), 70.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
