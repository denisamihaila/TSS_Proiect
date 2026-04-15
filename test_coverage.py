"""
test_coverage.py – Acoperire instrucțiuni, decizii și condiții.

Conține 3 clase de test:
    TestStatementCoverage   – 100% acoperire la nivel de instrucțiune
    TestDecisionCoverage    – 100% acoperire la nivel de decizie (True+False)
    TestConditionCoverage   – acoperire la nivel de condiție (condiții compuse)

Proiect TSS – T1 | FitnessClassBooking
"""

import unittest
from fitness_class_booking import FitnessClassBooking


# =============================================================================
# TestStatementCoverage – Acoperire la nivel de instrucțiune (100%)
# =============================================================================

class TestStatementCoverage(unittest.TestCase):
    """
    Suită minimă de teste care execută FIECARE instrucțiune din
    fitness_class_booking.py cel puțin o dată.

    Instrucțiunile sunt grupate pe metode; fiecare test documentează
    ce linii / ramuri acoperă.
    """

    def setUp(self) -> None:
        # Acoperă: __init__ valid → toate assignment-urile
        self.b = FitnessClassBooking("yoga", "Ana Pop", 5, 10.0)

    # ── __init__ ──────────────────────────────────────────────────────

    # setUp acoperă deja __init__ cu argumente valide.

    def test_sc_init_invalid_class_name(self) -> None:
        """Acoperă: if class_name not in VALID_CLASSES → True → raise ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("boxing", "Instructor", 5, 10.0)

    def test_sc_init_empty_instructor(self) -> None:
        """Acoperă: if not instructor → True → raise ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "", 5, 10.0)

    def test_sc_init_invalid_max_spots(self) -> None:
        """Acoperă: if [max_spots invalid] → True → raise ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 0, 10.0)

    def test_sc_init_invalid_price(self) -> None:
        """Acoperă: if price_per_session <= 0 → True → raise ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, -1.0)

    # ── book_spot ─────────────────────────────────────────────────────

    def test_sc_book_spot_empty_name_raises(self) -> None:
        """Acoperă: if not client_name → True → raise ValueError."""
        with self.assertRaises(ValueError):
            self.b.book_spot("")

    def test_sc_book_spot_confirmed(self) -> None:
        """Acoperă: client = strip(), if booked < max → True,
        append confirmed, increment, return 'confirmed'."""
        result = self.b.book_spot("Alice")
        self.assertEqual(result, "confirmed")

    def test_sc_book_spot_waitlist(self) -> None:
        """Acoperă: if booked < max → False, elif len(waitlist) < 5 → True,
        append waitlist, return 'waitlist'."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        result = self.b.book_spot("WClient")
        self.assertEqual(result, "waitlist")

    def test_sc_book_spot_rejected(self) -> None:
        """Acoperă: elif len(waitlist) < 5 → False → return 'rejected'."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        for i in range(5):
            self.b.book_spot(f"W{i}")
        result = self.b.book_spot("Rejected")
        self.assertEqual(result, "rejected")

    # ── cancel_booking ────────────────────────────────────────────────

    def test_sc_cancel_confirmed_no_waitlist(self) -> None:
        """Acoperă: name = strip(), if name in confirmed → True,
        remove, decrement, if waitlist → False, return True."""
        self.b.book_spot("Alice")
        result = self.b.cancel_booking("Alice")
        self.assertTrue(result)

    def test_sc_cancel_confirmed_with_waitlist_promotion(self) -> None:
        """Acoperă: if waitlist → True, pop, append promoted, increment."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        self.b.book_spot("Waitlisted")
        self.b.cancel_booking("C0")
        self.assertIn("Waitlisted", self.b._confirmed)

    def test_sc_cancel_waitlist_client(self) -> None:
        """Acoperă: if name in confirmed → False, elif name in waitlist → True,
        remove from waitlist, return True."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        self.b.book_spot("WClient")
        result = self.b.cancel_booking("WClient")
        self.assertTrue(result)

    def test_sc_cancel_not_found(self) -> None:
        """Acoperă: elif name in waitlist → False → return False."""
        result = self.b.cancel_booking("Ghost")
        self.assertFalse(result)

    # ── calculate_cost ────────────────────────────────────────────────

    def test_sc_calculate_cost_invalid_sessions(self) -> None:
        """Acoperă: if sessions < 1 or sessions > 20 → True → raise ValueError."""
        with self.assertRaises(ValueError):
            self.b.calculate_cost(0, False)

    def test_sc_calculate_cost_no_discounts(self) -> None:
        """Acoperă: cost = sessions × price, if has_membership → False,
        if sessions >= 10 → False, return round(cost, 2)."""
        cost = self.b.calculate_cost(5, False)
        self.assertAlmostEqual(cost, 50.0)

    def test_sc_calculate_cost_membership_discount(self) -> None:
        """Acoperă: if has_membership → True → cost *= 0.80."""
        cost = self.b.calculate_cost(5, True)
        self.assertAlmostEqual(cost, 40.0)

    def test_sc_calculate_cost_volume_discount(self) -> None:
        """Acoperă: if sessions >= 10 → True → cost *= 0.90."""
        cost = self.b.calculate_cost(10, False)
        self.assertAlmostEqual(cost, 90.0)


