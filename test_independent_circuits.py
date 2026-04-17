"""
Basis Path Testing (McCabe).

Strategie: Se calculează complexitatea ciclomatică V(G) pentru fiecare metodă,
se construiește graful de flux de control (CFG) și se scrie câte un test
pentru fiecare circuit independent (cale de bază).
"""

# =============================================================================
# ANALIZA CFG ȘI COMPLEXITATE CICLOMATICĂ
# =============================================================================
#
# ─────────────────────────────────────────────────────────────────────────────
# METODA: __init__(class_name, instructor, max_spots, price_per_session)
# ─────────────────────────────────────────────────────────────────────────────
#
# Cod simplificat (fiecare condiție compusă tratată ca o singură decizie):
#   (1) if class_name not in VALID_CLASSES:                        raise ValueError
#   (2) if not instructor or not instructor.strip():                raise ValueError
#   (3) if not isinstance(max_spots,int) or max_spots<1 or >30:    raise ValueError
#   (4) if price_per_session <= 0:                                  raise ValueError
#   (5) self.class_name = ...; self.instructor = ...; ...          [assignments]
#
# Graf de flux de control (CFG):
#
#   N1 [intrare]
#    │
#    ▼
#   N2: if class_name not in VALID_CLASSES
#    │ True             │ False
#    ▼                  ▼
#   N3: raise       N4: if not instructor or not instructor.strip()
#   ValueError       │ True             │ False
#    │               ▼                  ▼
#    │           N5: raise         N6: if [max_spots invalid]
#    │           ValueError         │ True        │ False
#    │               │              ▼              ▼
#    │               │         N7: raise     N8: if price_per_session <= 0
#    │               │         ValueError     │ True        │ False
#    │               │              │         ▼             ▼
#    │               │              │    N9: raise     N10: assignments
#    │               │              │    ValueError        │
#    └───────────────┴──────────────┴─────────────────────┘
#                                                          │
#                                                       [Nexit]
#
# Calcul:
#   Decizii: D1 (N2), D2 (N4), D3 (N6), D4 (N8) → V(G) = 4 + 1 = 5
#
# Circuite independente (baza):
#   PATH_INIT_1: N1→N2(T)→N3→Nexit              [D1=T]              → ValueError class_name
#   PATH_INIT_2: N1→N2(F)→N4(T)→N5→Nexit        [D1=F, D2=T]        → ValueError instructor
#   PATH_INIT_3: N1→N2(F)→N4(F)→N6(T)→N7→Nexit  [D1=F, D2=F, D3=T] → ValueError max_spots
#   PATH_INIT_4: N1→N2(F)→N4(F)→N6(F)→N8(T)→N9→Nexit [D1..3=F,D4=T]→ ValueError price
#   PATH_INIT_5: N1→N2(F)→N4(F)→N6(F)→N8(F)→N10→Nexit [toate=F]    → obiect creat
#
# ─────────────────────────────────────────────────────────────────────────────
#
# ─────────────────────────────────────────────────────────────────────────────
# METODA: book_spot(client_name)
# ─────────────────────────────────────────────────────────────────────────────
#
# Cod simplificat:
#   (1) if not isinstance(client_name, str) or not client_name or not client_name.strip():  raise ValueError
#   (2) client = client_name.strip()
#   (3) if self.booked_spots < self.max_spots:
#           return "confirmed"
#   (4) elif len(self.waitlist) < MAX_WAITLIST_SIZE:
#           return "waitlist"
#   (5) else:
#           return "rejected"
#
# Graf de flux de control (CFG):
#
#   N1 [intrare]
#    │
#    ▼
#   N2: if not client_name or not client_name.strip()
#    │ True                           │ False
#    ▼                                ▼
#   N3: raise ValueError            N4: client = strip()
#    │                               │
#    │                               ▼
#    │                         N5: if booked_spots < max_spots
#    │                          │ True              │ False
#    │                          ▼                   ▼
#    │                    N6: return          N7: if len(waitlist) < 5
#    │                    "confirmed"          │ True        │ False
#    │                          │              ▼             ▼
#    │                          │        N8: return    N9: return
#    │                          │        "waitlist"    "rejected"
#    │                          │              │             │
#    └──────────────────────────┴──────────────┴─────────────┘
#                                              │
#                                           [Nexit]
#
# Calcul:
#   Noduri   N = 9  (N1–N9 fără Nexit), cu Nexit → N = 9, dar ca graf N = 9+1 = 10 cu exit
#   Alternativ simplu: V(G) = număr_decizii + 1 = 3 + 1 = 4
#
#   Decizii: D1 (N2), D2 (N5), D3 (N7) → V(G) = 4
#
# Circuite independente (baza):
#   PATH_BS_1: N1→N2→N3→Nexit            [D1=True]  → ValueError (client invalid)
#   PATH_BS_2: N1→N2→N4→N5→N6→Nexit     [D1=F,D2=T] → "confirmed"
#   PATH_BS_3: N1→N2→N4→N5→N7→N8→Nexit  [D1=F,D2=F,D3=T] → "waitlist"
#   PATH_BS_4: N1→N2→N4→N5→N7→N9→Nexit  [D1=F,D2=F,D3=F] → "rejected"
#
# ─────────────────────────────────────────────────────────────────────────────
# METODA: calculate_cost(sessions, has_membership)
# ─────────────────────────────────────────────────────────────────────────────
#
# Cod complet (inclusiv garda de validare):
#   (1) if not isinstance(sessions,int) or isinstance(sessions,bool)
#       or sessions < 1 or sessions > 20:  raise ValueError    ← D_guard
#   (2) cost = sessions * price_per_session
#   (3) discount = 0.0
#   (4) if has_membership:   discount += 0.20                  ← D7
#   (5) if sessions >= 10:   discount += 0.10                  ← D8
#   (6) return round(cost * (1 - discount), 2)
#
# Graf de flux de control (CFG):
#
#   N1 [intrare]
#    │
#    ▼
#   N2: if [sessions invalid]   ← D_guard
#    │ True             │ False
#    ▼                  ▼
#   N3: raise      N4: cost = sessions × price; discount = 0.0
#   ValueError          │
#    │                  ▼
#    │             N5: if has_membership   ← D7
#    │              │ True    │ False
#    │              ▼         │
#    │         N6: discount   │
#    │             += 0.20    │
#    │              └────┬────┘
#    │                   ▼
#    │             N7: if sessions >= 10   ← D8
#    │              │ True    │ False
#    │              ▼         │
#    │         N8: discount   │
#    │             += 0.10    │
#    │              └────┬────┘
#    │                   ▼
#    │             N9: return round(cost × (1−discount), 2)
#    │                   │
#    └───────────────────┘
#                        │
#                     [Nexit]
#
# Calcul:
#   Decizii: D_guard (N2), D7 (N5), D8 (N7) → V(G) = 3 + 1 = 4
#   Garda de validare (N2) este o decizie reală din metodă și se include
#   în CFG; a o exclude ar subevalua complexitatea metodei.
#
# Circuite independente (baza):
#   PATH_CC_1: N1→N2(T)→N3→Nexit                    [D_guard=T]          → ValueError
#   PATH_CC_2: N1→N2(F)→N4→N5(F)→N7(F)→N9→Nexit    [D_guard=F,D7=F,D8=F]→ cost de bază
#   PATH_CC_3: N1→N2(F)→N4→N5(T)→N6→N7(F)→N9→Nexit [D_guard=F,D7=T,D8=F]→ 20% off
#   PATH_CC_4: N1→N2(F)→N4→N5(F)→N7(T)→N8→N9→Nexit [D_guard=F,D7=F,D8=T]→ 10% off
#   (Combinația D7=T,D8=T nu generează un circuit nou independent în baza McCabe)
#
# ─────────────────────────────────────────────────────────────────────────────
# METODA: cancel_booking(client_name)
# ─────────────────────────────────────────────────────────────────────────────
#
# Cod simplificat:
#   (1) name = client_name.strip()
#   (2) if name in self._confirmed:
#           remove; booked_spots -= 1
#           (3) if self.waitlist:
#                   promote first from waitlist; booked_spots += 1
#           return True
#       (4) elif name in self.waitlist:
#               remove from waitlist
#               return True
#       else:
#           return False
#
# Decizii: D4 (name in confirmed), D5 (waitlist non-empty), D6 (name in waitlist)
# V(G) = 3 + 1 = 4
#
# Circuite independente (baza):
#   PATH_CB_1: confirmed=T, waitlist=F → cancels, no promotion, True
#   PATH_CB_2: confirmed=T, waitlist=T → cancels, promotes, True
#   PATH_CB_3: confirmed=F, waitlist=T → removes from waitlist, True
#   PATH_CB_4: confirmed=F, waitlist=F → not found, False
#
# =============================================================================

