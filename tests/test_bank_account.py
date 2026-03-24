"""
Teste unitare pentru clasa BankAccount.

Strategii de testare ilustrate:
  1. Partitionare in clase de echivalenta
  2. Analiza valorilor de frontiera
  3. Acoperire la nivel de instructiune (statement coverage)
  4. Acoperire la nivel de decizie (decision coverage)
  5. Acoperire la nivel de conditie (condition coverage)
  6. Circuite independente / acoperire la nivel de cai (basis path testing)

Strategia 7 (mutation killing) se afla in:
  tests/test_bank_account_additional_mutation.py

Conventii de naming:
  test_<metoda>_<strategie>_<descriere>
  ex: test_deposit_bv_exactly_max, test_withdraw_basis_path_p3_daily_limit
"""
import pytest
from src.bank_account import BankAccount


# =============================================================================
# STRATEGIA 1 – PARTITIONARE IN CLASE DE ECHIVALENTA
# =============================================================================


class TestDepositEquivalenceClasses:
    """
    Partitionare in clase de echivalenta pentru deposit(amount).

    Clase identificate:
      CE-D1 (valida)  : 0 < amount < MAX_DEPOSIT        → depunere reusita
      CE-D2 (invalida): amount <= 0                      → ValueError
      CE-D3 (invalida): amount >= MAX_DEPOSIT            → ValueError
      CE-D4 (invalida): amount non-numeric               → TypeError
    """

    def setup_method(self) -> None:
        self.account = BankAccount("Ion Popescu", 1_000.0)

    def test_deposit_ce_d1_valid_amount(self):
        """CE-D1: suma pozitiva in intervalul permis → sold actualizat."""
        result = self.account.deposit(500.0)
        assert result == 1_500.0

    def test_deposit_ce_d1_increments_transaction_count(self):
        """CE-D1: depunerea valida incrementeaza transactions_count."""
        before = self.account.get_transaction_count()
        self.account.deposit(100.0)
        assert self.account.get_transaction_count() == before + 1

    def test_deposit_ce_d2_zero_amount(self):
        """CE-D2: suma zero → ValueError."""
        with pytest.raises(ValueError, match="pozitiva"):
            self.account.deposit(0.0)

    def test_deposit_ce_d2_negative_amount(self):
        """CE-D2: suma negativa → ValueError."""
        with pytest.raises(ValueError, match="pozitiva"):
            self.account.deposit(-100.0)

    def test_deposit_ce_d3_exceeds_maximum(self):
        """CE-D3: suma depaseste MAX_DEPOSIT → ValueError."""
        with pytest.raises(ValueError, match="limita maxima"):
            self.account.deposit(2_000_000.0)

    def test_deposit_ce_d4_non_numeric_string(self):
        """CE-D4: amount este string → TypeError."""
        with pytest.raises(TypeError, match="numerica"):
            self.account.deposit("500")

    def test_deposit_ce_d4_non_numeric_none(self):
        """CE-D4: amount este None → TypeError."""
        with pytest.raises(TypeError, match="numerica"):
            self.account.deposit(None)


class TestWithdrawEquivalenceClasses:
    """
    Partitionare in clase de echivalenta pentru withdraw(amount).

    Clase identificate:
      CE-W1 (valida)  : 0 < amount, fonduri ok, sub limita zilnica   → succes
      CE-W2 (invalida): amount <= 0                                   → ValueError
      CE-W3 (invalida): balance - amount < overdraft_limit            → ValueError
      CE-W4 (invalida): daily_withdrawn + amount > MAX_DAILY_WITHDRAWAL → ValueError
      CE-W5 (invalida): amount non-numeric                            → TypeError
    """

    def setup_method(self) -> None:
        self.account = BankAccount("Ion Popescu", 2_000.0)

    def test_withdraw_ce_w1_valid(self):
        """CE-W1: retragere valida → sold actualizat."""
        result = self.account.withdraw(500.0)
        assert result == 1_500.0

    def test_withdraw_ce_w1_increments_transaction_count(self):
        """CE-W1: retragerea valida incrementeaza transactions_count."""
        before = self.account.get_transaction_count()
        self.account.withdraw(100.0)
        assert self.account.get_transaction_count() == before + 1

    def test_withdraw_ce_w2_zero(self):
        """CE-W2: suma zero → ValueError."""
        with pytest.raises(ValueError, match="pozitiva"):
            self.account.withdraw(0.0)

    def test_withdraw_ce_w2_negative(self):
        """CE-W2: suma negativa → ValueError."""
        with pytest.raises(ValueError, match="pozitiva"):
            self.account.withdraw(-50.0)

    def test_withdraw_ce_w3_insufficient_funds_savings(self):
        """CE-W3: savings nu permite descoperit → ValueError."""
        acc = BankAccount("Test", 100.0, "savings")
        with pytest.raises(ValueError, match="Fonduri insuficiente"):
            acc.withdraw(200.0)

    def test_withdraw_ce_w4_daily_limit_exceeded(self):
        """CE-W4: suma depaseste limita zilnica → ValueError."""
        with pytest.raises(ValueError, match="Limita zilnica"):
            self.account.withdraw(5_001.0)

    def test_withdraw_ce_w5_non_numeric(self):
        """CE-W5: amount non-numeric → TypeError."""
        with pytest.raises(TypeError, match="numerica"):
            self.account.withdraw("100")