# =============================================================================
# TestDecisionCoverage – Acoperire la nivel de decizie
# =============================================================================

class TestDecisionCoverage(unittest.TestCase):
    """
    Fiecare decizie (if/elif/else) este testată cu ambele ramuri: True și False.

    Decizii identificate:
    ─────────────────────────────────────────────────────────────────────────
    book_spot (3 decizii):
        D1: if not client_name or not client_name.strip()
        D2: if self.booked_spots < self.max_spots
        D3: elif len(self.waitlist) < MAX_WAITLIST_SIZE

    cancel_booking (3 decizii):
        D4: if name in self._confirmed
        D5: if self.waitlist  (ramura waitlist din confirmed)
        D6: elif name in self.waitlist

    calculate_cost (2 decizii în logica de business):
        D7: if has_membership
        D8: if sessions >= 10
    ─────────────────────────────────────────────────────────────────────────
    """

    def setUp(self) -> None:
        self.b = FitnessClassBooking("yoga", "Ana Pop", 5, 10.0)

    # ── D1: if not client_name or not client_name.strip() ─────────────

    def test_dc_book_spot_D1_true_empty_name_raises(self) -> None:
        """Decision D1 → True: client_name='' → not '' = True → ValueError."""
        with self.assertRaises(ValueError):
            self.b.book_spot("")

    def test_dc_book_spot_D1_false_valid_name_continues(self) -> None:
        """Decision D1 → False: client_name='Alice' → condiție False → continuă."""
        result = self.b.book_spot("Alice")
        self.assertEqual(result, "confirmed")

    # ── D2: if self.booked_spots < self.max_spots ─────────────────────

    def test_dc_book_spot_D2_true_free_spot_confirmed(self) -> None:
        """Decision D2 → True: booked(0) < max(5) → True → 'confirmed'."""
        result = self.b.book_spot("Bob")
        self.assertEqual(result, "confirmed")

    def test_dc_book_spot_D2_false_class_full_continues(self) -> None:
        """Decision D2 → False: booked(5) < max(5) → False → trece la D3."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        result = self.b.book_spot("Overflow")
        self.assertIn(result, ("waitlist", "rejected"))

    # ── D3: elif len(self.waitlist) < MAX_WAITLIST_SIZE ───────────────

    def test_dc_book_spot_D3_true_waitlist_available(self) -> None:
        """Decision D3 → True: len(waitlist)(0) < 5 → True → 'waitlist'."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        result = self.b.book_spot("WClient")
        self.assertEqual(result, "waitlist")

    def test_dc_book_spot_D3_false_waitlist_full_rejected(self) -> None:
        """Decision D3 → False: len(waitlist)(5) < 5 → False → 'rejected'."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        for i in range(5):
            self.b.book_spot(f"W{i}")
        result = self.b.book_spot("Rejected")
        self.assertEqual(result, "rejected")

    # ── D4: if name in self._confirmed ────────────────────────────────

    def test_dc_cancel_D4_true_confirmed_client_returns_true(self) -> None:
        """Decision D4 → True: 'Alice' în confirmed → True → spot eliberat."""
        self.b.book_spot("Alice")
        result = self.b.cancel_booking("Alice")
        self.assertTrue(result)

    def test_dc_cancel_D4_false_not_confirmed_checks_waitlist(self) -> None:
        """Decision D4 → False: 'Ghost' nu este în confirmed → continuă la D6."""
        result = self.b.cancel_booking("Ghost")
        self.assertFalse(result)

    # ── D5: if self.waitlist ───────────────────────────────────────────

    def test_dc_cancel_D5_true_promotes_from_waitlist(self) -> None:
        """Decision D5 → True: waitlist non-gol → primul promovat la confirmed."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        self.b.book_spot("WClient")
        self.b.cancel_booking("C0")
        self.assertIn("WClient", self.b._confirmed)

    def test_dc_cancel_D5_false_no_promotion(self) -> None:
        """Decision D5 → False: waitlist gol → nicio promovare, booked_spots scade."""
        self.b.book_spot("Alice")
        self.b.cancel_booking("Alice")
        self.assertEqual(self.b.booked_spots, 0)
        self.assertEqual(len(self.b.waitlist), 0)

    # ── D6: elif name in self.waitlist ────────────────────────────────

    def test_dc_cancel_D6_true_waitlist_client_removed(self) -> None:
        """Decision D6 → True: client pe waitlist → eliminat, return True."""
        for i in range(5):
            self.b.book_spot(f"C{i}")
        self.b.book_spot("WClient")
        result = self.b.cancel_booking("WClient")
        self.assertTrue(result)
        self.assertNotIn("WClient", self.b.waitlist)

    def test_dc_cancel_D6_false_not_found_returns_false(self) -> None:
        """Decision D6 → False: client absent din ambele liste → return False."""
        result = self.b.cancel_booking("Nobody")
        self.assertFalse(result)

    # ── D7: if has_membership ─────────────────────────────────────────

    def test_dc_calculate_D7_true_membership_discount_applied(self) -> None:
        """Decision D7 → True: has_membership=True → cost × 0.80."""
        cost = self.b.calculate_cost(5, True)
        self.assertAlmostEqual(cost, 40.0)  # 5 × 10 × 0.80

    def test_dc_calculate_D7_false_no_membership_discount(self) -> None:
        """Decision D7 → False: has_membership=False → fără reducere membership."""
        cost = self.b.calculate_cost(5, False)
        self.assertAlmostEqual(cost, 50.0)  # 5 × 10

    # ── D8: if sessions >= 10 ─────────────────────────────────────────

    def test_dc_calculate_D8_true_volume_discount_applied(self) -> None:
        """Decision D8 → True: sessions=10 >= 10 → cost × 0.90."""
        cost = self.b.calculate_cost(10, False)
        self.assertAlmostEqual(cost, 90.0)  # 10 × 10 × 0.90

    def test_dc_calculate_D8_false_no_volume_discount(self) -> None:
        """Decision D8 → False: sessions=9 < 10 → fără reducere de volum."""
        cost = self.b.calculate_cost(9, False)
        self.assertAlmostEqual(cost, 90.0)  # 9 × 10, fără discount


