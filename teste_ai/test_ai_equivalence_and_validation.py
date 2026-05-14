import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("pilates", "Ioana Marin", price_per_session)


class TestAIEquivalenceClasses(unittest.TestCase):
    """
    Teste generate cu AI pentru clase de echivalenta.

    Sunt acoperite clase valide si invalide pentru constructor, datele metodei
    evaluate_client_package si statusurile acceptate in session_history.
    """

    def test_ai_eq_valid_constructor_with_integer_price(self) -> None:
        booking = FitnessClassBooking("zumba", "  Radu Ionescu  ", 35)

        self.assertEqual(booking.class_name, "zumba")
        self.assertEqual(booking.instructor, "Radu Ionescu")
        self.assertEqual(booking.price_per_session, 35.0)

    def test_ai_eq_invalid_class_name_none_raises_value_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^class_name must be dance, pilates, yoga or zumba$"
        ):
            FitnessClassBooking(None, "Ana Pop", 50.0)

    def test_ai_eq_invalid_class_name_case_sensitive_raises_value_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^class_name must be dance, pilates, yoga or zumba$"
        ):
            FitnessClassBooking("Yoga", "Ana Pop", 50.0)

    def test_ai_eq_invalid_instructor_none_raises_value_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^instructor must be a non-empty string$"
        ):
            FitnessClassBooking("yoga", None, 50.0)

    def test_ai_eq_invalid_instructor_only_newlines_raises_value_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^instructor must be a non-empty string$"
        ):
            FitnessClassBooking("yoga", "\n\t  ", 50.0)

    def test_ai_eq_invalid_price_string_raises_value_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^price_per_session must be greater than 0$"
        ):
            FitnessClassBooking("yoga", "Ana Pop", "50")

    def test_ai_eq_invalid_price_negative_raises_value_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^price_per_session must be greater than 0$"
        ):
            FitnessClassBooking("yoga", "Ana Pop", -5)

    def test_ai_eq_valid_empty_history_active_package(self) -> None:
        result = make_booking().evaluate_client_package([], 8, False)

        self.assertEqual(result["attended"], 0)
        self.assertEqual(result["no_show"], 0)
        self.assertEqual(result["cancelled"], 0)
        self.assertEqual(result["used_sessions"], 0)
        self.assertEqual(result["remaining_sessions"], 8)
        self.assertEqual(result["status"], "active")

    def test_ai_eq_valid_history_with_all_status_types(self) -> None:
        result = make_booking().evaluate_client_package(
            ["cancelled", "attended", "no_show", "attended"],
            6,
            True,
        )

        self.assertEqual(result["attended"], 2)
        self.assertEqual(result["no_show"], 1)
        self.assertEqual(result["cancelled"], 1)
        self.assertEqual(result["used_sessions"], 3)
        self.assertEqual(result["remaining_sessions"], 3)
        self.assertEqual(result["total_cost"], 240.0)
        self.assertEqual(result["status"], "active")

    def test_ai_eq_all_attended_complete_successfully(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "attended", "attended", "attended"],
            4,
            False,
        )

        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_successfully")

    def test_ai_eq_all_no_show_complete_with_absences(self) -> None:
        result = make_booking().evaluate_client_package(
            ["no_show", "no_show"],
            2,
            False,
        )

        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["status"], "completed_with_absences")

    def test_ai_eq_only_cancelled_sessions_keep_package_active(self) -> None:
        result = make_booking().evaluate_client_package(
            ["cancelled", "cancelled", "cancelled"],
            3,
            False,
        )

        self.assertEqual(result["cancelled"], 3)
        self.assertEqual(result["used_sessions"], 0)
        self.assertEqual(result["remaining_sessions"], 3)
        self.assertEqual(result["status"], "active")

    def test_ai_eq_invalid_session_history_tuple_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package(("attended",), 3, False)

    def test_ai_eq_invalid_package_sessions_float_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package([], 3.5, False)

    def test_ai_eq_invalid_membership_integer_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package([], 3, 0)

    def test_ai_eq_invalid_status_empty_string_raises_value_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid session status$"):
            make_booking().evaluate_client_package([""], 3, False)

    def test_ai_eq_consumed_sessions_greater_than_package_raises_value_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^used sessions cannot exceed package sessions$"
        ):
            make_booking().evaluate_client_package(
                ["attended", "attended", "no_show"],
                2,
                False,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