class TestInitEquivalenceClasses:
    """
    Partitionare in clase de echivalenta pentru constructorul BankAccount.

    TypeError pentru tipuri invalide, ValueError pentru valori invalide.
    """

    def test_init_ce_valid_default_params(self):
        """Constructor cu parametrii impliciti → instanta creata corect."""
        acc = BankAccount("Ana Ionescu")
        assert acc.owner == "Ana Ionescu"
        assert acc.balance == 0.0
        assert acc.account_type == "checking"
        assert acc.transactions_count == 0
        assert acc.daily_withdrawn == 0.0

    def test_init_ce_valid_all_params(self):
        """Constructor cu toti parametrii expliciti valizi."""
        acc = BankAccount("Test", 500.0, "savings", 3, 100.0)
        assert acc.balance == 500.0
        assert acc.account_type == "savings"
        assert acc.transactions_count == 3
        assert acc.daily_withdrawn == 100.0

    def test_init_ce_invalid_owner_empty(self):
        """owner gol → ValueError (valoare invalida)."""
        with pytest.raises(ValueError, match="non-gol"):
            BankAccount("")

    def test_init_ce_invalid_owner_whitespace(self):
        """owner numai spatii → ValueError."""
        with pytest.raises(ValueError, match="non-gol"):
            BankAccount("   ")

    def test_init_ce_invalid_owner_non_string(self):
        """owner non-string → TypeError (tip invalid)."""
        with pytest.raises(TypeError):
            BankAccount(123)

    def test_init_ce_invalid_balance_negative(self):
        """balance negativ → ValueError (valoare invalida)."""
        with pytest.raises(ValueError, match="non-negativ"):
            BankAccount("Test", -100.0)

    def test_init_ce_invalid_balance_non_numeric(self):
        """balance non-numeric → TypeError (tip invalid)."""
        with pytest.raises(TypeError):
            BankAccount("Test", "abc")

    def test_init_ce_invalid_account_type(self):
        """account_type necunoscut → ValueError."""
        with pytest.raises(ValueError, match="invalid"):
            BankAccount("Test", 0.0, "platinum")

    def test_init_ce_valid_account_types(self):
        """Toate tipurile valide sunt acceptate."""
        for atype in ("checking", "savings", "premium"):
            acc = BankAccount("Test", 0.0, atype)
            assert acc.account_type == atype

    def test_init_ce_invalid_transactions_count_negative(self):
        """transactions_count negativ → ValueError."""
        with pytest.raises(ValueError, match="non-negativ"):
            BankAccount("Test", 0.0, "checking", transactions_count=-1)

    def test_init_ce_invalid_transactions_count_non_int(self):
        """transactions_count non-int → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", 0.0, "checking", transactions_count=1.5)

    def test_init_ce_invalid_daily_withdrawn_negative(self):
        """daily_withdrawn negativ → ValueError."""
        with pytest.raises(ValueError, match="non-negativ"):
            BankAccount("Test", 0.0, "checking", daily_withdrawn=-1.0)

    def test_init_ce_invalid_daily_withdrawn_non_numeric(self):
        """daily_withdrawn non-numeric → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", 0.0, "checking", daily_withdrawn="abc")

    def test_init_ce_owner_stripped(self):
        """owner cu spatii laterale este strip-uit la stocare."""
        acc = BankAccount("  Ana  ")
        assert acc.owner == "Ana"

    def test_init_ce_daily_withdrawn_is_public(self):
        """daily_withdrawn este atribut public (nu _daily_withdrawn)."""
        acc = BankAccount("Test", 0.0, "checking", daily_withdrawn=100.0)
        assert acc.daily_withdrawn == 100.0
        assert not hasattr(acc, "_daily_withdrawn")


class TestApplyInterestEquivalenceClasses:
    """
    Partitionare in clase de echivalenta pentru apply_interest().

    Clase:
      CE-I1 (valida): balance > 0  → dobanda aplicata si returnata
      CE-I2         : balance <= 0 → dobanda 0.0, soldul neschimbat
    """

    def test_apply_interest_ce_i1_positive_balance_checking(self):
        """CE-I1: checking cu sold pozitiv → 1% dobanda."""
        acc = BankAccount("Test", 1_000.0, "checking")
        interest = acc.apply_interest()
        assert interest == 10.0
        assert acc.balance == 1_010.0

    def test_apply_interest_ce_i1_savings(self):
        """CE-I1: savings cu sold pozitiv → 5% dobanda."""
        acc = BankAccount("Test", 1_000.0, "savings")
        interest = acc.apply_interest()
        assert interest == 50.0
        assert acc.balance == 1_050.0

    def test_apply_interest_ce_i1_premium(self):
        """CE-I1: premium cu sold pozitiv → 8% dobanda."""
        acc = BankAccount("Test", 1_000.0, "premium")
        interest = acc.apply_interest()
        assert interest == 80.0
        assert acc.balance == 1_080.0

    def test_apply_interest_ce_i2_zero_balance(self):
        """CE-I2: sold zero → dobanda 0.0."""
        acc = BankAccount("Test", 0.0)
        assert acc.apply_interest() == 0.0
        assert acc.balance == 0.0


