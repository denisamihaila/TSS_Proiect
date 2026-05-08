import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "Ana Pop", price_per_session)


class TestIndependentCircuitsEvaluateClientPackage(unittest.TestCase):
    """
    Circuite independente pentru evaluate_client_package.

    Decizii principale urmarite:
    D1  validarea parametrilor metodei
    D2  validarea fiecarui status din session_history
    D3  session_status == "attended"
    D4  session_status == "no_show"
    D5  session_status == "cancelled"
    D6  used_sessions > package_sessions
    D7  has_membership
    D8  remaining_sessions == 0 and no_show == 0
    D9  remaining_sessions == 0
    """

    def test_path1_invalid_method_parameters_raise_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package([], 0, False)

    def test_path2_empty_history_active_package(self) -> None:
        result = make_booking().evaluate_client_package([], 4, False)

        self.assertEqual(result["used_sessions"], 0)
        self.assertEqual(result["status"], "active")

    def test_path3_invalid_session_status_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package(["attended", "late"], 4, False)

    def test_path4_attended_sessions_complete_clean_package(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "attended"], 2, False
        )

        self.assertEqual(result["status"], "completed_clean")

    def test_path5_no_show_consumes_session_and_completes_package(self) -> None:
        result = make_booking().evaluate_client_package(["no_show"], 1, False)

        self.assertEqual(result["used_sessions"], 1)
        self.assertEqual(result["status"], "completed")

    def test_path6_cancelled_session_does_not_consume_package(self) -> None:
        result = make_booking().evaluate_client_package(["cancelled"], 1, False)

        self.assertEqual(result["used_sessions"], 0)
        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_path7_mixed_history_with_membership_is_active(self) -> None:
        result = make_booking().evaluate_client_package(
            ["attended", "cancelled", "no_show"], 5, True
        )

        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["total_cost"], 200.0)
        self.assertEqual(result["status"], "active")

    def test_path8_used_sessions_over_package_raise_value_error(self) -> None:
        with self.assertRaises(ValueError):
            make_booking().evaluate_client_package(
                ["attended", "attended", "no_show"], 2, False
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