import unittest
from fitness_class_booking import FitnessClassBooking


class TestIndependentCircuitsBookSpot(unittest.TestCase):
    """
    Teste pentru cele V(G)=4 circuite independente ale metodei book_spot.
    """

    def setUp(self) -> None:
        self.b = FitnessClassBooking("yoga", "Ana Pop", 5, 10.0)

    def test_bs_path1_invalid_client_raises_value_error(self) -> None:
        """
        Path PATH_BS_1: N1→N2(True)→N3→Nexit
        Condiție: client_name='' → D1=True → raise ValueError.
        Circuit acoperit: calea excepției la validarea input-ului.
        """
        with self.assertRaises(ValueError):
            self.b.book_spot("")

    def test_bs_path2_free_spot_returns_confirmed(self) -> None:
        """
        Path PATH_BS_2: N1→N2(False)→N4→N5(True)→N6→Nexit
        Condiție: client valid (D1=F), booked_spots(0) < max_spots(5) (D2=T) → 'confirmed'.
        Circuit acoperit: calea fericită (loc liber disponibil).
        """
        result = self.b.book_spot("Alice")
        self.assertEqual(result, "confirmed")
        self.assertEqual(self.b.booked_spots, 1)

    def test_bs_path3_full_class_waitlist_available_returns_waitlist(self) -> None:
        """
        Path PATH_BS_3: N1→N2(False)→N4→N5(False)→N7(True)→N8→Nexit
        Condiție: client valid (D1=F), clasa plină (D2=F), waitlist<5 (D3=T) → 'waitlist'.
        Circuit acoperit: calea de adăugare pe lista de așteptare.
        """
        for i in range(5):
            self.b.book_spot(f"C{i}")
        result = self.b.book_spot("WClient")
        self.assertEqual(result, "waitlist")
        self.assertIn("WClient", self.b.waitlist)

    def test_bs_path4_full_class_full_waitlist_returns_rejected(self) -> None:
        """
        Path PATH_BS_4: N1→N2(False)→N4→N5(False)→N7(False)→N9→Nexit
        Condiție: client valid (D1=F), clasa plină (D2=F), waitlist=5 (D3=F) → 'rejected'.
        Circuit acoperit: calea refuzului complet.
        """
        for i in range(5):
            self.b.book_spot(f"C{i}")
        for i in range(5):
            self.b.book_spot(f"W{i}")
        result = self.b.book_spot("Rejected")
        self.assertEqual(result, "rejected")