class TestLoanEquivalenceClasses:
    """
    Partitionare in clase de echivalenta pentru is_eligible_for_loan().

    Clase:
      CE-L1: toate conditiile indeplinite    → True
      CE-L2: balance <= 0                    → False
      CE-L3: transactions_count < 5          → False
      CE-L4: loan_amount > balance * factor  → False
      CE-L5: loan_amount non-numeric         → TypeError
      CE-L6: loan_amount <= 0                → ValueError
    """

    def test_loan_ce_l1_eligible(self, account_with_transactions):
        """CE-L1: toate conditiile indeplinite → True."""
        assert account_with_transactions.is_eligible_for_loan(500.0) is True

    def test_loan_ce_l2_zero_balance(self):
        """CE-L2: sold zero → False."""
        acc = BankAccount("Test", 0.0, "checking", transactions_count=10)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_loan_ce_l2_negative_balance_after_overdraft(self):
        """CE-L2: sold negativ (dupa descoperit) → False."""
        acc = BankAccount("Test", 100.0, "checking", transactions_count=10)
        acc.withdraw(400.0)  # balance = -300
        assert acc.is_eligible_for_loan(100.0) is False

    def test_loan_ce_l3_insufficient_transactions(self):
        """CE-L3: prea putine tranzactii → False."""
        acc = BankAccount("Test", 1_000.0, "checking", transactions_count=2)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_loan_ce_l4_amount_too_large(self, account_with_transactions):
        """CE-L4: suma ceruta depaseste factor * balance → False (checking×2=2000)."""
        assert account_with_transactions.is_eligible_for_loan(2_001.0) is False

    def test_loan_ce_l5_non_numeric(self, account_with_transactions):
        """CE-L5: loan_amount non-numeric → TypeError."""
        with pytest.raises(TypeError, match="numerica"):
            account_with_transactions.is_eligible_for_loan("500")

    def test_loan_ce_l6_non_positive(self, account_with_transactions):
        """CE-L6: loan_amount <= 0 → ValueError."""
        with pytest.raises(ValueError, match="pozitiva"):
            account_with_transactions.is_eligible_for_loan(0.0)


class TestTransferEquivalenceClasses:
    """
    Partitionare in clase de echivalenta pentru transfer().

    transfer() returneaza un dict cu statusul operatiei.
    """

    def test_transfer_ce_t1_valid_returns_dict(self, checking_account, savings_account):
        """CE-T1: transfer valid → dict cu status success."""
        result = checking_account.transfer(savings_account, 200.0)
        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert result["amount"] == 200.0
        assert result["from_owner"] == checking_account.owner
        assert result["to_owner"] == savings_account.owner

    def test_transfer_ce_t1_balances_updated(self, checking_account, savings_account):
        """CE-T1: soldurile sunt actualizate corect dupa transfer."""
        checking_account.transfer(savings_account, 200.0)
        assert checking_account.balance == 800.0
        assert savings_account.balance == 1_200.0

    def test_transfer_ce_t2_invalid_target_type(self, checking_account):
        """CE-T2: target nu este BankAccount → TypeError."""
        with pytest.raises(TypeError, match="BankAccount"):
            checking_account.transfer("not_an_account", 100.0)

    def test_transfer_ce_t3_self_transfer(self, checking_account):
        """CE-T3: transfer catre sine insusi → ValueError."""
        with pytest.raises(ValueError, match="acelasi cont"):
            checking_account.transfer(checking_account, 100.0)

    def test_transfer_ce_t4_insufficient_funds(self, savings_account):
        """CE-T4: fonduri insuficiente (savings fara overdraft) → ValueError."""
        target = BankAccount("Destinatar", 0.0)
        with pytest.raises(ValueError, match="Fonduri insuficiente"):
            savings_account.transfer(target, 2_000.0)

    def test_transfer_ce_t4_target_balance_unchanged_on_failure(self, savings_account):
        """CE-T4: daca withdraw esueaza, deposit pe target nu se executa."""
        target = BankAccount("Destinatar", 500.0)
        with pytest.raises(ValueError):
            savings_account.transfer(target, 2_000.0)
        assert target.balance == 500.0


# =============================================================================
# STRATEGIA 2 – ANALIZA VALORILOR DE FRONTIERA
# =============================================================================


class TestDepositBoundaryValues:
    """
    Analiza valorilor de frontiera pentru deposit(amount).
    Interval valid: 0 < amount < MAX_DEPOSIT (ambele capete excluse).
    """

    def setup_method(self) -> None:
        self.account = BankAccount("Test", 0.0)

    def test_deposit_bv_just_below_zero(self):
        """VF: -0.01 → ValueError."""
        with pytest.raises(ValueError):
            self.account.deposit(-0.01)

    def test_deposit_bv_exactly_zero(self):
        """VF: 0.0 → ValueError (frontiera inferioara)."""
        with pytest.raises(ValueError):
            self.account.deposit(0.0)

    def test_deposit_bv_just_above_zero(self):
        """VF: 0.01 → succes (primul valid)."""
        assert self.account.deposit(0.01) == pytest.approx(0.01)

    def test_deposit_bv_just_below_max(self):
        """VF: 999_999.99 → succes (ultimul valid)."""
        assert self.account.deposit(999_999.99) == pytest.approx(999_999.99)

    def test_deposit_bv_exactly_max(self):
        """VF: 1_000_000.0 → ValueError (conditia >= exclude frontiera)."""
        with pytest.raises(ValueError, match="limita maxima"):
            self.account.deposit(1_000_000.0)

    def test_deposit_bv_just_above_max(self):
        """VF: 1_000_000.01 → ValueError."""
        with pytest.raises(ValueError, match="limita maxima"):
            self.account.deposit(1_000_000.01)


