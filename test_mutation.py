import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "Ana Pop", price_per_session)


class TestMutationFocusedCases(unittest.TestCase):
    """
    Teste suplimentare orientate pe mutanti neechivalenti probabili.

    Sunt vizate mutatii in incrementarea contoarelor, consumarea sedintelor,
    calculul costului, aplicarea discountului, rotunjire si mesajele publice
    de eroare.
    """

    def test_mutation_membership_discount_is_applied_to_whole_package(self) -> None:
        result = make_booking().evaluate_client_package([], 10, True)

        self.assertEqual(result["total_cost"], 400.0)

    def test_mutation_membership_discount_is_not_applied_without_membership(self) -> None:
        result = make_booking().evaluate_client_package([], 10, False)

        self.assertEqual(result["total_cost"], 500.0)

    def test_mutation_total_cost_uses_package_sessions_not_used_sessions(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 5, False)

        self.assertEqual(result["used_sessions"], 1)
        self.assertEqual(result["remaining_sessions"], 4)
        self.assertEqual(result["total_cost"], 250.0)

    def test_mutation_multiple_attended_sessions_are_all_counted(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "attended"], 3, False
        )

        self.assertEqual(result["attended"], 2)
        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_mutation_no_show_consumes_session_and_prevents_clean_completion(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "no_show"], 2, False
        )

        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_with_absences")
        self.assertNotEqual(result["status"], "completed_successfully")

    def test_mutation_cancelled_session_does_not_consume_package_session(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "cancelled"], 2, False
        )

        self.assertEqual(result["used_sessions"], 1)
        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_mutation_multiple_no_show_sessions_are_all_counted(self) -> None:
        result = make_booking().evaluate_client_package(
            ["no_show", "no_show"], 3, False
        )

        self.assertEqual(result["no_show"], 2)
        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_mutation_multiple_cancelled_sessions_are_all_counted(self) -> None:
        result = make_booking().evaluate_client_package(
            ["cancelled", "cancelled"], 3, False
        )

        self.assertEqual(result["cancelled"], 2)
        self.assertEqual(result["used_sessions"], 0)
        self.assertEqual(result["remaining_sessions"], 3)
        self.assertEqual(result["status"], "active")

    def test_mutation_total_cost_is_rounded_to_two_decimals(self) -> None:
        result = make_booking(1 / 3).evaluate_client_package([], 1, False)

        self.assertEqual(result["total_cost"], 0.33)

    def test_mutation_bool_price_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Ana Pop", True)

    def test_mutation_public_error_messages_are_stable(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^class_name must be dance, pilates, yoga or zumba$"
        ):
            FitnessClassBooking("boxing", "Ana Pop", 50.0)
        with self.assertRaisesRegex(
            ValueError, "^instructor must be a non-empty string$"
        ):
            FitnessClassBooking("yoga", "   ", 50.0)
        with self.assertRaisesRegex(
            ValueError, "^price_per_session must be greater than 0$"
        ):
            FitnessClassBooking("yoga", "Ana Pop", 0.0)
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package([], 0, False)
        with self.assertRaisesRegex(ValueError, "^invalid session status$"):
            make_booking().evaluate_client_package(["late"], 2, False)
        with self.assertRaisesRegex(
            ValueError, "^used sessions cannot exceed package sessions$"
        ):
            make_booking().evaluate_client_package(["attended", "no_show"], 1, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
