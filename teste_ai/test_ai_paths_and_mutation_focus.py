import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("zumba", "Elena Dima", price_per_session)


class TestAIIndependentPathAlternatives(unittest.TestCase):
    """
    Teste generate cu AI pentru cai independente alternative.

    Cazurile sunt gandite ca variante ale circuitelor independente deja testate:
    validari timpurii, istoric gol, status invalid, fiecare status valid,
    membership, pachet depasit si cele trei rezultate finale.
    """

    def test_ai_path_invalid_session_history_stops_immediately(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package(None, 5, False)

    def test_ai_path_empty_history_with_membership_is_active(self) -> None:
        result = make_booking(30.0).evaluate_client_package([], 5, True)

        self.assertEqual(result["used_sessions"], 0)
        self.assertEqual(result["remaining_sessions"], 5)
        self.assertEqual(result["total_cost"], 120.0)
        self.assertEqual(result["status"], "active")

    def test_ai_path_invalid_status_after_valid_status_raises(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid session status$"):
            make_booking().evaluate_client_package(
                ["attended", "cancelled", "late_cancel"],
                5,
                False,
            )

    def test_ai_path_attended_then_cancelled_keeps_package_active(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "cancelled"],
            3,
            False,
        )

        self.assertEqual(result["attended"], 1)
        self.assertEqual(result["cancelled"], 1)
        self.assertEqual(result["used_sessions"], 1)
        self.assertEqual(result["remaining_sessions"], 2)
        self.assertEqual(result["status"], "active")

    def test_ai_path_no_show_then_cancelled_keeps_absence_count(self) -> None:
        result = make_booking().evaluate_client_package(
            ["no_show", "cancelled"],
            3,
            False,
        )

        self.assertEqual(result["no_show"], 1)
        self.assertEqual(result["cancelled"], 1)
        self.assertEqual(result["used_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_ai_path_cancelled_then_attended_can_complete_cleanly(self) -> None:
        result = make_booking().evaluate_client_package(
            ["cancelled", "attended"],
            1,
            False,
        )

        self.assertEqual(result["cancelled"], 1)
        self.assertEqual(result["attended"], 1)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_successfully")

    def test_ai_path_used_sessions_over_package_after_loop_raises(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^used sessions cannot exceed package sessions$"
        ):
            make_booking().evaluate_client_package(
                ["cancelled", "attended", "no_show"],
                1,
                False,
            )

    def test_ai_path_membership_complete_with_absences(self) -> None:
        result = make_booking().evaluate_client_package(
            ["no_show", "attended"],
            2,
            True,
        )

        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["total_cost"], 80.0)
        self.assertEqual(result["status"], "completed_with_absences")


class TestAIMutationFocusedAlternatives(unittest.TestCase):
    """
    Teste generate cu AI orientate pe mutanti probabili.

    Sunt verificate calcule care ar prinde schimbari in operatori, contoare,
    discount, rotunjire si validari stricte pentru bool.
    """

    def test_ai_mutation_total_cost_uses_total_package_not_consumed_sessions(self) -> None:
        result = make_booking(45.0).evaluate_client_package(["attended"], 6, False)

        self.assertEqual(result["used_sessions"], 1)
        self.assertEqual(result["remaining_sessions"], 5)
        self.assertEqual(result["total_cost"], 270.0)

    def test_ai_mutation_membership_discount_uses_twenty_percent(self) -> None:
        result = make_booking(75.0).evaluate_client_package([], 4, True)

        self.assertEqual(result["total_cost"], 240.0)

    def test_ai_mutation_no_membership_keeps_full_price(self) -> None:
        result = make_booking(75.0).evaluate_client_package([], 4, False)

        self.assertEqual(result["total_cost"], 300.0)

    def test_ai_mutation_multiple_status_counters_are_independent(self) -> None:
        result = make_booking().evaluate_client_package(
            ["cancelled", "no_show", "cancelled", "attended", "no_show"],
            5,
            False,
        )

        self.assertEqual(result["attended"], 1)
        self.assertEqual(result["no_show"], 2)
        self.assertEqual(result["cancelled"], 2)
        self.assertEqual(result["used_sessions"], 3)
        self.assertEqual(result["remaining_sessions"], 2)

    def test_ai_mutation_rounds_discounted_total_to_two_decimals(self) -> None:
        result = make_booking(19.995).evaluate_client_package([], 3, True)

        self.assertEqual(result["total_cost"], 47.99)

    def test_ai_mutation_package_sessions_false_is_invalid_bool(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package([], False, False)

    def test_ai_mutation_price_false_is_invalid_bool(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^price_per_session must be greater than 0$"
        ):
            FitnessClassBooking("zumba", "Elena Dima", False)

    def test_ai_mutation_error_messages_remain_public_contract(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^class_name must be dance, pilates, yoga or zumba$"
        ):
            FitnessClassBooking("cycling", "Elena Dima", 50.0)

        with self.assertRaisesRegex(
            ValueError, "^instructor must be a non-empty string$"
        ):
            FitnessClassBooking("zumba", "", 50.0)

        with self.assertRaisesRegex(ValueError, "^invalid session status$"):
            make_booking().evaluate_client_package(["absent"], 2, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