class TestWithdrawBoundaryValues:
    """
    Analiza valorilor de frontiera pentru withdraw(amount).
    """

    # ---- Limita zilnica (MAX_DAILY_WITHDRAWAL = 5_000, inclusiv) ----

    def test_withdraw_bv_daily_just_below_limit(self):
        """VF daily: 4_999.99 → succes."""
        acc = BankAccount("Test", 10_000.0)
        acc.withdraw(4_999.99)
        assert acc.daily_withdrawn == pytest.approx(4_999.99)

    def test_withdraw_bv_daily_exactly_at_limit(self):
        """VF daily: exact 5_000.0 → succes (limita inclusiva)."""
        acc = BankAccount("Test", 10_000.0)
        acc.withdraw(5_000.0)
        assert acc.daily_withdrawn == 5_000.0

    def test_withdraw_bv_daily_just_above_limit(self):
        """VF daily: 5_000.01 → ValueError."""
        acc = BankAccount("Test", 10_000.0)
        with pytest.raises(ValueError, match="Limita zilnica"):
            acc.withdraw(5_000.01)

    # ---- Overdraft checking (limita -500) ----

    def test_withdraw_bv_overdraft_checking_just_above_limit(self):
        """VF checking: balance-amount = -499.99 → succes."""
        acc = BankAccount("Test", 0.01, "checking")
        acc.withdraw(500.0)
        assert acc.balance == pytest.approx(-499.99)

    def test_withdraw_bv_overdraft_checking_exactly_at_limit(self):
        """VF checking: balance-amount = -500.0 (exact) → succes."""
        acc = BankAccount("Test", 0.0, "checking")
        acc.withdraw(500.0)
        assert acc.balance == -500.0

    def test_withdraw_bv_overdraft_checking_below_limit(self):
        """VF checking: balance-amount = -500.01 → ValueError."""
        acc = BankAccount("Test", 0.0, "checking")
        with pytest.raises(ValueError, match="Fonduri insuficiente"):
            acc.withdraw(500.01)

    # ---- Overdraft savings (limita 0) ----

    def test_withdraw_bv_overdraft_savings_exactly_zero(self):
        """VF savings: balance-amount = 0.0 (exact) → succes."""
        acc = BankAccount("Test", 100.0, "savings")
        acc.withdraw(100.0)
        assert acc.balance == 0.0

    def test_withdraw_bv_overdraft_savings_below_zero(self):
        """VF savings: balance-amount = -0.01 → ValueError."""
        acc = BankAccount("Test", 100.0, "savings")
        with pytest.raises(ValueError, match="Fonduri insuficiente"):
            acc.withdraw(100.01)

    # ---- Overdraft premium (limita -2_000) ----

    def test_withdraw_bv_overdraft_premium_exactly_at_limit(self):
        """VF premium: balance-amount = -2_000.0 (exact) → succes."""
        acc = BankAccount("Test", 0.0, "premium")
        acc.withdraw(2_000.0)
        assert acc.balance == -2_000.0

    def test_withdraw_bv_overdraft_premium_below_limit(self):
        """VF premium: balance-amount = -2_000.01 → ValueError."""
        acc = BankAccount("Test", 0.0, "premium")
        with pytest.raises(ValueError, match="Fonduri insuficiente"):
            acc.withdraw(2_000.01)