class TestIndependentCircuitsCalculateCost(unittest.TestCase):
    """
    Teste pentru cele V(G)=4 circuite independente ale metodei calculate_cost.

    V(G) = 4 deoarece există 3 decizii reale în metodă:
      D_guard : if sessions < 1 or sessions > 20  (garda de validare)
      D7      : if has_membership
      D8      : if sessions >= 10
    V(G) = 3 + 1 = 4
    """

    def setUp(self) -> None:
        self.b = FitnessClassBooking("pilates", "Ion Pop", 10, 10.0)

    def test_cc_path1_invalid_sessions_raises_value_error(self) -> None:
        """
        Path PATH_CC_1: N1→N2(True)→N3→Nexit
        Condiție: sessions=0 → D_guard=True → raise ValueError.
        Circuit acoperit: calea excepției la garda de validare.
        """
        with self.assertRaises(ValueError):
            self.b.calculate_cost(0, False)

    def test_cc_path2_no_membership_below_10_sessions_base_cost(self) -> None:
        """
        Path PATH_CC_2: N1→N2(False)→N4→N5(False)→N7(False)→N9→Nexit
        Condiție: D_guard=F, has_membership=False (D7=F), sessions=5 < 10 (D8=F).
        Nicio reducere → cost = 5 × 10.0 = 50.0.
        Circuit acoperit: calea fără nicio reducere.
        """
        cost = self.b.calculate_cost(5, False)
        self.assertAlmostEqual(cost, 50.0)

    def test_cc_path3_with_membership_below_10_sessions_membership_discount(self) -> None:
        """
        Path PATH_CC_3: N1→N2(False)→N4→N5(True)→N6→N7(False)→N9→Nexit
        Condiție: D_guard=F, has_membership=True (D7=T), sessions=5 < 10 (D8=F).
        Reducere membership 20% → cost = 5 × 10.0 × 0.80 = 40.0.
        Circuit acoperit: calea cu doar reducere de membership.
        """
        cost = self.b.calculate_cost(5, True)
        self.assertAlmostEqual(cost, 40.0)

    def test_cc_path4_no_membership_ten_sessions_volume_discount(self) -> None:
        """
        Path PATH_CC_4: N1→N2(False)→N4→N5(False)→N7(True)→N8→N9→Nexit
        Condiție: D_guard=F, has_membership=False (D7=F), sessions=10 >= 10 (D8=T).
        Reducere volum 10% → cost = 10 × 10.0 × 0.90 = 90.0.
        Circuit acoperit: calea cu doar reducere de volum.
        """
        cost = self.b.calculate_cost(10, False)
        self.assertAlmostEqual(cost, 90.0)


