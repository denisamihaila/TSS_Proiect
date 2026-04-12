"""
test_independent_circuits.py – Basis Path Testing (McCabe).

Strategie: Se calculează complexitatea ciclomatică V(G) pentru fiecare metodă,
se construiește graful de flux de control (CFG) și se scrie câte un test
pentru fiecare circuit independent (cale de bază).

Proiect TSS – T1 | FitnessClassBooking
"""

# =============================================================================
# ANALIZA CFG ȘI COMPLEXITATE CICLOMATICĂ
# =============================================================================
#
# ─────────────────────────────────────────────────────────────────────────────
# METODA: book_spot(client_name)
# ─────────────────────────────────────────────────────────────────────────────
#
# Cod simplificat:
#   (1) if not client_name or not client_name.strip():  raise ValueError
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
# Cod simplificat (logica de business, excluzând garda de validare):
#   (1) cost = sessions * price_per_session
#   (2) if has_membership:   cost *= 0.80
#   (3) if sessions >= 10:   cost *= 0.90
#   (4) return round(cost, 2)
#
# Graf de flux de control (CFG):
#
#   N1 [intrare + compute base cost]
#    │
#    ▼
#   N2: if has_membership
#    │ True             │ False
#    ▼                  │
#   N3: cost *= 0.80    │
#    │                  │
#    └──────────────────┘
#                       │
#                       ▼
#                  N4: if sessions >= 10
#                   │ True         │ False
#                   ▼              │
#              N5: cost *= 0.90    │
#                   │              │
#                   └──────────────┘
#                                  │
#                             N6: return round(cost, 2)
#                                  │
#                               [Nexit]
#
# Calcul:
#   V(G) = nr_decizii_principale + 1 = 2 + 1 = 3
#   (Nota: validarea sessions < 1 or > 20 este o gardă separată
#    și nu face parte din logica algoritmică principală)
#
# Circuite independente (baza):
#   PATH_CC_1: N1→N2→N4→N6→Nexit      [D7=F, D8=F] → cost de bază
#   PATH_CC_2: N1→N2→N3→N4→N6→Nexit   [D7=T, D8=F] → 20% off
#   PATH_CC_3: N1→N2→N4→N5→N6→Nexit   [D7=F, D8=T] → 10% off
#   (Combinația D7=T, D8=T nu este un circuit independent nou în baza McCabe)
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
    Teste pentru cele V(G)=3 circuite independente ale metodei calculate_cost.
    """

    def setUp(self) -> None:
        # price_per_session = 10.0 pentru calcule simple
        self.b = FitnessClassBooking("pilates", "Ion Pop", 10, 10.0)

    def test_cc_path1_no_membership_below_10_sessions_base_cost(self) -> None:
        """
        Path PATH_CC_1: N1→N2(False)→N4(False)→N6→Nexit
        Condiție: has_membership=False (D7=F), sessions=5 < 10 (D8=F).
        Nicio reducere → cost = 5 × 10.0 = 50.0.
        Circuit acoperit: calea fără nicio reducere.
        """
        cost = self.b.calculate_cost(5, False)
        self.assertAlmostEqual(cost, 50.0)

    def test_cc_path2_with_membership_below_10_sessions_membership_discount(self) -> None:
        """
        Path PATH_CC_2: N1→N2(True)→N3→N4(False)→N6→Nexit
        Condiție: has_membership=True (D7=T), sessions=5 < 10 (D8=F).
        Reducere membership 20% → cost = 5 × 10.0 × 0.80 = 40.0.
        Circuit acoperit: calea cu doar reducere de membership.
        """
        cost = self.b.calculate_cost(5, True)
        self.assertAlmostEqual(cost, 40.0)

    def test_cc_path3_no_membership_ten_sessions_volume_discount(self) -> None:
        """
        Path PATH_CC_3: N1→N2(False)→N4(True)→N5→N6→Nexit
        Condiție: has_membership=False (D7=F), sessions=10 >= 10 (D8=T).
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
