"""
Strategia 7 – Mutation Testing: teste suplimentare pentru uciderea mutantilor.

Acest modul contine teste scrise DUPA analiza raportului mutmut,
cu scopul de a omori mutantii neechivalenti care au supravietuit
suitei initiale din test_bank_account.py.

Motivul supravietuirii:
  - Suita initiala foloseste valori de test care produc numere rotunde
    (balance=1000.0 cu rate intregi → interesul este deja un numar rotund),
    deci mutatii la precizia round() nu schimba rezultatul.
  - Suita initiala testeaza creditul premium cu sume mult sub plafon
    (50_000 < 64_800 = 6480×10), deci mutatii mici la multiplier nu sunt
    observabile.

Mutanti neechivalenti documentati:
  Mutant #1 – apply_interest(): round(x, 2) → rotunjire modificata
  Mutant #2 – LOAN_MULTIPLIER["premium"]: 10 → 11 (sau alta valoare)

Vezi docs/tables/mutation_analysis.md pentru analiza completa.
"""
import pytest
from src.bank_account import BankAccount


# =============================================================================
# MUTANT #1 – apply_interest(): precizia round()
# =============================================================================
#
# Descrierea mutatiei:
#   Original : interest = round(self.balance * rate, 2)
#   Mutant   : interest = round(self.balance * rate, 1)   ← sau fara round()
#
# Efectul mutatiei:
#   Cu balance=1000.0 si orice rata intreaga (1%, 5%, 8%), rezultatul este
#   un numar cu cel mult 1 zecimala (10.0, 50.0, 80.0) si round() nu face
#   nicio diferenta → mutantul SUPRAVIETUIESTE.
#   Cu balance non-rotund (ex: 1000.33) si rata 5%:
#     1000.33 * 0.05 = 50.0165
#     round(50.0165, 2) = 50.02   ← original
#     round(50.0165, 1) = 50.0    ← mutant cu precizie 1
#   Acum exista o diferenta observabila → testul OMOARA mutantul.
#
# De ce a supravietuit initial:
#   Toate testele din suita principala folosesc balance=1000.0, ceea ce
#   produce valori rotunde (10.0, 50.0, 80.0) indiferent de precizia round().
#
# Test care omoara mutantul:
#   Folosim balance=1000.33 cu savings (rate=0.05):
#     1000.33 * 0.05 = 50.0165
#     round(50.0165, 2) = 50.02  ← original returneaza 50.02
#     round(50.0165, 1) = 50.0   ← mutant returneaza 50.0
#   assert interest == 50.02 → TRECE pe original, ESUEAZA pe mutant → OMORAT
# =============================================================================


class TestMutationKillingApplyInterestRounding:
    """Teste pentru uciderea Mutantului #1 (precizia round in apply_interest)."""

    def test_mutation1_interest_rounds_to_2_decimal_places(self):
        """
        Ucide Mutant #1: interest = round(x*rate, 2) vs round(x*rate, 1).

        balance=1000.33, savings rate=0.05
          1000.33 * 0.05 = 50.0165
          round(50.0165, 2) = 50.02   ← corect (original)
          round(50.0165, 1) = 50.0    ← incorect (mutant cu precizie 1)

        Testul TRECE pe original si ESUEAZA pe mutant → mutant OMORAT.
        """
        acc = BankAccount("Test Mutant1", 1_000.33, "savings")
        interest = acc.apply_interest()
        assert interest == pytest.approx(50.02, abs=1e-9)

    def test_mutation1_balance_updated_correctly_after_interest(self):
        """
        Confirma ca soldul este actualizat cu dobanda rotunjita corect.

        balance + interest = 1000.33 + 50.02 = 1050.35
        Cu mutant (precizie 1): 1000.33 + 50.0 = 1050.33 (diferit)
        """
        acc = BankAccount("Test Mutant1", 1_000.33, "savings")
        acc.apply_interest()
        assert acc.balance == pytest.approx(1_050.35, abs=1e-9)

    def test_mutation1_checking_account_rounding(self):
        """
        Verifica precizia si pentru checking cu balance non-rotund.

        balance=333.34, checking rate=0.01
          333.34 * 0.01 = 3.3334
          round(3.3334, 2) = 3.33   ← original
          round(3.3334, 1) = 3.3    ← mutant cu precizie 1
        """
        acc = BankAccount("Test Mutant1", 333.34, "checking")
        interest = acc.apply_interest()
        assert interest == pytest.approx(3.33, abs=1e-9)

    def test_mutation1_interest_not_applied_when_zero_balance(self):
        """
        Confirma ca dobanda nu se aplica la sold zero (nu este afectat de mutant).
        """
        acc = BankAccount("Test Mutant1", 0.0, "savings")
        assert acc.apply_interest() == 0.0


