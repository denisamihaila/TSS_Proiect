"""
test_equivalence_partitioning.py – Partiționare în clase de echivalență.

Strategie: Se împart input-urile fiecărei metode în grupe (clase) cu
comportament identic și se testează câte un reprezentant din fiecare clasă.

Proiect TSS – T1 | FitnessClassBooking
"""

import unittest
from fitness_class_booking import FitnessClassBooking


class TestEquivalencePartitioning(unittest.TestCase):
    """
    Partiționare în clase de echivalență pentru FitnessClassBooking.

    ═══════════════════════════════════════════════════════════════════
    __init__(class_name, instructor, max_spots, price_per_session)
    ───────────────────────────────────────────────────────────────────
    EC01  class_name valid ("yoga")                     → obiect creat
    EC02  class_name invalid ("crossfit")               → ValueError
    EC03  instructor non-empty ("Ana Pop")              → obiect creat
    EC04  instructor gol ("")                           → ValueError
    EC05  instructor whitespace-only ("   ")            → ValueError
    EC06  max_spots în domeniu (10)                     → obiect creat
    EC07  max_spots sub domeniu (0)                     → ValueError
    EC08  max_spots peste domeniu (31)                  → ValueError
    EC09  max_spots float (1.0)                         → ValueError
    EC10  max_spots bool False (≡ 0 < 1)               → ValueError
    EC11  price_per_session > 0 (15.0)                  → obiect creat
    EC12  price_per_session <= 0 (0.0)                  → ValueError

    book_spot(client_name)
    ───────────────────────────────────────────────────────────────────
    EC13  client_name valid, loc disponibil             → "confirmed"
    EC14  client_name gol ("")                          → ValueError
    EC15  clasa plină, waitlist disponibil              → "waitlist"
    EC16  clasa plină, waitlist plin                    → "rejected"
    EC29  client_name non-string (int)                  → ValueError

    cancel_booking(client_name)
    ───────────────────────────────────────────────────────────────────
    EC17  client cu rezervare confirmată                → True
    EC18  client pe waitlist                            → True
    EC19  client negăsit                                → False

    calculate_cost(sessions, has_membership)
    ───────────────────────────────────────────────────────────────────
    EC20  sessions valid (5), fără membership           → cost de bază
    EC21  sessions = 0 (sub domeniu)                    → ValueError
    EC22  sessions = 21 (peste domeniu)                 → ValueError
    EC23  sessions valid (5), cu membership             → 20% reducere
    EC24  sessions >= 10 (10), fără membership          → 10% reducere vol.
    EC25  sessions >= 10 (10), cu membership            → 20% + 10% reducere
    EC30  sessions non-integer (str "5")                → ValueError

    Validări suplimentare de tip (tipuri non-string sau non-int respinse explicit)
    ───────────────────────────────────────────────────────────────────
    EC26  instructor non-string (int 123)               → ValueError
    EC27  price_per_session non-numeric (str "10")      → ValueError
    EC28  max_spots bool True (subclasă int, dar bool)  → ValueError
    ═══════════════════════════════════════════════════════════════════
    """

    def setUp(self) -> None:
        """Creează o instanță standard refolosibilă în teste."""
        self.booking = FitnessClassBooking("yoga", "Ana Pop", 5, 10.0)

    # ── __init__ ──────────────────────────────────────────────────────

    def test_init_valid_class_name_creates_object(self) -> None:
        """EC01: class_name = 'yoga' (valid) → obiect creat fără excepție."""
        b = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(b.class_name, "yoga")

    def test_init_invalid_class_name_raises_value_error(self) -> None:
        """EC02: class_name = 'crossfit' (invalid) → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("crossfit", "Instructor", 5, 10.0)

    def test_init_valid_instructor_creates_object(self) -> None:
        """EC03: instructor non-empty → obiect creat corect."""
        b = FitnessClassBooking("dance", "Maria Ionescu", 5, 10.0)
        self.assertEqual(b.instructor, "Maria Ionescu")

    def test_init_empty_instructor_raises_value_error(self) -> None:
        """EC04: instructor = '' → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("dance", "", 5, 10.0)

    def test_init_whitespace_only_instructor_raises_value_error(self) -> None:
        """EC05: instructor = '   ' (whitespace pur) → ValueError.
        Ucide M12: schimbarea 'or' → 'and' ar permite whitespace-only instructor.
        not '   ' = False, dar not strip() = True → or → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "   ", 5, 10.0)

    def test_init_valid_max_spots_creates_object(self) -> None:
        """EC06: max_spots = 10 (în [1,30]) → obiect valid."""
        b = FitnessClassBooking("pilates", "Instructor", 10, 10.0)
        self.assertEqual(b.max_spots, 10)

    def test_init_max_spots_zero_raises_value_error(self) -> None:
        """EC07: max_spots = 0 (sub domeniu) → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 0, 10.0)

    def test_init_max_spots_over_limit_raises_value_error(self) -> None:
        """EC08: max_spots = 31 (peste domeniu) → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 31, 10.0)

    def test_init_max_spots_float_raises_value_error(self) -> None:
        """EC09: max_spots = 1.0 (float, nu int) → ValueError.
        isinstance(1.0, int) = False → not isinstance = True → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 1.0, 10.0)

    def test_init_max_spots_bool_false_raises_value_error(self) -> None:
        """EC10: max_spots = False (bool, echivalent cu 0) → ValueError.
        isinstance(False, int) = True, dar False == 0 < 1 → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", False, 10.0)

    def test_init_valid_price_creates_object(self) -> None:
        """EC11: price_per_session = 15.0 (> 0) → obiect valid."""
        b = FitnessClassBooking("zumba", "Instructor", 5, 15.0)
        self.assertAlmostEqual(b.price_per_session, 15.0)

    def test_init_zero_price_raises_value_error(self) -> None:
        """EC12: price_per_session = 0.0 (<= 0) → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("zumba", "Instructor", 5, 0.0)

    # ── book_spot ─────────────────────────────────────────────────────

    def test_book_spot_valid_client_confirmed(self) -> None:
        """EC13: client valid, loc disponibil → returnează 'confirmed'."""
        result = self.booking.book_spot("Ion Popescu")
        self.assertEqual(result, "confirmed")
        self.assertEqual(self.booking.booked_spots, 1)

    def test_book_spot_empty_client_name_raises_value_error(self) -> None:
        """EC14: client_name = '' → ValueError."""
        with self.assertRaises(ValueError):
            self.booking.book_spot("")

    def test_book_spot_class_full_adds_to_waitlist(self) -> None:
        """EC15: clasa plină, waitlist disponibil → returnează 'waitlist'."""
        for i in range(5):
            self.booking.book_spot(f"Client{i}")
        result = self.booking.book_spot("WaitlistClient")
        self.assertEqual(result, "waitlist")
        self.assertIn("WaitlistClient", self.booking.waitlist)

    def test_book_spot_waitlist_full_returns_rejected(self) -> None:
        """EC16: clasa plină, waitlist plin (5 persoane) → returnează 'rejected'."""
        for i in range(5):
            self.booking.book_spot(f"Confirmed{i}")
        for i in range(5):
            self.booking.book_spot(f"Waitlist{i}")
        result = self.booking.book_spot("Rejected")
        self.assertEqual(result, "rejected")

    # ── cancel_booking ────────────────────────────────────────────────

    def test_cancel_booking_confirmed_client_returns_true(self) -> None:
        """EC17: client cu rezervare confirmată → returnează True, spot eliberat."""
        self.booking.book_spot("Alice")
        result = self.booking.cancel_booking("Alice")
        self.assertTrue(result)
        self.assertEqual(self.booking.booked_spots, 0)

    def test_cancel_booking_waitlist_client_returns_true(self) -> None:
        """EC18: client pe waitlist → returnează True, eliminat din waitlist."""
        for i in range(5):
            self.booking.book_spot(f"C{i}")
        self.booking.book_spot("WaitingBob")
        result = self.booking.cancel_booking("WaitingBob")
        self.assertTrue(result)
        self.assertNotIn("WaitingBob", self.booking.waitlist)

    def test_cancel_booking_unknown_client_returns_false(self) -> None:
        """EC19: client negăsit → returnează False."""
        result = self.booking.cancel_booking("Nobody")
        self.assertFalse(result)

    # ── calculate_cost ────────────────────────────────────────────────

    def test_calculate_cost_valid_sessions_no_membership(self) -> None:
        """EC20: sessions=5, fără membership → cost de bază = 5 × 10.0 = 50.0."""
        cost = self.booking.calculate_cost(5, False)
        self.assertAlmostEqual(cost, 50.0)

    def test_calculate_cost_sessions_zero_raises_value_error(self) -> None:
        """EC21: sessions=0 (sub domeniu [1,20]) → ValueError."""
        with self.assertRaises(ValueError):
            self.booking.calculate_cost(0, False)

    def test_calculate_cost_sessions_over_limit_raises_value_error(self) -> None:
        """EC22: sessions=21 (peste domeniu [1,20]) → ValueError."""
        with self.assertRaises(ValueError):
            self.booking.calculate_cost(21, False)

    def test_calculate_cost_with_membership_applies_20_percent_discount(self) -> None:
        """EC23: sessions=5, cu membership → 5 × 10.0 × 0.80 = 40.0."""
        cost = self.booking.calculate_cost(5, True)
        self.assertAlmostEqual(cost, 40.0)

    def test_calculate_cost_sessions_ten_no_membership_applies_volume_discount(self) -> None:
        """EC24: sessions=10, fără membership → 10 × 10.0 × 0.90 = 90.0."""
        cost = self.booking.calculate_cost(10, False)
        self.assertAlmostEqual(cost, 90.0)

    def test_calculate_cost_sessions_ten_with_membership_applies_both_discounts(self) -> None:
        """EC25: sessions=10, cu membership → 10 × 10.0 × (1 − 0.30) = 70.0."""
        cost = self.booking.calculate_cost(10, True)
        self.assertAlmostEqual(cost, 70.0)

    def test_calculate_cost_non_integer_sessions_raises_value_error(self) -> None:
        """EC30: sessions="5" (str, non-int) → ValueError.
        Fără verificarea isinstance, "5" < 1 aruncă TypeError în loc de ValueError."""
        with self.assertRaises(ValueError):
            self.booking.calculate_cost("5", False)

    # ── Validări suplimentare de tip ──────────────────────────────────

    def test_init_non_string_instructor_raises_value_error(self) -> None:
        """EC26: instructor=123 (int, non-str) → ValueError.
        Fără verificarea isinstance, 123.strip() aruncă AttributeError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", 123, 5, 10.0)

    def test_init_non_numeric_price_raises_value_error(self) -> None:
        """EC27: price_per_session="10" (str) → ValueError.
        Fără verificarea isinstance, "10" <= 0 aruncă TypeError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, "10")

    def test_init_max_spots_bool_true_raises_value_error(self) -> None:
        """EC28: max_spots=True (bool, subclasă int, True==1) → ValueError.
        bool este subclasă de int, deci isinstance(True, int) = True și True >= 1,
        dar bool nu reprezintă o capacitate entitate validă; verificarea explicită
        isinstance(max_spots, bool) îl respinge înaintea celorlalte condiții."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", True, 10.0)

    def test_book_spot_non_string_client_name_raises_value_error(self) -> None:
        """EC29: client_name=123 (int, non-str) → ValueError.
        Fără verificarea isinstance, 123.strip() aruncă AttributeError."""
        with self.assertRaises(ValueError):
            self.booking.book_spot(123)


if __name__ == "__main__":
    unittest.main(verbosity=2)
