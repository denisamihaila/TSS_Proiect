import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "Ana Pop", price_per_session)


class TestEquivalencePartitioning(unittest.TestCase):
    """
    Partitionare in clase de echivalenta pentru clasa FitnessClassBooking si metoda
    evaluate_client_package(session_history, package_sessions, has_membership).

    Sunt verificate clase valide si invalide pentru constructor, istoricul
    sedintelor, numarul de sedinte din pachet, membership si statusul final.
    """

    def setUp(self) -> None:
        self.booking = make_booking()

    def test_ep_valid_constructor_data_creates_booking(self) -> None:
        booking = FitnessClassBooking("dance", "Maria Pop", 40)

        self.assertEqual(booking.class_name, "dance")
        self.assertEqual(booking.instructor, "Maria Pop")
        self.assertEqual(booking.price_per_session, 40.0)

    def test_ep_invalid_class_name_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking(123, "Ana Pop", 50.0)

    def test_ep_invalid_class_name_value_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("boxing", "Ana Pop", 50.0)

    def test_ep_invalid_instructor_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", None, 50.0)

    def test_ep_invalid_blank_instructor_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "   ", 50.0)

    def test_ep_invalid_price_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Ana Pop", "50")

    def test_ep_invalid_price_bool_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Ana Pop", True)

    def test_ep_invalid_price_non_positive_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Ana Pop", -10.0)

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

    def test_ep_valid_only_cancelled_history_does_not_consume_sessions(self) -> None:
        result = self.booking.evaluate_client_package(
            ["cancelled", "cancelled"], 4, False
        )

        self.assertEqual(result["cancelled"], 2)
        self.assertEqual(result["used_sessions"], 0)
        self.assertEqual(result["remaining_sessions"], 4)
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

    def test_ep_invalid_package_sessions_bool_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([], True, False)

    def test_ep_invalid_package_sessions_below_range_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([], 0, False)

    def test_ep_invalid_package_sessions_above_range_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([], 25, False)

    def test_ep_invalid_membership_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([], 5, "yes")

    def test_ep_invalid_session_status_type_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([None], 5, False)

    def test_ep_invalid_session_status_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package(["late_cancel"], 5, False)

    def test_ep_used_sessions_over_package_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package(["attended", "no_show"], 1, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
