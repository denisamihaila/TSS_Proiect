import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "Ana Pop", price_per_session)


class TestAIGeneratedFunctionalScenarios(unittest.TestCase):
    """
    Teste generate cu AI pentru scenarii functionale ale metodei
    evaluate_client_package.

    Testele pastreaza acelasi stil cu suita existenta: unittest, helper local
    si verificari explicite pentru campurile intoarse in dictionar.
    """

    def test_ai_mixed_history_counts_each_status_correctly(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "cancelled", "no_show", "cancelled", "attended"],
            6,
            False,
        )

        self.assertEqual(result["attended"], 2)
        self.assertEqual(result["no_show"], 1)
        self.assertEqual(result["cancelled"], 2)
        self.assertEqual(result["used_sessions"], 3)
        self.assertEqual(result["remaining_sessions"], 3)
        self.assertEqual(result["total_cost"], 300.0)
        self.assertEqual(result["status"], "active")

    def test_ai_cancelled_sessions_do_not_prevent_clean_completion(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "cancelled", "attended", "cancelled"],
            2,
            False,
        )

        self.assertEqual(result["cancelled"], 2)
        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_successfully")

    def test_ai_no_show_completes_package_with_absences(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "no_show", "attended"],
            3,
            False,
        )

        self.assertEqual(result["used_sessions"], 3)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_with_absences")

    def test_ai_no_show_keeps_status_active_when_sessions_remain(self) -> None:
        result = make_booking().evaluate_client_package(["no_show"], 3, False)

        self.assertEqual(result["no_show"], 1)
        self.assertEqual(result["remaining_sessions"], 2)
        self.assertEqual(result["status"], "active")

    def test_ai_membership_discount_is_applied_and_rounded(self) -> None:
        result = make_booking(12.345).evaluate_client_package(
            ["attended", "cancelled"],
            3,
            True,
        )

        self.assertEqual(result["total_cost"], 29.63)
        self.assertEqual(result["remaining_sessions"], 2)
        self.assertEqual(result["status"], "active")

    def test_ai_max_package_can_be_completed_with_mixed_consumed_sessions(self) -> None:
        history = ["attended"] * 18 + ["no_show"] * 2 + ["cancelled"] * 3

        result = make_booking(10.0).evaluate_client_package(history, 20, True)

        self.assertEqual(result["attended"], 18)
        self.assertEqual(result["no_show"], 2)
        self.assertEqual(result["cancelled"], 3)
        self.assertEqual(result["used_sessions"], 20)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["total_cost"], 160.0)
        self.assertEqual(result["status"], "completed_with_absences")


class TestAIGeneratedValidationScenarios(unittest.TestCase):
    """Teste generate cu AI pentru validari si mesaje de eroare."""

    def test_ai_constructor_accepts_all_declared_valid_classes(self) -> None:
        for class_name in ["dance", "pilates", "yoga", "zumba"]:
            with self.subTest(class_name=class_name):
                booking = FitnessClassBooking(class_name, "  Instructor Test  ", 25)

                self.assertEqual(booking.class_name, class_name)
                self.assertEqual(booking.instructor, "Instructor Test")
                self.assertEqual(booking.price_per_session, 25.0)

    def test_ai_constructor_rejects_boolean_price(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^price_per_session must be greater than 0$"
        ):
            FitnessClassBooking("yoga", "Ana Pop", False)

    def test_ai_package_sessions_bool_is_invalid_even_if_true(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package([], True, False)

    def test_ai_has_membership_must_be_strict_bool(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package([], 5, 1)

    def test_ai_invalid_status_type_raises_status_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid session status$"):
            make_booking().evaluate_client_package(["attended", True], 5, False)

    def test_ai_invalid_status_value_raises_status_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid session status$"):
            make_booking().evaluate_client_package(["attended", "late"], 5, False)

    def test_ai_used_sessions_over_package_raises_specific_error(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^used sessions cannot exceed package sessions$"
        ):
            make_booking().evaluate_client_package(
                ["attended", "no_show", "attended"],
                2,
                False,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