class TestLoanBoundaryValues:
    """
    Analiza valorilor de frontiera pentru is_eligible_for_loan().
    """

    # ---- transactions_count (prag = 5, inclusiv) ----

    def test_loan_bv_transactions_just_below_min(self):
        """VF tx: 4 tranzactii → False."""
        acc = BankAccount("Test", 1_000.0, "checking", transactions_count=4)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_loan_bv_transactions_exactly_at_min(self):
        """VF tx: exact 5 tranzactii → True."""
        acc = BankAccount("Test", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(100.0) is True

    def test_loan_bv_transactions_just_above_min(self):
        """VF tx: 6 tranzactii → True."""
        acc = BankAccount("Test", 1_000.0, "checking", transactions_count=6)
        assert acc.is_eligible_for_loan(100.0) is True

    # ---- loan_amount vs plafon (checking: 1000*2=2000) ----

    def test_loan_bv_amount_just_below_max(self):
        """VF plafon: 1_999.99 < 2_000 → True."""
        acc = BankAccount("Test", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(1_999.99) is True

    def test_loan_bv_amount_exactly_at_max(self):
        """VF plafon: exact 2_000 (checking: 1000×2) → True."""
        acc = BankAccount("Test", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(2_000.0) is True

    def test_loan_bv_amount_just_above_max(self):
        """VF plafon: 2_000.01 > 2_000 → False."""
        acc = BankAccount("Test", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(2_000.01) is False

    # ---- balance la frontiera 0 ----

    def test_loan_bv_balance_exactly_zero(self):
        """VF balance: exact 0 → False."""
        acc = BankAccount("Test", 0.0, transactions_count=5)
        assert acc.is_eligible_for_loan(100.0) is False


# =============================================================================
# STRATEGIA 3 – STATEMENT COVERAGE
# =============================================================================


class TestStatementCoverage:
    """
    Teste care asigura ca fiecare instructiune din bank_account.py
    este executata cel putin o data.

    Masurata cu: pytest --cov=src --cov-report=term-missing
    Tinta: 100% statements pe src/bank_account.py
    """

    def test_stmt_constructor_full_path(self):
        """Acopera toate instructiunile din __init__ (cale de succes)."""
        acc = BankAccount("Test", 100.0, "savings", 3, 50.0)
        assert acc.balance == 100.0
        assert acc.daily_withdrawn == 50.0

    def test_stmt_deposit_success_path(self):
        """Acopera instructiunile din deposit (cale de succes)."""
        acc = BankAccount("Test", 0.0)
        result = acc.deposit(100.0)
        assert result == 100.0
        assert acc.transactions_count == 1

    def test_stmt_withdraw_success_path(self):
        """Acopera instructiunile din withdraw (cale de succes)."""
        acc = BankAccount("Test", 1_000.0)
        result = acc.withdraw(200.0)
        assert result == 800.0
        assert acc.transactions_count == 1
        assert acc.daily_withdrawn == 200.0

    def test_stmt_transfer_success_path(self):
        """Acopera instructiunile din transfer (cale de succes)."""
        src = BankAccount("Sursa", 500.0)
        dst = BankAccount("Dest", 0.0)
        result = src.transfer(dst, 200.0)
        assert result["status"] == "success"

    def test_stmt_apply_interest_positive_balance(self):
        """Acopera ramura interest aplicat."""
        acc = BankAccount("Test", 1_000.0, "premium")
        interest = acc.apply_interest()
        assert interest > 0

    def test_stmt_apply_interest_zero_balance(self):
        """Acopera ramura return 0.0 din apply_interest."""
        acc = BankAccount("Test", 0.0)
        assert acc.apply_interest() == 0.0

    def test_stmt_loan_eligible(self):
        """Acopera instructiunile din is_eligible_for_loan (return True)."""
        acc = BankAccount("Test", 1_000.0, "premium", transactions_count=5)
        assert acc.is_eligible_for_loan(500.0) is True

    def test_stmt_loan_compound_condition_true(self):
        """Acopera return False din D3 (conditia compusa)."""
        acc = BankAccount("Test", 0.0, transactions_count=10)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_stmt_loan_amount_too_large(self):
        """Acopera return False din D4 (loan > max_loan)."""
        acc = BankAccount("Test", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(999_000.0) is False

    def test_stmt_get_balance(self):
        """Acopera get_balance()."""
        acc = BankAccount("Test", 250.0)
        assert acc.get_balance() == 250.0

    def test_stmt_get_transaction_count(self):
        """Acopera get_transaction_count()."""
        acc = BankAccount("Test", 0.0, transactions_count=7)
        assert acc.get_transaction_count() == 7

    def test_stmt_reset_daily_limit(self):
        """Acopera reset_daily_limit()."""
        acc = BankAccount("Test", 5_000.0)
        acc.withdraw(1_000.0)
        acc.reset_daily_limit()
        assert acc.daily_withdrawn == 0.0

    def test_stmt_str_repr(self):
        """Acopera __str__ si __repr__."""
        acc = BankAccount("Test", 100.0, "savings")
        assert "Test" in str(acc)
        assert "Test" in repr(acc)


# =============================================================================
# STRATEGIA 4 – DECISION COVERAGE
# =============================================================================


class TestDecisionCoverage:
    """
    Teste care asigura ca fiecare decizie (if) este evaluata
    atat cu True cat si cu False.

    Nomenclatura: test_dc_<metoda>_<decizie>_<ramura>
    """

    # ---- deposit ----

    def test_dc_deposit_d1_type_check_true(self):
        """DC deposit D1 = True → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("T", 0.0).deposit("abc")

    def test_dc_deposit_d1_type_check_false(self):
        """DC deposit D1 = False → continua."""
        BankAccount("T", 0.0).deposit(100.0)

    def test_dc_deposit_d2_nonpositive_true(self):
        """DC deposit D2 (amount <= 0) = True → ValueError."""
        with pytest.raises(ValueError):
            BankAccount("T", 0.0).deposit(0.0)

    def test_dc_deposit_d2_nonpositive_false(self):
        """DC deposit D2 = False → continua."""
        BankAccount("T", 0.0).deposit(1.0)

    def test_dc_deposit_d3_exceeds_max_true(self):
        """DC deposit D3 (amount >= MAX) = True → ValueError."""
        with pytest.raises(ValueError):
            BankAccount("T", 0.0).deposit(1_000_000.0)

    def test_dc_deposit_d3_exceeds_max_false(self):
        """DC deposit D3 = False → succes."""
        BankAccount("T", 0.0).deposit(999_999.99)

    # ---- withdraw ----

    def test_dc_withdraw_d1_type_check_true(self):
        """DC withdraw D1 = True → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("T", 1_000.0).withdraw(None)

    def test_dc_withdraw_d1_type_check_false(self):
        """DC withdraw D1 = False → continua."""
        BankAccount("T", 1_000.0).withdraw(100.0)

    def test_dc_withdraw_d2_nonpositive_true(self):
        """DC withdraw D2 (amount <= 0) = True → ValueError."""
        with pytest.raises(ValueError):
            BankAccount("T", 1_000.0).withdraw(-1.0)

    def test_dc_withdraw_d2_nonpositive_false(self):
        """DC withdraw D2 = False → continua."""
        BankAccount("T", 1_000.0).withdraw(100.0)

    def test_dc_withdraw_d3_daily_limit_true(self):
        """DC withdraw D3 (daily limit exceeded) = True → ValueError."""
        with pytest.raises(ValueError, match="Limita zilnica"):
            BankAccount("T", 10_000.0).withdraw(5_001.0)

    def test_dc_withdraw_d3_daily_limit_false(self):
        """DC withdraw D3 = False → continua."""
        BankAccount("T", 10_000.0).withdraw(4_999.0)

    def test_dc_withdraw_d4_overdraft_true(self):
        """DC withdraw D4 (overdraft exceeded) = True → ValueError."""
        acc = BankAccount("T", 100.0, "savings")
        with pytest.raises(ValueError, match="Fonduri insuficiente"):
            acc.withdraw(200.0)

    def test_dc_withdraw_d4_overdraft_false(self):
        """DC withdraw D4 = False → succes."""
        acc = BankAccount("T", 1_000.0)
        acc.withdraw(500.0)
        assert acc.balance == 500.0

    # ---- apply_interest ----

    def test_dc_interest_balance_nonpositive_true(self):
        """DC apply_interest (balance <= 0) = True → return 0.0."""
        assert BankAccount("T", 0.0).apply_interest() == 0.0

    def test_dc_interest_balance_nonpositive_false(self):
        """DC apply_interest = False → dobanda calculata."""
        acc = BankAccount("T", 1_000.0, "savings")
        assert acc.apply_interest() == 50.0

    # ---- is_eligible_for_loan ----

    def test_dc_loan_d3_compound_true_via_balance(self):
        """DC loan D3 (compusa) = True prin balance <= 0 → False."""
        acc = BankAccount("T", 0.0, transactions_count=10)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_dc_loan_d3_compound_true_via_transactions(self):
        """DC loan D3 (compusa) = True prin transactions < MIN → False."""
        acc = BankAccount("T", 1_000.0, transactions_count=3)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_dc_loan_d4_amount_exceeds_max_true(self):
        """DC loan D4 (loan > max_loan) = True → False."""
        acc = BankAccount("T", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(5_000.0) is False

    def test_dc_loan_all_decisions_false(self):
        """DC loan toate deciziile False → True."""
        acc = BankAccount("T", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(500.0) is True


# =============================================================================
# STRATEGIA 5 – CONDITION COVERAGE
# =============================================================================


class TestConditionCoverage:
    """
    Teste pentru acoperire la nivel de conditie.

    Fiecare sub-conditie dintr-o expresie compusa este testata
    atat cu True cat si cu False, independent de celelalte.

    Conditii compuse in __init__ (parametri numerici):
      CC-BAL : isinstance(balance, bool) OR not isinstance(balance, (int,float))
      CC-TX  : isinstance(transactions_count, bool) OR not isinstance(transactions_count, int)
      CC-DW  : isinstance(daily_withdrawn, bool) OR not isinstance(daily_withdrawn, (int,float))

    Conditie compusa in is_eligible_for_loan (D3):
      CC-LOAN: self.balance <= 0 OR self.transactions_count < MIN_TRANSACTIONS_FOR_LOAN
    """

    # ---- CC-BAL: validare balance ----

    def test_cc_balance_is_bool(self):
        """CC-BAL sub-C1=True: balance=True → isinstance(True, bool)=True → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", True)

    def test_cc_balance_not_numeric_string(self):
        """CC-BAL sub-C1=False, sub-C2=True: balance="abc" → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", "abc")

    def test_cc_balance_both_false(self):
        """CC-BAL ambele False: balance=0.0 (numeric, not bool) → succes."""
        acc = BankAccount("Test", 0.0)
        assert acc.balance == 0.0

    # ---- CC-TX: validare transactions_count ----

    def test_cc_transactions_is_bool(self):
        """CC-TX sub-C1=True: transactions_count=True → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", 0.0, "checking", transactions_count=True)

    def test_cc_transactions_not_int(self):
        """CC-TX sub-C1=False, sub-C2=True: transactions_count=1.5 → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", 0.0, "checking", transactions_count=1.5)

    def test_cc_transactions_both_false(self):
        """CC-TX ambele False: transactions_count=0 (int, not bool) → succes."""
        acc = BankAccount("Test", 0.0, "checking", transactions_count=0)
        assert acc.transactions_count == 0

    # ---- CC-DW: validare daily_withdrawn ----

    def test_cc_daily_is_bool(self):
        """CC-DW sub-C1=True: daily_withdrawn=False → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", 0.0, "checking", daily_withdrawn=False)

    def test_cc_daily_not_numeric(self):
        """CC-DW sub-C1=False, sub-C2=True: daily_withdrawn='abc' → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", 0.0, "checking", daily_withdrawn="abc")

    def test_cc_daily_both_false(self):
        """CC-DW ambele False: daily_withdrawn=0.0 → succes."""
        acc = BankAccount("Test", 0.0, "checking", daily_withdrawn=0.0)
        assert acc.daily_withdrawn == 0.0

    # ---- CC-LOAN: conditia compusa D3 din is_eligible_for_loan ----

    def test_cc_loan_d3a_balance_zero(self):
        """CC-LOAN D3a=True (balance<=0, short-circuit): OR returneaza True imediat → False."""
        acc = BankAccount("T", 0.0, transactions_count=10)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_cc_loan_d3a_false_d3b_true(self):
        """CC-LOAN D3a=False (balance>0), D3b=True (tx<MIN): OR returneaza True → False."""
        acc = BankAccount("T", 1_000.0, transactions_count=3)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_cc_loan_both_false(self):
        """CC-LOAN ambele False (balance>0 si tx>=MIN): OR=False → continua spre D4."""
        acc = BankAccount("T", 1_000.0, transactions_count=5)
        assert acc.is_eligible_for_loan(500.0) is True

    # ---- owner validation – separate TypeError/ValueError ----

    def test_cc_owner_not_string_raises_typeerror(self):
        """owner non-string → TypeError (verificare separata de tip)."""
        with pytest.raises(TypeError):
            BankAccount(42)

    def test_cc_owner_is_string_but_empty_raises_valueerror(self):
        """owner gol (str, dar fara continut) → ValueError."""
        with pytest.raises(ValueError):
            BankAccount("")


# =============================================================================
# STRATEGIA 6 – CIRCUITE INDEPENDENTE / BASIS PATH TESTING
# =============================================================================
#
# Complexitate ciclomatica McCabe: V(G) = numar_decizii + 1
#
# withdraw         : 4 decizii simple (D1-D4)       → V(G) = 5
# is_eligible_for_loan: 2 simple + 1 compusa + 1 simple → V(G) = 5
#   (OR compus D3 numarat ca 1 decizie pentru McCabe)
# =============================================================================


class TestWithdrawBasisPaths:
    """
    Cele 5 circuite independente ale metodei withdraw().

    CFG:
      [START]
        D1(type?) → T→TypeError
        D2(<=0?)  → T→ValueError
        D3(daily) → T→ValueError
        D4(overdraft)→T→ValueError
        → succes
      [END]

    V(G) = 4 + 1 = 5
    """

    def test_withdraw_basis_path_p1_type_error(self):
        """P1: D1=True → TypeError."""
        with pytest.raises(TypeError):
            BankAccount("Test", 1_000.0).withdraw("cincizeci")

    def test_withdraw_basis_path_p2_nonpositive_amount(self):
        """P2: D1=False, D2=True → ValueError."""
        with pytest.raises(ValueError, match="pozitiva"):
            BankAccount("Test", 1_000.0).withdraw(0.0)

    def test_withdraw_basis_path_p3_daily_limit_exceeded(self):
        """P3: D1=F, D2=F, D3=True → ValueError."""
        with pytest.raises(ValueError, match="Limita zilnica"):
            BankAccount("Test", 10_000.0).withdraw(5_000.01)

    def test_withdraw_basis_path_p4_overdraft_exceeded(self):
        """P4: D1=F, D2=F, D3=F, D4=True → ValueError."""
        acc = BankAccount("Test", 100.0, "savings")
        with pytest.raises(ValueError, match="Fonduri insuficiente"):
            acc.withdraw(200.0)

    def test_withdraw_basis_path_p5_success(self):
        """P5: D1=F, D2=F, D3=F, D4=F → succes."""
        acc = BankAccount("Test", 1_000.0)
        result = acc.withdraw(300.0)
        assert result == 700.0
        assert acc.transactions_count == 1
        assert acc.daily_withdrawn == 300.0


class TestLoanBasisPaths:
    """
    Cele 5 circuite independente ale metodei is_eligible_for_loan().

    CFG:
      [START]
        D1(type?)      → T→TypeError
        D2(<=0?)       → T→ValueError
        D3(bal<=0 OR tx<MIN) [compusa] → T→False
        D4(loan>max?)  → T→False
        → True
      [END]

    V(G) = 4 + 1 = 5
    Condition coverage pentru D3 (OR compus) adauga 2 sub-cai:
      D3a: balance<=0 (True, short-circuit)
      D3b: balance>0 dar tx<MIN (True, a doua sub-conditie)
    """

    def test_loan_basis_path_p1_type_error(self):
        """P1: D1=True → TypeError."""
        acc = BankAccount("T", 1_000.0, transactions_count=5)
        with pytest.raises(TypeError):
            acc.is_eligible_for_loan([100])

    def test_loan_basis_path_p2_nonpositive_amount(self):
        """P2: D1=False, D2=True → ValueError."""
        acc = BankAccount("T", 1_000.0, transactions_count=5)
        with pytest.raises(ValueError, match="pozitiva"):
            acc.is_eligible_for_loan(-50.0)

    def test_loan_basis_path_p3a_zero_balance(self):
        """P3a: D1=F, D2=F, D3(D3a=True) → False (sold zero, short-circuit OR)."""
        acc = BankAccount("T", 0.0, transactions_count=10)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_loan_basis_path_p3b_insufficient_transactions(self):
        """P3b: D1=F, D2=F, D3(D3a=F, D3b=True) → False (tx insuficiente)."""
        acc = BankAccount("T", 1_000.0, transactions_count=3)
        assert acc.is_eligible_for_loan(100.0) is False

    def test_loan_basis_path_p4_amount_exceeds_max(self):
        """P4: D1=F, D2=F, D3=F, D4=True → False."""
        acc = BankAccount("T", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(3_000.0) is False

    def test_loan_basis_path_p5_success(self):
        """P5: toate deciziile False → True."""
        acc = BankAccount("T", 1_000.0, "checking", transactions_count=5)
        assert acc.is_eligible_for_loan(1_500.0) is True


# =============================================================================
# TESTE DE ACUMULARE – ucid mutatii de tip += → = si float() eliminat
# =============================================================================


class TestAccumulationAndConversion:
    """
    Teste care verifica comportamentul de acumulare (nu asignare simpla)
    si conversia la float in constructor.

    Mutatii vizate:
      M-ACC1: self.daily_withdrawn += amount  →  self.daily_withdrawn = amount
      M-ACC2: self.balance += amount (deposit) → self.balance = amount
      M-ACC3: self.transactions_count += 1     → self.transactions_count = 1
      M-FLOAT: float(balance) eliminat / float(daily_withdrawn) eliminat
    """

    def test_acc_daily_withdrawn_accumulates_over_multiple_withdrawals(self):
        """M-ACC1: doua retrageri → daily_withdrawn = suma lor, nu ultima."""
        acc = BankAccount("Test", 5_000.0)
        acc.withdraw(1_000.0)
        acc.withdraw(1_500.0)
        # Daca mutant face = in loc de +=, al doilea withdraw seteaza 1500
        assert acc.daily_withdrawn == 2_500.0

    def test_acc_balance_accumulates_across_deposits(self):
        """M-ACC2: trei depuneri de la sold initial → sold final cumulat."""
        acc = BankAccount("Test", 200.0)
        acc.deposit(300.0)
        acc.deposit(500.0)
        # Daca mutant face balance = amount, soldul ar fi 500, nu 1000
        assert acc.balance == 1_000.0

    def test_acc_transactions_count_cumulates_across_mixed_operations(self):
        """M-ACC3: doua deposit + un withdraw = 3 tranzactii, nu 1."""
        acc = BankAccount("Test", 1_000.0)
        acc.deposit(100.0)
        acc.deposit(100.0)
        acc.withdraw(50.0)
        assert acc.transactions_count == 3

    def test_conv_balance_stored_as_float_when_int_given(self):
        """M-FLOAT: balance=100 (int) trebuie stocat ca float(100) = 100.0."""
        acc = BankAccount("Test", 100)
        assert type(acc.balance) is float
        assert acc.balance == 100.0

    def test_conv_daily_withdrawn_stored_as_float_when_int_given(self):
        """M-FLOAT: daily_withdrawn=50 (int) trebuie stocat ca float."""
        acc = BankAccount("Test", 0.0, "checking", daily_withdrawn=50)
        assert type(acc.daily_withdrawn) is float
        assert acc.daily_withdrawn == 50.0

    def test_acc_withdraw_balance_decreases_cumulatively(self):
        """M-ACC: doua retrageri consecutive scad soldul corect."""
        acc = BankAccount("Test", 1_000.0)
        acc.withdraw(200.0)
        acc.withdraw(300.0)
        assert acc.balance == 500.0

    def test_acc_interest_adds_to_existing_balance(self):
        """Dobanda se aduna la sold, nu il inlocuieste (self.balance += interest)."""
        acc = BankAccount("Test", 2_000.0, "savings")
        acc.apply_interest()
        # 2000 + 2000*0.05 = 2000 + 100 = 2100
        # Daca mutant face balance = interest → balance ar fi 100
        assert acc.balance == pytest.approx(2_100.0)

    def test_acc_reset_daily_limit_sets_to_zero(self):
        """reset_daily_limit seteaza daily_withdrawn la 0, nu la alt numar."""
        acc = BankAccount("Test", 5_000.0)
        acc.withdraw(2_000.0)
        acc.reset_daily_limit()
        assert acc.daily_withdrawn == 0.0
        # Dupa reset, o noua retragere de 2000 trebuie sa reuseasca
        acc.withdraw(2_000.0)
        assert acc.daily_withdrawn == 2_000.0


# =============================================================================
# TESTE DE INTEGRARE
# =============================================================================


class TestIntegration:
    """Scenarii end-to-end care combina mai multe operatii."""

    def test_integration_full_loan_flow(self):
        """Cont nou → depuneri → eligibilitate credit (savings)."""
        acc = BankAccount("Popescu Ion", 0.0, "savings")
        for i in range(6):
            acc.deposit(200.0)
        assert acc.get_balance() == 1_200.0
        assert acc.get_transaction_count() == 6
        # savings multiplier=5 → max_loan=6000
        assert acc.is_eligible_for_loan(5_000.0) is True
        assert acc.is_eligible_for_loan(6_001.0) is False

    def test_integration_overdraft_then_interest(self):
        """Retragere cu descoperit checking → dobanda nu se aplica."""
        acc = BankAccount("Test", 100.0, "checking")
        acc.withdraw(500.0)  # balance = -400
        assert acc.apply_interest() == 0.0

    def test_integration_daily_limit_reset(self, high_balance_account):
        """Retragere la limita → reset → noua retragere posibila."""
        high_balance_account.withdraw(5_000.0)
        with pytest.raises(ValueError, match="Limita zilnica"):
            high_balance_account.withdraw(1.0)
        high_balance_account.reset_daily_limit()
        high_balance_account.withdraw(1_000.0)
        assert high_balance_account.balance == 4_000.0

    def test_integration_transfer_then_interest(self, checking_account, savings_account):
        """Transfer de la checking la savings → interest pe savings."""
        checking_account.transfer(savings_account, 500.0)
        interest = savings_account.apply_interest()
        assert interest == pytest.approx(75.0)  # 1500 * 0.05
        assert savings_account.balance == pytest.approx(1_575.0)

    def test_integration_premium_full_scenario(self):
        """Premium: depunere, dobanda, credit."""
        acc = BankAccount("VIP Client", 5_000.0, "premium", transactions_count=4)
        acc.deposit(1_000.0)  # balance=6000, tx=5
        interest = acc.apply_interest()  # 6000 * 0.08 = 480
        assert interest == pytest.approx(480.0)
        assert acc.balance == pytest.approx(6_480.0)
        # premium×10=64800 → 50000 eligibil
        assert acc.is_eligible_for_loan(50_000.0) is True
