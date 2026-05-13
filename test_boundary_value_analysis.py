import unittest

from fitness_class_booking import FitnessClassBooking


def make_booking(price_per_session: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "Ana Pop", price_per_session)


class TestBoundaryValueAnalysis(unittest.TestCase):
    """
    Analiza valorilor de frontiera pentru pachetul de sedinte.

    Frontiere analizate:
    - package_sessions in [1, 20]
    - used_sessions <= package_sessions
    - statusul final cand remaining_sessions devine 0
    """

    def setUp(self) -> None:
        self.booking = make_booking()

    def test_bva_package_sessions_zero_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([], 0, False)

    def test_bva_package_sessions_one_is_valid(self) -> None:
        result = self.booking.evaluate_client_package([], 1, False)

        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_bva_package_sessions_two_is_valid(self) -> None:
        result = self.booking.evaluate_client_package(["attended"], 2, False)

        self.assertEqual(result["used_sessions"], 1)
        self.assertEqual(result["remaining_sessions"], 1)

    def test_bva_package_sessions_nineteen_is_valid(self) -> None:
        result = self.booking.evaluate_client_package(["attended"], 19, False)

        self.assertEqual(result["remaining_sessions"], 18)
        self.assertEqual(result["total_cost"], 950.0)

    def test_bva_package_sessions_twenty_is_valid(self) -> None:
        result = self.booking.evaluate_client_package(["attended"], 20, False)

        self.assertEqual(result["remaining_sessions"], 19)
        self.assertEqual(result["total_cost"], 1000.0)

    def test_bva_package_sessions_twenty_one_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package([], 21, False)

    def test_bva_one_session_before_completion_is_active(self) -> None:
        result = self.booking.evaluate_client_package(
            ["attended", "attended"], 3, False
        )

        self.assertEqual(result["used_sessions"], 2)
        self.assertEqual(result["remaining_sessions"], 1)
        self.assertEqual(result["status"], "active")

    def test_bva_exact_completion_without_no_show_is_completed_successfully(self) -> None:
        result = self.booking.evaluate_client_package(
            ["attended", "attended", "attended"], 3, False
        )

        self.assertEqual(result["used_sessions"], 3)
        self.assertEqual(result["remaining_sessions"], 0)
        self.assertEqual(result["status"], "completed_successfully")

    def test_bva_one_session_over_package_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.booking.evaluate_client_package(
                ["attended", "attended", "attended", "attended"], 3, False
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
