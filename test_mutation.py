"""
test_mutation.py – Analiza mutanților (Mutation Testing).

Demonstrează strategia de testare prin mutanți: se modifică codul sursă în
moduri mici și se verifică că testele detectează modificările (omoară mutantul).

Proiect TSS – T1 | FitnessClassBooking

═══════════════════════════════════════════════════════════════════════════════
RAPORT MUTANȚI (simulat – tipic pentru mutmut pe această clasă)
───────────────────────────────────────────────────────────────────────────────

Mutant M1: `booked_spots < max_spots` → `booked_spots <= max_spots`
           Locație: book_spot(), decizia de confirmare
           Tip: NEECHIVALENT
           Efect: Când booked_spots = max_spots (clasa plină), condiția
                  `<=` devine True → rezervare „confirmată" incorect,
                  booked_spots depășește max_spots → bug real.

Mutant M2: `len(self.waitlist) < self.MAX_WAITLIST_SIZE` →
           `len(self.waitlist) <= self.MAX_WAITLIST_SIZE`
           Locație: book_spot(), decizia de waitlist
           Tip: NEECHIVALENT
           Efect: Când waitlist are 5 persoane, `<=` devine True → al 6-lea
                  client adăugat pe waitlist în loc să fie respins → bug real.

Mutant M3: `sessions >= 10` → `sessions > 10`
           Locație: calculate_cost(), decizia discount de volum
           Tip: NEECHIVALENT
           Efect: La sessions=10 nu se mai aplică reducerea de volum 10%
                  (10 > 10 = False) → client plătește mai mult → bug real.

Mutant M4: `cost *= 0.80` → `cost *= 0.90`
           Locație: calculate_cost(), aplicarea discount-ului de membership
           Tip: NEECHIVALENT
           Efect: Reducerea de membership devine 10% în loc de 20%
                  → client plătește mai mult decât ar trebui → bug real.

Mutant M5: `self.booked_spots -= 1` → `self.booked_spots = self.booked_spots - 1`
           Locație: cancel_booking(), decrementarea contorului
           Tip: ECHIVALENT
           Justificare: În Python, `a -= b` și `a = a - b` sunt semantically
           identice pentru tipul `int` (imutabil). Nicio secvență de apeluri
           de metodă nu poate distinge comportamentul celor două variante.
           Orice test valid obține același sold înainte și după anulare.

Mutant M6: `cost *= 0.90` → `cost = cost * 0.90`
           Locație: calculate_cost(), aplicarea discount-ului de volum
           Tip: ECHIVALENT
           Justificare: `*=` și `= ... *` pe `float` produc rezultat identic.
           Python evaluează `cost *= 0.90` ca `cost = cost.__imul__(0.90)` care,
           pentru float (tip imutabil), este echivalent cu `cost = cost * 0.90`.
           Nu există test care să distingă cele două forme.

───────────────────────────────────────────────────────────────────────────────
SUMAR:
    Mutanți generați:       6
    Neechivalenți (uciși):  4  (M1, M2, M3, M4)
    Echivalenți (vii):      2  (M5, M6)
    Scor mutație:           4/4 = 100% (excluzând echivalenții)
═══════════════════════════════════════════════════════════════════════════════
"""

import unittest
from fitness_class_booking import FitnessClassBooking


