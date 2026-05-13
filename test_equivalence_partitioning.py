import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "Ana Pop", price_per_session)


class TestEquivalencePartitioning(unittest.TestCase):
    """
    Partitionare in clase de echivalenta pentru metoda
    evaluate_client_package(session_history, package_sessions, has_membership).
    """

    def setUp(self) -> None:
        self.booking = make_booking()

    def test_ep_valid_empty_history_returns_active_package(self) -> None:
        result = self.booking.evaluate_client_package([], 5, False)

        self.assertEqual(result["used_sessions"], 0)
        self.assertEqual(result["remaining_sessions"], 5)
        self.assertEqual(result["status"], "active")

    def test_ep_valid_mixed_history_with_membership(self) -> None:
        result = self.booking.evaluate_client_package(
            ["attended", "no_show", "cancelled"], 5, True
        )

        self.assertEqual(result["attended"], 1)
        self.assertEqual(result["no_show"], 1)
        self.assertEqual(result["cancelled"], 1)
        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 3)
        self.assertEqual(result["total_cost"], 200.0)
        self.assertEqual(result["status"], "active")

    def test_ep_completed_successfully_when_all_sessions_attended(self) -> None:
        result = self.booking.evaluate_client_package(
            ["attended", "attended", "attended"], 3, False
        )

        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_successfully")

    def test_ep_completed_with_absences_when_package_finished_with_no_show(self) -> None:
        result = self.booking.evaluate_client_package(
            ["attended", "no_show"], 2, False
        )

        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_with_absences")

    def test_ep_invalid_session_history_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package("attended", 5, False)

    def test_ep_invalid_package_sessions_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([], "5", False)

    def test_ep_invalid_membership_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([], 5, "yes")

    def test_ep_invalid_session_status_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package(["late_cancel"], 5, False)

    def test_ep_used_sessions_over_package_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package(["attended", "no_show"], 1, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
