"""
Fixture-uri pytest partajate intre modulele de test.
"""
import pytest
from src.bank_account import BankAccount


@pytest.fixture
def checking_account() -> BankAccount:
    """Cont curent (checking) cu sold 1 000."""
    return BankAccount("Ion Popescu", 1_000.0, "checking")


@pytest.fixture
def savings_account() -> BankAccount:
    """Cont de economii (savings) cu sold 1 000."""
    return BankAccount("Maria Ionescu", 1_000.0, "savings")


@pytest.fixture
def premium_account() -> BankAccount:
    """Cont premium cu sold 1 000."""
    return BankAccount("Andrei Popa", 1_000.0, "premium")


@pytest.fixture
def empty_account() -> BankAccount:
    """Cont curent fara sold."""
    return BankAccount("Test User", 0.0, "checking")


@pytest.fixture
def account_with_transactions() -> BankAccount:
    """
    Cont cu exact MIN_TRANSACTIONS_FOR_LOAN (5) tranzactii inregistrate.
    Folosit pentru testele de eligibilitate la credit.
    """
    return BankAccount(
        "Test User",
        1_000.0,
        "checking",
        transactions_count=BankAccount.MIN_TRANSACTIONS_FOR_LOAN,
    )


@pytest.fixture
def high_balance_account() -> BankAccount:
    """Cont cu sold mare (10 000) pentru testarea limitei zilnice."""
    return BankAccount("Test User", 10_000.0, "checking")
