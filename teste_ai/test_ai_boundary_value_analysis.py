"""AI-generated boundary value analysis tests."""

import unittest

from teste_ai.fitness_class_booking import FitnessClassBooking


class TestAIBoundaryValueAnalysis(unittest.TestCase):
    """Boundary checks for constructor limits, waitlist limits and discounts."""

    def test_ai_bva_max_spots_zero_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 0, 10.0)

    def test_ai_bva_max_spots_one_is_valid(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        self.assertEqual(b.max_spots, 1)

    def test_ai_bva_max_spots_two_is_valid(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 2, 10.0)
        self.assertEqual(b.max_spots, 2)

    def test_ai_bva_max_spots_twenty_nine_is_valid(self) -> None:
        b = FitnessClassBooking("dance", "Instructor", 29, 10.0)
        self.assertEqual(b.max_spots, 29)

    def test_ai_bva_max_spots_thirty_is_valid(self) -> None:
        b = FitnessClassBooking("dance", "Instructor", 30, 10.0)
        self.assertEqual(b.max_spots, 30)

    def test_ai_bva_max_spots_thirty_one_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("dance", "Instructor", 31, 10.0)

    def test_ai_bva_price_negative_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, -0.01)

    def test_ai_bva_price_zero_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, 0.0)

    def test_ai_bva_price_one_cent_is_valid(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 5, 0.01)
        self.assertEqual(b.price_per_session, 0.01)

    def test_ai_bva_price_bool_true_is_rejected_by_ai_copy(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, True)

    def test_ai_bva_last_confirmed_spot_returns_confirmed(self) -> None:
        booking = FitnessClassBooking("pilates", "Instructor", 5, 10.0)
        for idx in range(4):
            booking.book_spot(f"C{idx}")
        self.assertEqual(booking.book_spot("LastFree"), "confirmed")
        self.assertEqual(booking.booked_spots, 5)

    def test_ai_bva_first_waitlist_spot_returns_waitlist(self) -> None:
        booking = FitnessClassBooking("pilates", "Instructor", 5, 10.0)
        for idx in range(5):
            booking.book_spot(f"C{idx}")
        self.assertEqual(booking.book_spot("W0"), "waitlist")
        self.assertEqual(len(booking.waitlist), 1)

    def test_ai_bva_fifth_waitlist_spot_returns_waitlist(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 2, 10.0)
        booking.book_spot("C1")
        booking.book_spot("C2")
        for idx in range(4):
            booking.book_spot(f"W{idx}")
        self.assertEqual(booking.book_spot("W4"), "waitlist")
        self.assertEqual(len(booking.waitlist), 5)

    def test_ai_bva_sixth_waitlist_spot_returns_rejected(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 2, 10.0)
        booking.book_spot("C1")
        booking.book_spot("C2")
        for idx in range(5):
            booking.book_spot(f"W{idx}")
        self.assertEqual(booking.book_spot("Overflow"), "rejected")

    def test_ai_bva_sessions_zero_raises_value_error(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        with self.assertRaises(ValueError):
            booking.calculate_cost(0, False)

    def test_ai_bva_sessions_one_is_valid(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(1, False), 10.0)

    def test_ai_bva_sessions_two_is_valid(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(2, False), 20.0)

    def test_ai_bva_sessions_nine_has_no_volume_discount(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(9, False), 90.0)

    def test_ai_bva_sessions_ten_has_volume_discount(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(10, False), 90.0)

    def test_ai_bva_sessions_eleven_has_volume_discount(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(11, False), 99.0)

    def test_ai_bva_sessions_nineteen_is_valid(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(19, False), 171.0)

    def test_ai_bva_sessions_twenty_is_valid(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(booking.calculate_cost(20, False), 180.0)

    def test_ai_bva_sessions_twenty_one_raises_value_error(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        with self.assertRaises(ValueError):
            booking.calculate_cost(21, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
