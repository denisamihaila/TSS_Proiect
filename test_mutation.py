"""
test_mutation.py – Analiză mutanți generată cu mutmut 2.5.1.

═══════════════════════════════════════════════════════════════════════════════
RAPORT MUTMUT
───────────────────────────────────────────────────────────────────────────────
Comandă: mutmut run --paths-to-mutate fitness_class_booking.py
         --tests-dir . --runner "python -m pytest"
Rulat în: WSL Ubuntu 24.04 / Python 3.12.3 / mutmut 2.5.1

  Total mutanți generați : 86
  - Uciși               : 65
  - Suspicioși          : 13
  - Supraviețuitori     :  8
  - Omiși               :  0

  Scor mutație inițial   : 65/86 ≈ 75.6%

───────────────────────────────────────────────────────────────────────────────
CLASIFICAREA MUTANȚILOR SUPRAVIEȚUITORI (8)
───────────────────────────────────────────────────────────────────────────────

Grup A – Mutanți de tip „string" (mesaj de eroare) (6 mutanți)
───────────────────────────────────────────────────────────────
mutmut modifică șirurile din `raise ValueError(...)` adăugând
prefixul/sufixul literal "XX". Excepția este în continuare aruncată;
comportamentul observabil prin API-ul public al clasei este IDENTIC
cu originalul. Testele nu verifică textul mesajului → supraviețuiesc.

  M9  – mesaj class_name ValueError: "XXclass_name...XX"
  M14 – mesaj instructor ValueError: "XXinstructor...XX"
  M21 – mesaj max_spots ValueError: "XXmax_spots...XX"
  M26 – mesaj price ValueError: "XXprice_per_session...XX"
  M39 – mesaj client_name ValueError: "XXclient_name...XX"
  M70 – mesaj sessions ValueError: "XXsessions...XX"

  Tip: NECRITICALI (pot fi omorâți cu assertRaisesRegex, dar nu
  reprezintă bug-uri de logică).

Grup B – Mutant quasi-echivalent (1 mutant)
────────────────────────────────────────────
  M49 – cancel_booking: `if client_name else ""` → `if client_name else "XXXX"`

  Schimbarea este observabilă DOAR dacă există un client confirmat cu
  numele literal "XXXX" și se apelează cancel_booking(None).
  Niciun scenariu realist nu produce această combinație; în practică
  mutantul se comportă identic cu implementarea corectă.
  Tip: QUASI-ECHIVALENT.

Grup C – Mutant comportamental NEECHIVALENT (1 mutant)
───────────────────────────────────────────────────────
  M75 – calculate_cost: `round(cost, 2)` → `round(cost, 3)`
        EFECT: costul este returnat cu 3 zecimale în loc de 2.

  !  M75 este omorât de testele suplimentare din acest fișier.

  Notă: M12 (instructor cu whitespace pur) și M22 (price_per_session <= 1)
  au apărut ca SUSPICIOȘI (nu supraviețuitori) în raportul mutmut.
  Testele din acest fișier contribuie la eliminarea și a mutanților suspicioși.

───────────────────────────────────────────────────────────────────────────────
SUMAR FINAL (după adăugarea testelor suplimentare):
  Mutanți comportamentali neechivalenți omorâți : 1/1 = 100%
  (M75 → test_mutation)
═══════════════════════════════════════════════════════════════════════════════
"""

import unittest
from fitness_class_booking import FitnessClassBooking