# =============================================================================
# TestConditionCoverage – Acoperire la nivel de condiție
# =============================================================================

class TestConditionCoverage(unittest.TestCase):
    """
    Fiecare condiție atomică dintr-o decizie compusă este evaluată
    atât True cât și False, independent de celelalte.

    Condiții compuse identificate:
    ─────────────────────────────────────────────────────────────────────────
    __init__ – max_spots:
        `isinstance(max_spots, bool) OR not isinstance(max_spots, int) OR max_spots < 1 OR max_spots > 30`
        C_init_0  isinstance(max_spots, bool)    → True (True) | False (int 5)
        C_init_1  not isinstance(max_spots, int) → True (float 1.0) | False (int 5)
        C_init_2  max_spots < 1                  → True (0)         | False (5)
        C_init_3  max_spots > 30                 → True (31)        | False (5)
        (short-circuit OR: fiecare condiție e evaluată doar dacă toate precedentele = False)

    book_spot D1: `not isinstance(client_name, str)  OR  not client_name  OR  not client_name.strip()`
        C1pre  not isinstance(client_name, str)  → True (client_name=123) | False (client_name="x")
        C1a    not client_name                   → True (client_name="")   | False (client_name="x")
        C1b    not client_name.strip()           → True (client_name=" ")  | False (client_name="x")
        (short-circuit: C1a evaluată doar când C1pre=False; C1b evaluată când C1a=False)

    calculate_cost – combinații independente ale D7 și D8:
        Chiar dacă în cod sunt 2 if-uri separate, comportamentul final
        depinde de combinația ambelor condiții atomice.
        C2  has_membership=False, sessions<10   → fără discount
        C3  has_membership=True,  sessions<10   → doar discount membership
        C4  has_membership=False, sessions>=10  → doar discount volum
        C5  has_membership=True,  sessions>=10  → ambele discounturi
    ─────────────────────────────────────────────────────────────────────────
    """

    def setUp(self) -> None:
        self.b = FitnessClassBooking("yoga", "Ana Pop", 5, 10.0)

    # ── C_init_1: not isinstance(max_spots, int) ──────────────────────

    def test_cc_Cinit1_true_float_raises_value_error(self) -> None:
        """C_init_1=True: max_spots=1.0 (float) → not isinstance(1.0, int) = True
        → short-circuit OR → ValueError imediat, C_init_2..3 nu sunt evaluate."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 1.0, 10.0)

    def test_cc_Cinit1_false_int_evaluates_Cinit2(self) -> None:
        """C_init_1=False: max_spots=5 (int) → not isinstance(5, int) = False
        → C_init_2 este evaluată (5 < 1 = False → C_init_3 evaluată)."""
        b = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(b.max_spots, 5)

    # ── C_init_2: max_spots < 1 ───────────────────────────────────────

    def test_cc_Cinit2_true_zero_raises_value_error(self) -> None:
        """C_init_2=True: max_spots=0 → C_init_1=False (0 e int),
        0 < 1 = True → OR → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 0, 10.0)

    def test_cc_Cinit2_false_positive_evaluates_Cinit3(self) -> None:
        """C_init_2=False: max_spots=5 → 5 < 1 = False → C_init_3 evaluată."""
        b = FitnessClassBooking("yoga", "Instructor", 5, 10.0)
        self.assertEqual(b.max_spots, 5)

    # ── C_init_3: max_spots > 30 ──────────────────────────────────────

    def test_cc_Cinit3_true_over_limit_raises_value_error(self) -> None:
        """C_init_3=True: max_spots=31 → C_init_1=False, C_init_2=False,
        31 > 30 = True → OR → ValueError."""
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 31, 10.0)

    def test_cc_Cinit3_false_all_conditions_false_valid(self) -> None:
        """C_init_3=False: max_spots=30 → toate condițiile False → obiect creat.
        Aceasta este singura combinație în care întreaga condiție compusă = False."""
        b = FitnessClassBooking("yoga", "Instructor", 30, 10.0)
        self.assertEqual(b.max_spots, 30)

    # ── C1a: not client_name ──────────────────────────────────────────

    def test_cc_C1a_true_empty_string_raises(self) -> None:
        """C1a=True: client_name='' → not '' = True → ValueError (short-circuit).
        C1b nu este evaluată."""
        with self.assertRaises(ValueError):
            self.b.book_spot("")

    def test_cc_C1a_false_nonempty_evaluates_C1b(self) -> None:
        """C1a=False: client_name='Alice' → not 'Alice' = False → C1b este evaluată."""
        result = self.b.book_spot("Alice")
        self.assertEqual(result, "confirmed")

    # ── C1b: not client_name.strip() ─────────────────────────────────

    def test_cc_C1b_true_whitespace_only_raises(self) -> None:
        """C1b=True: client_name='   ' → strip()='' → not '' = True → ValueError.
        C1a=False (string nevid), deci C1b este evaluată."""
        with self.assertRaises(ValueError):
            self.b.book_spot("   ")

    def test_cc_C1b_false_has_content_continues(self) -> None:
        """C1b=False: client_name='Bob' → strip()='Bob' → not 'Bob' = False → continuă."""
        result = self.b.book_spot("Bob")
        self.assertEqual(result, "confirmed")

    # ── Combinații C2–C5: has_membership × sessions>=10 ─────────────

    def test_cc_C2_no_membership_sessions_below_10_no_discounts(self) -> None:
        """C2: has_membership=False (D7=False) ∧ sessions<10 (D8=False).
        Nicio reducere aplicată → cost = 5 × 10 = 50.0."""
        cost = self.b.calculate_cost(5, False)
        self.assertAlmostEqual(cost, 50.0)

    def test_cc_C3_membership_sessions_below_10_only_membership_discount(self) -> None:
        """C3: has_membership=True (D7=True) ∧ sessions<10 (D8=False).
        Doar reducerea membership (20%) → cost = 5 × 10 × 0.80 = 40.0."""
        cost = self.b.calculate_cost(5, True)
        self.assertAlmostEqual(cost, 40.0)

    def test_cc_C4_no_membership_sessions_ten_only_volume_discount(self) -> None:
        """C4: has_membership=False (D7=False) ∧ sessions>=10 (D8=True).
        Doar reducerea de volum (10%) → cost = 10 × 10 × 0.90 = 90.0."""
        cost = self.b.calculate_cost(10, False)
        self.assertAlmostEqual(cost, 90.0)

    def test_cc_C5_membership_sessions_ten_both_discounts_applied(self) -> None:
        """C5: has_membership=True (D7=True) ∧ sessions>=10 (D8=True).
        Ambele reduceri aditiv → cost = 10 × 10 × (1 − 0.30) = 70.0."""
        cost = self.b.calculate_cost(10, True)
        self.assertAlmostEqual(cost, 70.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
