"""AI-generated tests aimed at mutation-testing weak spots."""

import unittest

from teste_ai.fitness_class_booking import FitnessClassBooking


class TestAIMutationFocusedCases(unittest.TestCase):
    def test_ai_mutation_whitespace_only_instructor_must_raise_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "instructor must be a non-empty string"):
            FitnessClassBooking("yoga", "   ", 5, 10.0)

    def test_ai_mutation_tab_only_instructor_must_raise_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "instructor must be a non-empty string"):
            FitnessClassBooking("yoga", "\t", 5, 10.0)

    def test_ai_mutation_max_spots_true_must_raise_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "max_spots must be an integer"):
            FitnessClassBooking("yoga", "Instructor", True, 10.0)

    def test_ai_mutation_price_true_must_raise_value_error_in_ai_copy(self) -> None:
        with self.assertRaisesRegex(ValueError, "price_per_session must be greater than 0"):
            FitnessClassBooking("yoga", "Instructor", 5, True)

    def test_ai_mutation_price_just_above_zero_must_stay_valid(self) -> None:
        b = FitnessClassBooking("yoga", "Instructor", 5, 0.01)
        self.assertEqual(b.price_per_session, 0.01)

    def test_ai_mutation_rounds_base_cost_to_two_decimals(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 1.2345)
        self.assertEqual(booking.calculate_cost(3, False), 3.7)

    def test_ai_mutation_rounds_discounted_cost_to_two_decimals(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 1.2345)
        self.assertEqual(booking.calculate_cost(3, True), 2.96)

    def test_ai_mutation_cancel_confirmed_promotes_exact_first_waitlist_client(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        booking.book_spot("Alice")
        booking.book_spot("Bob")
        booking.book_spot("Carol")
        booking.cancel_booking("Alice")
        self.assertEqual(booking._confirmed, ["Bob"])
        self.assertEqual(booking.waitlist, ["Carol"])

    def test_ai_mutation_cancel_none_does_not_remove_blank_named_client(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        booking.book_spot("XXXX")
        self.assertFalse(booking.cancel_booking(None))
        self.assertEqual(booking._confirmed, ["XXXX"])

    def test_ai_mutation_error_message_for_invalid_price_is_stable(self) -> None:
        with self.assertRaisesRegex(ValueError, "price_per_session must be greater than 0"):
            FitnessClassBooking("yoga", "Instructor", 5, "10")

    def test_ai_mutation_sessions_bool_is_rejected(self) -> None:
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        with self.assertRaisesRegex(ValueError, "sessions must be between 1 and 20 inclusive"):
            booking.calculate_cost(False, True)

    def test_ai_mutation_list_class_name_documents_type_gap(self) -> None:
        with self.assertRaises(TypeError):
            FitnessClassBooking([], "Instructor", 5, 10.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
