import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "Ana Pop", price_per_session)


class TestStatementCoverage(unittest.TestCase):
    """
    Teste pentru acoperire la nivel de instructiune.

    Sunt executate instructiunile principale din constructor si din
    evaluate_client_package, inclusiv caile valide si caile cu ValueError.
    """

    def test_sc_constructor_valid_assigns_fields(self) -> None:
        booking = FitnessClassBooking("pilates", "  Maria Pop  ", 30.0)

        self.assertEqual(booking.class_name, "pilates")
        self.assertEqual(booking.instructor, "Maria Pop")
        self.assertEqual(booking.price_per_session, 30.0)

    def test_sc_constructor_invalid_class_raises(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("boxing", "Ana Pop", 50.0)

    def test_sc_constructor_invalid_instructor_raises(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "   ", 50.0)

    def test_sc_constructor_invalid_price_raises(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Ana Pop", 0.0)

    def test_sc_invalid_package_data_raises(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([], False, False)

    def test_sc_invalid_session_status_raises(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package(["unknown"], 5, False)

    def test_sc_active_mixed_history_with_membership(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "no_show", "cancelled"], 5, True
        )

        self.assertEqual(result["attended"], 1)
        self.assertEqual(result["no_show"], 1)
        self.assertEqual(result["cancelled"], 1)
        self.assertEqual(result["total_cost"], 200.0)
        self.assertEqual(result["status"], "active")

    def test_sc_completed_successfully_without_membership(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 1, False)

        self.assertEqual(result["status"], "completed_successfully")

    def test_sc_completed_with_absences_with_no_show(self) -> None:
        result = make_booking().evaluate_client_package(["no_show"], 1, False)

        self.assertEqual(result["status"], "completed_with_absences")

    def test_sc_used_sessions_over_package_raises(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package(["attended", "no_show"], 1, False)


class TestDecisionCoverage(unittest.TestCase):
    """
    Teste pentru acoperire la nivel de decizie.

    Fiecare decizie relevanta este executata cel putin o data pe ramura True
    si cel putin o data pe ramura False.
    """

    def test_dc_package_validation_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([], 0, False)

    def test_dc_package_validation_false(self) -> None:
        result = make_booking().evaluate_client_package([], 1, False)

        self.assertEqual(result["status"], "active")

    def test_dc_session_status_validation_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([123], 5, False)

    def test_dc_session_status_validation_false(self) -> None:
        result = make_booking().evaluate_client_package(["cancelled"], 5, False)

        self.assertEqual(result["cancelled"], 1)

    def test_dc_attended_branch_true(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 2, False)

        self.assertEqual(result["attended"], 1)

    def test_dc_attended_branch_false_no_show(self) -> None:
        result = make_booking().evaluate_client_package(["no_show"], 2, False)

        self.assertEqual(result["no_show"], 1)

    def test_dc_cancelled_branch_true(self) -> None:
        result = make_booking().evaluate_client_package(["cancelled"], 2, False)

        self.assertEqual(result["cancelled"], 1)

    def test_dc_used_sessions_over_package_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package(["attended", "attended"], 1, False)

    def test_dc_membership_true(self) -> None:
        result = make_booking().evaluate_client_package([], 2, True)

        self.assertEqual(result["total_cost"], 80.0)

    def test_dc_membership_false(self) -> None:
        result = make_booking().evaluate_client_package([], 2, False)

        self.assertEqual(result["total_cost"], 100.0)

    def test_dc_completed_successfully_condition_true(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 1, False)

        self.assertEqual(result["status"], "completed_successfully")

    def test_dc_completed_successfully_condition_false_absences(self) -> None:
        result = make_booking().evaluate_client_package(["no_show"], 1, False)

        self.assertEqual(result["status"], "completed_with_absences")

    def test_dc_completed_successfully_condition_false_active(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 2, False)

        self.assertEqual(result["status"], "active")


class TestConditionCoverage(unittest.TestCase):
    """
    Teste pentru conditii simple si compuse.

    Sunt verificate conditii atomice din validarile constructorului, validarile
    metodei, conditia simpla has_membership si conditia compusa pentru status.
    """

    def test_cc_constructor_class_name_non_string_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking(123, "Ana Pop", 50.0)

    def test_cc_constructor_instructor_non_string_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", None, 50.0)

    def test_cc_constructor_price_bool_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Ana Pop", True)

    def test_cc_constructor_price_non_number_true(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Ana Pop", "50")

    def test_cc_simple_condition_has_membership_true(self) -> None:
        result = make_booking().evaluate_client_package([], 1, True)

        self.assertEqual(result["total_cost"], 40.0)

    def test_cc_simple_condition_has_membership_false(self) -> None:
        result = make_booking().evaluate_client_package([], 1, False)

        self.assertEqual(result["total_cost"], 50.0)

    def test_cc_compound_status_both_atomic_conditions_true(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 1, False)

        self.assertEqual(result["status"], "completed_successfully")

    def test_cc_compound_status_remaining_true_no_show_false(self) -> None:
        result = make_booking().evaluate_client_package(["no_show"], 1, False)

        self.assertEqual(result["status"], "completed_with_absences")

    def test_cc_compound_status_remaining_false(self) -> None:
        result = make_booking().evaluate_client_package(["attended"], 2, False)

        self.assertEqual(result["status"], "active")

    def test_cc_validation_condition_package_bool_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([], True, False)

    def test_cc_validation_condition_session_history_non_list_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package("attended", 5, False)

    def test_cc_validation_condition_package_non_int_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([], "5", False)

    def test_cc_validation_condition_package_below_min_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([], 0, False)

    def test_cc_validation_condition_package_above_max_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([], 21, False)

    def test_cc_validation_condition_membership_non_bool_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([], 5, "yes")

    def test_cc_session_status_condition_non_string_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([None], 3, False)

    def test_cc_session_status_condition_invalid_string_true(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package(["missed"], 3, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