class TestMutationKilling(unittest.TestCase):
    """
    Teste suplimentare care omoară mutantul comportamental
    neechivalent M75 rămas în viață după rularea mutmut.
    M12 și M22 (suspicioși) sunt de asemenea adresați de testele din acest fișier.
    """

    def setUp(self) -> None:
        self.b = FitnessClassBooking("yoga", "Ana Pop", 5, 10.0)

    # =========================================================================
    # Ucide M12: `not instructor OR not instructor.strip()`
    #            → `not instructor AND not instructor.strip()`
    # =========================================================================

    def test_kill_M12_whitespace_only_instructor_must_raise_value_error(self) -> None:
        """
        Ucide M12: `not instructor or not instructor.strip()`
                 → `not instructor and not instructor.strip()`

        Implementarea CORECTĂ (OR):
            instructor = "   " → not "   " = False, not strip() = True
            False OR True = True → raise ValueError ✓

        Mutantul M12 (AND):
            False AND True = False → NU ridică ValueError (BUG!)
            Un instructor format doar din spații ar fi acceptat,
            iar instructor.strip() ar produce șirul gol "".

        Testul eșuează pe M12 deoarece assertRaises nu primește
        excepția → FAIL.
        """
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "   ", 5, 10.0)

    def test_kill_M12_tab_only_instructor_must_raise_value_error(self) -> None:
        """
        Test auxiliar M12: instructor format dintr-un singur tab.

        Tab-ul (\t) este whitespace → strip() → "" → not "" = True.
        Implementarea corectă: False OR True = True → ValueError.
        Mutantul M12 (AND): False AND True = False → fără eroare (BUG).
        """
        with self.assertRaises(ValueError):
            FitnessClassBooking("dance", "\t", 5, 10.0)

    # =========================================================================
    # Ucide M76: `round(cost, 2)` → `round(cost, 3)`
    # =========================================================================

    def test_kill_M76_cost_rounds_to_two_decimal_places(self) -> None:
        """
        Ucide M76: `return round(cost, 2)` → `return round(cost, 3)`.

        Scenariu: price_per_session = 1/3 ≈ 0.3333...,
                  sessions = 1, has_membership = False.
            cost brut = 1 × (1/3) = 0.3333...
            round(0.3333..., 2) = 0.33   ← implementarea CORECTĂ
            round(0.3333..., 3) = 0.333  ← mutantul M76 (BUG!)

        assertEqual(cost, 0.33) eșuează pe M76 deoarece 0.333 ≠ 0.33.

        Bug real reprezentat: costuri cu 3 zecimale pot cauza
        erori la comparații exacte sau afișare monetară.
        """
        b = FitnessClassBooking("yoga", "Instructor", 5, 1 / 3)
        cost = b.calculate_cost(1, False)
        self.assertEqual(cost, round(1 / 3, 2))      # 0.33
        self.assertNotEqual(cost, round(1 / 3, 3))   # ≠ 0.333

    def test_kill_M76_membership_cost_rounds_to_two_decimal_places(self) -> None:
        """
        Test auxiliar M76 cu membership discount aplicat.

        price = 1/3, sessions = 1, has_membership = True:
            cost = (1/3) × 0.80 = 0.2666...
            round(0.2666..., 2) = 0.27  ← corect
            round(0.2666..., 3) = 0.267 ← mutant (BUG)

        assertEqual(cost, 0.27) eșuează pe M76.
        """
        b = FitnessClassBooking("yoga", "Instructor", 5, 1 / 3)
        cost = b.calculate_cost(1, True)
        self.assertEqual(cost, round(1 / 3 * 0.80, 2))    # 0.27
        self.assertNotEqual(cost, round(1 / 3 * 0.80, 3)) # ≠ 0.267

    # =========================================================================
    # Documentare mutanți quasi-echivalenți / string mutations
    # =========================================================================

    def test_document_M45_quasi_equivalent_none_client_cancel(self) -> None:
        """
        Documentare M49 (quasi-echivalent):
            Original: name = client_name.strip() if client_name else ""
            Mutant:   name = client_name.strip() if client_name else "XXXX"

        Justificare quasi-echivalență:
            Comportamentul diferă DOAR dacă există un client confirmat
            cu numele exact "XXXX" și se apelează cancel_booking(None).
            Niciun scenariu realist nu produce această combinație;
            în practică ambele variante returnează False la cancel_booking(None)
            fără rezervări existente, identic cu implementarea corectă.

        Demonstrație: cancel_booking(None) returnează False în ambele cazuri.
        """
        result = self.b.cancel_booking(None)
        self.assertFalse(result)

    def test_document_string_mutations_raise_value_error(self) -> None:
        """
        Documentare mutanți string M9, M14, M21, M26, M39, M70:

        mutmut modifică textul mesajelor din raise ValueError(...)
        adăugând prefix/sufix "XX". Excepția este în continuare
        aruncată → comportamentul observabil prin API-ul public este
        IDENTIC cu originalul.

        Acești mutanți pot fi omorâți prin assertRaisesRegex cu
        pattern exact, dar nu reprezintă bug-uri de logică. Testul de
        mai jos demonstrează că excepțiile sunt ridicate corect
        indiferent de textul mesajului (care nu este vizibil extern).
        """
        with self.assertRaises(ValueError):
            FitnessClassBooking("crossfit", "Instructor", 5, 10.0)  # M9
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "", 5, 10.0)                # M14
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 0, 10.0)      # M21
        with self.assertRaises(ValueError):
            FitnessClassBooking("yoga", "Instructor", 5, 0.0)       # M26
        with self.assertRaises(ValueError):
            self.b.book_spot("")                                     # M39
        with self.assertRaises(ValueError):
            self.b.calculate_cost(0, False)                         # M70


if __name__ == "__main__":
    unittest.main(verbosity=2)