class TestMutationKilling(unittest.TestCase):
    """
    Teste care omoară cei 4 mutanți neechivalenți și documentează
    de ce cei 2 mutanți echivalenți nu pot fi omorâți.
    """

    def setUp(self) -> None:
        self.b = FitnessClassBooking("yoga", "Ana Pop", 5, 10.0)

    # =========================================================================
    # Ucide M1: `booked_spots < max_spots` → `booked_spots <= max_spots`
    # =========================================================================

    def test_kill_M1_full_class_next_booking_must_be_waitlist(self) -> None:
        """
        Ucide M1: `booked_spots < max_spots` → `booked_spots <= max_spots`.

        Implementarea CORECTĂ: când booked_spots = max_spots = 5,
            condiția  5 < 5  = False → merge la elif (waitlist). ✓

        Mutantul M1: condiția  5 <= 5 = True → returnează 'confirmed' (BUG!),
            booked_spots devine 6, depășind capacitatea de 5.

        Bug real reprezentat: suprarezervarae clasei; mai mulți clienți
        confirmați decât locuri fizice disponibile.

        Testul eșuează pe M1 deoarece assertEqual('waitlist', 'confirmed') → FAIL.
        """
        for i in range(5):
            self.b.book_spot(f"C{i}")
        self.assertEqual(self.b.booked_spots, 5)

        result = self.b.book_spot("OverflowClient")

        self.assertEqual(
            result,
            "waitlist",
            msg="Când clasa e plină (booked=max), rezervarea trebuie să fie 'waitlist', nu 'confirmed'",
        )
        # Pe mutant, booked_spots ar fi 6 (imposibil); implementarea corectă: rămâne 5
        self.assertEqual(self.b.booked_spots, 5)

    # =========================================================================
    # Ucide M2: `len(waitlist) < 5` → `len(waitlist) <= 5`
    # =========================================================================

    def test_kill_M2_full_waitlist_next_booking_must_be_rejected(self) -> None:
        """
        Ucide M2: `len(waitlist) < 5` → `len(waitlist) <= 5`.

        Implementarea CORECTĂ: când len(waitlist) = 5,
            condiția  5 < 5  = False → returnează 'rejected'. ✓

        Mutantul M2: condiția  5 <= 5 = True → adaugă pe waitlist (BUG!),
            waitlist-ul ajunge la 6 persoane (depășind limita).

        Bug real reprezentat: permite mai mult de 5 persoane pe waitlist,
        ceea ce încalcă politica de maxim 5 locuri pe lista de așteptare.

        Testul eșuează pe M2 deoarece assertEqual('rejected', 'waitlist') → FAIL.
        """
        # Umple clasa (5 confirmați)
        for i in range(5):
            self.b.book_spot(f"C{i}")
        # Umple waitlist-ul (5 pe waitlist)
        for i in range(5):
            self.b.book_spot(f"W{i}")

        self.assertEqual(len(self.b.waitlist), 5)

        result = self.b.book_spot("SixthWaitlist")

        self.assertEqual(
            result,
            "rejected",
            msg="Când waitlist e plin (5 persoane), rezervarea trebuie să fie 'rejected', nu 'waitlist'",
        )
        # Pe mutant, len(waitlist) ar fi 6; implementarea corectă: rămâne 5
        self.assertEqual(len(self.b.waitlist), 5)

    # =========================================================================
    # Ucide M3: `sessions >= 10` → `sessions > 10`
    # =========================================================================

    def test_kill_M3_exactly_10_sessions_must_apply_volume_discount(self) -> None:
        """
        Ucide M3: `sessions >= 10` → `sessions > 10`.

        Implementarea CORECTĂ: sessions=10 satisface  10 >= 10  = True
            → se aplică reducerea de 10% → cost = 10 × 10.0 × 0.90 = 90.0. ✓

        Mutantul M3: sessions=10 satisface  10 > 10  = False
            → NU se aplică reducerea → cost = 10 × 10.0 = 100.0 (BUG!).

        Bug real reprezentat: clienții cu exact 10 ședințe nu primesc
        reducerea de volum la care au dreptul → pierdere financiară pentru client.

        Testul eșuează pe M3 deoarece assertAlmostEqual(100.0, 90.0) → FAIL.
        """
        cost = self.b.calculate_cost(10, False)

        self.assertAlmostEqual(
            cost,
            90.0,
            msg="La sessions=10, reducerea de volum 10% trebuie aplicată: 10×10×0.90=90.0",
        )

    def test_kill_M3_sessions_nine_must_not_apply_volume_discount(self) -> None:
        """
        Test complementar M3: sessions=9 NU trebuie să primească reducerea de volum.

        Verifică că frontiera este corectă: la sessions=9 nu se aplică reducerea,
        deci costul este 9 × 10.0 = 90.0 (fără × 0.90).
        Atât implementarea corectă cât și M3 returnează același rezultat la sessions=9
        → acest test NU omoară M3 singur, dar validează comportamentul sub frontieră.
        """
        cost = self.b.calculate_cost(9, False)
        self.assertAlmostEqual(cost, 90.0)  # 9 × 10 = 90.0, fără reducere

    # =========================================================================
    # Ucide M4: `cost *= 0.80` → `cost *= 0.90`
    # =========================================================================

    def test_kill_M4_membership_discount_must_be_20_percent(self) -> None:
        """
        Ucide M4: `cost *= 0.80` → `cost *= 0.90`.

        Implementarea CORECTĂ: has_membership=True → cost × 0.80 (reducere 20%).
            calculate_cost(1, True) = 1 × 10.0 × 0.80 = 8.0. ✓

        Mutantul M4: cost × 0.90 (reducere 10% în loc de 20%).
            calculate_cost(1, True) = 1 × 10.0 × 0.90 = 9.0 (BUG!).

        Bug real reprezentat: clienții cu abonament primesc o reducere de
        10% în loc de 20% → pierdere financiară pentru toți abonații.

        Testul eșuează pe M4 deoarece assertAlmostEqual(9.0, 8.0) → FAIL.
        """
        cost = self.b.calculate_cost(1, True)

        self.assertAlmostEqual(
            cost,
            8.0,
            msg="Reducerea de membership trebuie să fie 20%: 1×10×0.80=8.0",
        )

    def test_kill_M4_membership_discount_distinguishes_10_vs_20_percent(self) -> None:
        """
        Test auxiliar M4: verifică explicit că 8.0 ≠ 9.0 (20% ≠ 10%).

        Folosind sessions=5 pentru a evita interferența cu discountul de volum.
            Corect:  5 × 10 × 0.80 = 40.0
            Mutant:  5 × 10 × 0.90 = 45.0
        """
        cost = self.b.calculate_cost(5, True)
        self.assertAlmostEqual(cost, 40.0)
        self.assertNotAlmostEqual(cost, 45.0,
            msg="Reducerea trebuie să fie 20% (×0.80=40.0), nu 10% (×0.90=45.0)")

    # =========================================================================
    # Documentare mutanți echivalenți (M5, M6)
    # =========================================================================

    def test_document_M5_equivalent_augmented_subtract_cancel(self) -> None:
        """
        Documentare M5 (echivalent):
            Original: self.booked_spots -= 1
            Mutant:   self.booked_spots = self.booked_spots - 1

        Justificare echivalență:
            `int` în Python este imutabil. `-=` pe un atribut int se traduce în
            `attr = attr - 1` (Python nu definește __isub__ separat pentru int).
            Orice test care verifică valoarea booked_spots după cancel va obține
            același rezultat pe ambele variante → M5 nu poate fi omorât.

        Demonstrație: booked_spots scade cu 1 după anulare în ambele cazuri.
        """
        self.b.book_spot("Alice")
        self.assertEqual(self.b.booked_spots, 1)
        self.b.cancel_booking("Alice")
        self.assertEqual(self.b.booked_spots, 0)

    def test_document_M6_equivalent_augmented_multiply_cost(self) -> None:
        """
        Documentare M6 (echivalent):
            Original: cost *= 0.90
            Mutant:   cost = cost * 0.90

        Justificare echivalență:
            `float` în Python este imutabil. `*=` și `= ... *` produc
            exact același rezultat numeric și același obiect din perspectiva
            valorii. Niciun test nu poate distinge aceste două forme prin
            comportamentul observabil al metodei calculate_cost.

        Demonstrație: reducerea de volum produce același cost în ambele cazuri.
        """
        cost = self.b.calculate_cost(10, False)
        self.assertAlmostEqual(cost, 90.0)  # 10 × 10 × 0.90 = 90.0


if __name__ == "__main__":
    unittest.main(verbosity=2)