class TestIndependentCircuitsCancelBooking(unittest.TestCase):
    """
    Teste pentru cele V(G)=4 circuite independente ale metodei cancel_booking.
    """

    def setUp(self) -> None:
        self.b = FitnessClassBooking("zumba", "Maria Pop", 5, 10.0)

    def test_cb_path1_confirmed_no_waitlist_cancels_returns_true(self) -> None:
        """
        Path PATH_CB_1: D4=True, D5=False → anulează confirmat, fără promovare.
        Condiție: client în confirmed (D4=T), waitlist gol (D5=F) → return True.
        booked_spots scade cu 1, waitlist rămâne gol.
        """
        self.b.book_spot("Alice")
        result = self.b.cancel_booking("Alice")
        self.assertTrue(result)
        self.assertEqual(self.b.booked_spots, 0)
        self.assertEqual(len(self.b.waitlist), 0)

    def test_cb_path2_confirmed_with_waitlist_promotes_returns_true(self) -> None:
        """
        Path PATH_CB_2: D4=True, D5=True → anulează confirmat, promovează din waitlist.
        Condiție: client în confirmed (D4=T), waitlist non-gol (D5=T) → promovare + True.
        Primul din waitlist devine confirmat automat.
        """
        for i in range(5):
            self.b.book_spot(f"C{i}")
        self.b.book_spot("WaitlistPerson")
        result = self.b.cancel_booking("C0")
        self.assertTrue(result)
        self.assertIn("WaitlistPerson", self.b._confirmed)
        self.assertEqual(len(self.b.waitlist), 0)
        self.assertEqual(self.b.booked_spots, 5)

    def test_cb_path3_waitlist_client_removed_returns_true(self) -> None:
        """
        Path PATH_CB_3: D4=False, D6=True → client pe waitlist, eliminat.
        Condiție: client absent din confirmed (D4=F), client în waitlist (D6=T) → True.
        """
        for i in range(5):
            self.b.book_spot(f"C{i}")
        self.b.book_spot("WClient")
        result = self.b.cancel_booking("WClient")
        self.assertTrue(result)
        self.assertNotIn("WClient", self.b.waitlist)

    def test_cb_path4_client_not_found_returns_false(self) -> None:
        """
        Path PATH_CB_4: D4=False, D6=False → client absent din ambele liste.
        Condiție: client absent din confirmed (D4=F) și din waitlist (D6=F) → False.
        """
        result = self.b.cancel_booking("GhostClient")
        self.assertFalse(result)


class TestIndependentCircuitsInit(unittest.TestCase):
    """
    Teste pentru cele V(G)=5 circuite independente ale metodei __init__.

    Fiecare test acoperă exact un circuit din baza McCabe,
    urmând structura CFG descrisă în antetul fișierului.
    """

    def test_init_path1_invalid_class_name_raises_value_error(self) -> None:
        """
        Path PATH_INIT_1: N1→N2(True)→N3→Nexit
        Condiție: class_name='crossfit' ∉ VALID_CLASSES (D1=True) → ValueError.
        Circuit acoperit: calea excepției la primul punct de validare.
        """
        with self.assertRaises(ValueError):
            FitnessClassBooking("crossfit", "Instructor", 5, 10.0)

    def test_init_path2_invalid_instructor_raises_value_error(self) -> None:
        """
        Path PATH_INIT_2: N1→N2(False)→N4(True)→N5→Nexit
        Condiție: class_name valid (D1=F), instructor='' → not ''=True (D2=T) → ValueError.
        Circuit acoperit: calea excepției la validarea instructor.
        """
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "", 5, 10.0)

    def test_init_path3_invalid_max_spots_raises_value_error(self) -> None:
        """
        Path PATH_INIT_3: N1→N2(False)→N4(False)→N6(True)→N7→Nexit
        Condiție: class_name valid (D1=F), instructor valid (D2=F),
                  max_spots=0 → max_spots < 1 = True (D3=T) → ValueError.
        Circuit acoperit: calea excepției la validarea max_spots.
        """
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 0, 10.0)

    def test_init_path4_invalid_price_raises_value_error(self) -> None:
        """
        Path PATH_INIT_4: N1→N2(F)→N4(F)→N6(F)→N8(True)→N9→Nexit
        Condiție: class_name valid (D1=F), instructor valid (D2=F),
                  max_spots valid (D3=F), price=0.0 → price <= 0 = True (D4=T) → ValueError.
        Circuit acoperit: calea excepției la validarea prețului.
        """
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, 0.0)

    def test_init_path5_all_valid_creates_object(self) -> None:
        """
        Path PATH_INIT_5: N1→N2(F)→N4(F)→N6(F)→N8(False)→N10→Nexit
        Condiție: toți parametrii valizi (toate deciziile False) → obiect creat.
        Circuit acoperit: calea fericită – toate validările trec.
        """
        b = FitnessClassBooking("pilates", "Maria Pop", 10, 25.0)
        self.assertEqual(b.class_name, "pilates")
        self.assertEqual(b.instructor, "Maria Pop")
        self.assertEqual(b.max_spots, 10)
        self.assertAlmostEqual(b.price_per_session, 25.0)
        self.assertEqual(b.booked_spots, 0)
        self.assertEqual(b.waitlist, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