# =============================================================================
# MUTANT #2 – LOAN_MULTIPLIER["premium"]: 10 → 11
# =============================================================================
#
# Descrierea mutatiei:
#   Original : LOAN_MULTIPLIER["premium"] = 10
#   Mutant   : LOAN_MULTIPLIER["premium"] = 11  (sau alta valoare != 10)
#
# Efectul mutatiei:
#   Cu mutant 11: max_loan = balance * 11 in loc de balance * 10.
#   Sume intre 10× si 11× balance vor fi acceptate incorect.
#   Sume la exact 10× balance: acceptate de original, acceptate si de mutant
#   (11×>10×) → NU este un test killer.
#
# De ce a supravietuit initial:
#   Testul de integrare `test_integration_premium_full_scenario` foloseste:
#     balance=6480, premium×10=64800, testeaza loan=50_000 < 64_800 → True
#   Cu mutant 11: 6480×11=71280, 50000<=71280 → True (acelasi rezultat).
#   Niciun test nu testa la exact 10× pentru premium.
#
# Test care omoara mutantul:
#   balance=1000, premium×10=10_000
#   is_eligible_for_loan(10_000.0) trebuie True (exact la plafon).
#   - Original (×10): max=10_000, 10_000<=10_000 → True (test TRECE)
#   - Mutant   (×11): max=11_000, 10_000<=11_000 → True (test TRECE – NU omoara)
#
#   Deci pentru mutant ×11, testul cu 10_000 NU omoara.
#   In schimb, testul cu valoare INTRE 10× si 11× omoara:
#     is_eligible_for_loan(10_500.0) → original: False, mutant×11: True → OMORAT
# =============================================================================


class TestMutationKillingPremiumLoanMultiplier:
    """
    Teste pentru uciderea Mutantului #2 (LOAN_MULTIPLIER["premium"]).

    Strategie de testare:
      - Testam suma INTRE 10× si 11× balance
      - Original (×10): suma > max_loan → False
      - Mutant   (×11): suma < max_loan → True
      - Test expect=False → TRECE pe original, ESUEAZA pe mutant → OMORAT
    """

    def test_mutation2_premium_amount_between_10x_and_11x_is_rejected(self):
        """
        Ucide Mutant #2: suma intre 10× si 11× balance trebuie respinsa.

        balance=1000, premium:
          Original (×10): max=10_000, 10_500 > 10_000 → False (test TRECE)
          Mutant   (×11): max=11_000, 10_500 <= 11_000 → True  (test ESUEAZA → OMORAT)
        """
        acc = BankAccount("Test Mutant2", 1_000.0, "premium", transactions_count=5)
        assert acc.is_eligible_for_loan(10_500.0) is False

    def test_mutation2_premium_amount_at_exact_10x_is_accepted(self):
        """
        Confirma ca suma la exact 10× balance este acceptata (ambele versiuni).
        Rolul: valideaza plafonul corect, nu este un killer direct.
        """
        acc = BankAccount("Test Mutant2", 1_000.0, "premium", transactions_count=5)
        assert acc.is_eligible_for_loan(10_000.0) is True

    def test_mutation2_premium_amount_just_above_10x_is_rejected(self):
        """
        Confirma ca suma de 10_000.01 (peste 10× exact) este respinsa.

        Original (×10): 10_000.01 > 10_000 → False (test TRECE)
        Mutant   (×11): 10_000.01 <= 11_000 → True (test ESUEAZA → OMORAT)
        """
        acc = BankAccount("Test Mutant2", 1_000.0, "premium", transactions_count=5)
        assert acc.is_eligible_for_loan(10_000.01) is False

    def test_mutation2_savings_multiplier_not_affected(self):
        """
        Confirma ca multiplicatorul pentru savings (5) nu este afectat.
        balance=1000, savings×5=5000: sume sub 5000 acceptate.
        """
        acc = BankAccount("Test Mutant2", 1_000.0, "savings", transactions_count=5)
        assert acc.is_eligible_for_loan(5_000.0) is True
        assert acc.is_eligible_for_loan(5_000.01) is False
