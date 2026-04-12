"""
test_boundary_value_analysis.py – Analiza valorilor de frontieră (BVA).

Strategie: Se testează exact la frontieră, imediat sub și imediat deasupra
fiecărei limite critice, deoarece bug-urile apar cel mai frecvent la granițe.

Proiect TSS – T1 | FitnessClassBooking
"""

import unittest
from fitness_class_booking import FitnessClassBooking


class TestBoundaryValueAnalysis(unittest.TestCase):
    """
    Analiza valorilor de frontieră pentru FitnessClassBooking.

    ═══════════════════════════════════════════════════════════════════
    FRONTIERE IDENTIFICATE
    ───────────────────────────────────────────────────────────────────
    __init__ – max_spots ∈ [1, 30]:
        Frontiera inferioară la 1:
            BVA01  max_spots = 0   (sub frontieră)   → ValueError
            BVA02  max_spots = 1   (la frontieră)    → valid
            BVA03  max_spots = 2   (peste frontieră) → valid
        Frontiera superioară la 30:
            BVA04  max_spots = 29  (sub frontieră)   → valid
            BVA05  max_spots = 30  (la frontieră)    → valid
            BVA06  max_spots = 31  (peste frontieră) → ValueError

    book_spot – tranziție confirmed → waitlist (la max_spots):
        Frontiera la booked_spots = max_spots:
            BVA07  booked_spots = max_spots - 1 → următoarea rezervare: "confirmed"
            BVA08  booked_spots = max_spots     → următoarea rezervare: "waitlist"

    book_spot – tranziție waitlist → rejected (la 5 persoane pe waitlist):
        Frontiera la len(waitlist) = 5:
            BVA09  len(waitlist) = 0  (primul pe waitlist)   → "waitlist"
            BVA10  len(waitlist) = 4  (al 5-lea pe waitlist) → "waitlist"
            BVA11  len(waitlist) = 5  (al 6-lea refuzat)     → "rejected"

    calculate_cost – sessions ∈ [1, 20]:
        Frontiera inferioară la 1:
            BVA12  sessions = 0   (sub frontieră)   → ValueError
            BVA13  sessions = 1   (la frontieră)    → valid, fără discount vol.
            BVA14  sessions = 2   (peste frontieră) → valid, fără discount vol.
        Tranziția discount volum la sessions = 10:
            BVA15  sessions = 9   (sub frontieră)   → fără discount de volum
            BVA16  sessions = 10  (la frontieră)    → cu discount de volum
            BVA17  sessions = 11  (peste frontieră) → cu discount de volum
        Frontiera superioară la 20:
            BVA18  sessions = 19  (sub frontieră)   → valid
            BVA19  sessions = 20  (la frontieră)    → valid
            BVA20  sessions = 21  (peste frontieră) → ValueError
    ═══════════════════════════════════════════════════════════════════
    """

    # ── __init__ – max_spots ──────────────────────────────────────────

    def test_init_max_spots_zero_raises_value_error(self) -> None:
        """BVA01: frontieră inferioară la 1; max_spots=0 (sub) → ValueError.
        Condiție: max_spots < 1."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 0, 10.0)

    def test_init_max_spots_one_is_valid(self) -> None:
        """BVA02: frontieră inferioară la 1; max_spots=1 (la) → valid.
        Condiție: max_spots >= 1, prima valoare acceptată."""
        b = FitnessClassBooking("yoga", "Instructor", 1, 10.0)
        self.assertEqual(b.max_spots, 1)

    def test_init_max_spots_two_is_valid(self) -> None:
        """BVA03: frontieră inferioară la 1; max_spots=2 (peste) → valid.
        Condiție: valoare imediat deasupra frontierei inferioare."""
        b = FitnessClassBooking("yoga", "Instructor", 2, 10.0)
        self.assertEqual(b.max_spots, 2)

    def test_init_max_spots_twenty_nine_is_valid(self) -> None:
        """BVA04: frontieră superioară la 30; max_spots=29 (sub) → valid.
        Condiție: valoare imediat sub frontiera superioară."""
        b = FitnessClassBooking("dance", "Instructor", 29, 10.0)
        self.assertEqual(b.max_spots, 29)

    def test_init_max_spots_thirty_is_valid(self) -> None:
        """BVA05: frontieră superioară la 30; max_spots=30 (la) → valid.
        Condiție: ultima valoare acceptată."""
        b = FitnessClassBooking("dance", "Instructor", 30, 10.0)
        self.assertEqual(b.max_spots, 30)

    def test_init_max_spots_thirty_one_raises_value_error(self) -> None:
        """BVA06: frontieră superioară la 30; max_spots=31 (peste) → ValueError.
        Condiție: max_spots > 30."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("dance", "Instructor", 31, 10.0)

    # ── book_spot – tranziție confirmed → waitlist ────────────────────

    def test_book_spot_one_spot_left_returns_confirmed(self) -> None:
        """BVA07: frontieră la max_spots; booked_spots = max_spots-1 = 4 → next: 'confirmed'.
        Condiție: booked_spots (4) < max_spots (5) este True → loc confirmat."""
        booking = FitnessClassBooking("pilates", "Instructor", 5, 10.0)
        for i in range(4):
            booking.book_spot(f"C{i}")
        # Al 5-lea: ultimul loc liber
        result = booking.book_spot("LastFree")
        self.assertEqual(result, "confirmed")
        self.assertEqual(booking.booked_spots, 5)

    def test_book_spot_class_full_goes_to_waitlist(self) -> None:
        """BVA08: frontieră la max_spots; booked_spots = max_spots = 5 → next: 'waitlist'.
        Condiție: booked_spots (5) < max_spots (5) este False → trece la elif."""
        booking = FitnessClassBooking("pilates", "Instructor", 5, 10.0)
        for i in range(5):
            booking.book_spot(f"C{i}")
        result = booking.book_spot("Overflow")
        self.assertEqual(result, "waitlist")

    # ── book_spot – tranziție waitlist → rejected ─────────────────────

    def test_book_spot_first_on_waitlist(self) -> None:
        """BVA09: frontieră la len(waitlist)=5; waitlist=0 (primul) → 'waitlist'.
        Condiție: len(waitlist) (0) < 5 este True."""
        booking = FitnessClassBooking("yoga", "Instructor", 2, 10.0)
        booking.book_spot("C1")
        booking.book_spot("C2")
        result = booking.book_spot("W1")
        self.assertEqual(result, "waitlist")
        self.assertEqual(len(booking.waitlist), 1)

    def test_book_spot_fifth_on_waitlist(self) -> None:
        """BVA10: frontieră la len(waitlist)=5; waitlist=4 (al 5-lea) → 'waitlist'.
        Condiție: len(waitlist) (4) < 5 este True, ultima adăugare permisă."""
        booking = FitnessClassBooking("yoga", "Instructor", 2, 10.0)
        booking.book_spot("C1")
        booking.book_spot("C2")
        for i in range(4):
            booking.book_spot(f"W{i}")
        result = booking.book_spot("W4")  # al 5-lea pe waitlist
        self.assertEqual(result, "waitlist")
        self.assertEqual(len(booking.waitlist), 5)

    def test_book_spot_sixth_on_waitlist_returns_rejected(self) -> None:
        """BVA11: frontieră la len(waitlist)=5; waitlist=5 (al 6-lea) → 'rejected'.
        Condiție: len(waitlist) (5) < 5 este False → rejected."""
        booking = FitnessClassBooking("yoga", "Instructor", 2, 10.0)
        booking.book_spot("C1")
        booking.book_spot("C2")
        for i in range(5):
            booking.book_spot(f"W{i}")
        result = booking.book_spot("Rejected")
        self.assertEqual(result, "rejected")

    # ── calculate_cost – frontiera inferioară sessions = 1 ───────────

    def test_calculate_cost_sessions_zero_raises_value_error(self) -> None:
        """BVA12: frontieră inferioară la 1; sessions=0 (sub) → ValueError.
        Condiție: sessions (0) < 1 este True."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        with self.assertRaises(ValueError):
            booking.calculate_cost(0, False)

    def test_calculate_cost_sessions_one_is_valid(self) -> None:
        """BVA13: frontieră inferioară la 1; sessions=1 (la) → cost = 1×10 = 10.0.
        Condiție: prima valoare acceptată, fără discount de volum."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        cost = booking.calculate_cost(1, False)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_cost_sessions_two_is_valid(self) -> None:
        """BVA14: frontieră inferioară la 1; sessions=2 (peste) → cost = 2×10 = 20.0.
        Condiție: valoare imediat deasupra frontierei inferioare."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        cost = booking.calculate_cost(2, False)
        self.assertAlmostEqual(cost, 20.0)

    # ── calculate_cost – tranziția discount volum la sessions = 10 ────

    def test_calculate_cost_sessions_nine_no_volume_discount(self) -> None:
        """BVA15: tranziție la 10; sessions=9 (sub) → fără discount volum.
        Condiție: sessions (9) >= 10 este False → nu se aplică reducerea de 10%."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        cost = booking.calculate_cost(9, False)
        self.assertAlmostEqual(cost, 90.0)  # 9 × 10 = 90.0, fără discount

    def test_calculate_cost_sessions_ten_applies_volume_discount(self) -> None:
        """BVA16: tranziție la 10; sessions=10 (la frontieră) → discount volum 10%.
        Condiție: sessions (10) >= 10 este True → se aplică reducerea de 10%."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        cost = booking.calculate_cost(10, False)
        self.assertAlmostEqual(cost, 90.0)  # 10 × 10 × 0.90 = 90.0

    def test_calculate_cost_sessions_eleven_applies_volume_discount(self) -> None:
        """BVA17: tranziție la 10; sessions=11 (peste) → discount volum 10%.
        Condiție: sessions (11) >= 10 este True."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        cost = booking.calculate_cost(11, False)
        self.assertAlmostEqual(cost, 99.0)  # 11 × 10 × 0.90 = 99.0

    # ── calculate_cost – frontiera superioară sessions = 20 ──────────

    def test_calculate_cost_sessions_nineteen_is_valid(self) -> None:
        """BVA18: frontieră superioară la 20; sessions=19 (sub) → valid.
        Condiție: valoare imediat sub frontiera superioară."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        cost = booking.calculate_cost(19, False)
        self.assertAlmostEqual(cost, 171.0)  # 19 × 10 × 0.90 = 171.0

    def test_calculate_cost_sessions_twenty_is_valid(self) -> None:
        """BVA19: frontieră superioară la 20; sessions=20 (la) → valid.
        Condiție: ultima valoare acceptată."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        cost = booking.calculate_cost(20, False)
        self.assertAlmostEqual(cost, 180.0)  # 20 × 10 × 0.90 = 180.0

    def test_calculate_cost_sessions_twenty_one_raises_value_error(self) -> None:
        """BVA20: frontieră superioară la 20; sessions=21 (peste) → ValueError.
        Condiție: sessions (21) > 20 este True."""
        booking = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        with self.assertRaises(ValueError):
            booking.calculate_cost(21, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
