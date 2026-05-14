import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("dance", "Mihai Stan", price_per_session)


class TestAIBoundaryValues(unittest.TestCase):
    """
    Teste generate cu AI pentru valori de frontiera.

    Sunt reluate frontierele importante din proiect: instructor dupa strip,
    pretul pozitiv, package_sessions in intervalul [1, 20] si granita dintre
    pachet activ, finalizat exact si depasit.
    """

    def test_ai_bva_instructor_one_visible_character_after_strip_is_valid(self) -> None:
        booking = FitnessClassBooking("dance", "   M   ", 20.0)

        self.assertEqual(booking.instructor, "M")

    def test_ai_bva_instructor_empty_after_strip_is_invalid(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^instructor must be a non-empty string$"
        ):
            FitnessClassBooking("dance", "      ", 20.0)

    def test_ai_bva_price_small_positive_value_is_valid(self) -> None:
        booking = FitnessClassBooking("dance", "Mihai Stan", 0.001)

        self.assertEqual(booking.price_per_session, 0.001)

    def test_ai_bva_price_zero_is_invalid(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^price_per_session must be greater than 0$"
        ):
            FitnessClassBooking("dance", "Mihai Stan", 0)

    def test_ai_bva_package_sessions_below_lower_limit_is_invalid(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package([], 0, False)

    def test_ai_bva_package_sessions_lower_limit_is_valid(self) -> None:
        result = make_booking().evaluate_client_package(["cancelled"], 1, False)

        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_ai_bva_package_sessions_just_above_lower_limit_is_valid(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 2, False)

        self.assertEqual(result["used_sessions"], 1)
        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_ai_bva_package_sessions_just_below_upper_limit_is_valid(self) -> None:
        result = make_booking().evaluate_client_package(["attended"] * 18, 19, False)

        self.assertEqual(result["used_sessions"], 18)
        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["total_cost"], 950.0)

    def test_ai_bva_package_sessions_upper_limit_is_valid(self) -> None:
        result = make_booking().evaluate_client_package(["attended"] * 19, 20, False)

        self.assertEqual(result["used_sessions"], 19)
        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["total_cost"], 1000.0)

    def test_ai_bva_package_sessions_above_upper_limit_is_invalid(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid package data$"):
            make_booking().evaluate_client_package([], 21, False)

    def test_ai_bva_exact_completion_without_absences(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "attended", "cancelled"],
            2,
            False,
        )

        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_successfully")

    def test_ai_bva_exact_completion_with_absences(self) -> None:
        result = make_booking().evaluate_client_package(
            ["no_show", "attended", "cancelled"],
            2,
            False,
        )

        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_with_absences")

    def test_ai_bva_one_consumed_session_over_package_is_invalid(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "^used sessions cannot exceed package sessions$"
        ):
            make_booking().evaluate_client_package(
                ["attended", "attended", "attended"],
                2,
                False,
            )


class TestAIStructuralDecisions(unittest.TestCase):
    """
    Teste generate cu AI pentru ramuri si conditii.

    Fiecare decizie majora este exercitata pe valori diferite fata de testele
    originale: validari, statusurile din for, membership si statusul final.
    """

    def test_ai_decision_package_validation_false_path(self) -> None:
        result = make_booking().evaluate_client_package([], 4, False)

        self.assertEqual(result["status"], "active")

    def test_ai_decision_status_validation_true_path(self) -> None:
        with self.assertRaisesRegex(ValueError, "^invalid session status$"):
            make_booking().evaluate_client_package(["cancelled", object()], 4, False)

    def test_ai_decision_attended_branch_true_path(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 4, False)

        self.assertEqual(result["attended"], 1)
        self.assertEqual(result["used_sessions"], 1)

    def test_ai_decision_attended_branch_false_no_show_path(self) -> None:
        result = make_booking().evaluate_client_package(["no_show"], 4, False)

        self.assertEqual(result["attended"], 0)
        self.assertEqual(result["no_show"], 1)

    def test_ai_decision_attended_branch_false_cancelled_path(self) -> None:
        result = make_booking().evaluate_client_package(["cancelled"], 4, False)

        self.assertEqual(result["attended"], 0)
        self.assertEqual(result["cancelled"], 1)
        self.assertEqual(result["used_sessions"], 0)

    def test_ai_decision_membership_true_path(self) -> None:
        result = make_booking().evaluate_client_package(["cancelled"], 4, True)

        self.assertEqual(result["total_cost"], 160.0)

    def test_ai_decision_membership_false_path(self) -> None:
        result = make_booking().evaluate_client_package(["cancelled"], 4, False)

        self.assertEqual(result["total_cost"], 200.0)

    def test_ai_decision_compound_status_true_true(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 1, False)

        self.assertEqual(result["status"], "completed_successfully")

    def test_ai_decision_compound_status_true_false(self) -> None:
        result = make_booking().evaluate_client_package(["no_show"], 1, False)

        self.assertEqual(result["status"], "completed_with_absences")

    def test_ai_decision_compound_status_false_branch(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 3, False)

        self.assertEqual(result["status"], "active")


if __name__ == "__main__":
    unittest.main(verbosity=2)
