"""
Modul bank_account – implementarea clasei BankAccount.

Utilizat ca SUT (System Under Test) pentru demonstrarea strategiilor
de testare unitara in Python in cadrul cursului TSS T1.
"""
from __future__ import annotations


class BankAccount:
    """
    Modeleaza un cont bancar cu operatii de baza.

    Atribute de clasa:
        VALID_ACCOUNT_TYPES     : multimea tipurilor valide de cont
        MAX_DEPOSIT             : suma maxima admisa per depunere (exclusiv)
        MAX_DAILY_WITHDRAWAL    : limita zilnica de retragere (inclusiv)
        OVERDRAFT_LIMIT         : limita de descoperit de cont per tip
        INTEREST_RATE           : rata dobanzii per tip de cont
        LOAN_MULTIPLIER         : multiplicator pentru suma maxima de credit
        MIN_TRANSACTIONS_FOR_LOAN : numar minim de tranzactii pentru credit
    """

    VALID_ACCOUNT_TYPES = {"checking", "savings", "premium"}
    MAX_DEPOSIT = 1_000_000.0
    MAX_DAILY_WITHDRAWAL = 5_000.0
    OVERDRAFT_LIMIT = {
        "checking": -500.0,
        "savings": 0.0,
        "premium": -2_000.0,
    }
    INTEREST_RATE = {
        "checking": 0.01,
        "savings": 0.05,
        "premium": 0.08,
    }
    LOAN_MULTIPLIER = {
        "checking": 2,
        "savings": 5,
        "premium": 10,
    }
    MIN_TRANSACTIONS_FOR_LOAN = 5

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(
        self,
        owner: str,
        balance: float = 0.0,
        account_type: str = "checking",
        transactions_count: int = 0,
        daily_withdrawn: float = 0.0,
    ) -> None:
        """
        Initializeaza contul bancar.

        Args:
            owner             : proprietarul (str non-gol)
            balance           : sold initial (numeric, >= 0)
            account_type      : tipul contului (checking / savings / premium)
            transactions_count: numar initial de tranzactii (int, >= 0)
            daily_withdrawn   : suma retrasa azi (numeric, >= 0)

        Raises:
            TypeError : daca un parametru are tipul gresit
            ValueError: daca un parametru are o valoare invalida
        """
        # --- owner ---
        if not isinstance(owner, str):
            raise TypeError("owner trebuie sa fie de tip str")
        if not owner.strip():
            raise ValueError("owner trebuie sa fie un string non-gol")

        # --- balance – conditie compusa pentru condition coverage ---
        # Sub-conditia 1: isinstance(balance, bool) → True elimina True/False
        # Sub-conditia 2: not isinstance(balance, (int,float)) → elimina non-numerice
        if isinstance(balance, bool) or not isinstance(balance, (int, float)):
            raise TypeError("balance trebuie sa fie de tip numeric (int sau float)")
        if balance < 0:
            raise ValueError("balance trebuie sa fie non-negativ")

        # --- account_type ---
        if account_type not in self.VALID_ACCOUNT_TYPES:
            raise ValueError(
                f"Tip de cont invalid: {account_type!r}. "
                f"Valori acceptate: {self.VALID_ACCOUNT_TYPES}"
            )

        # --- transactions_count – conditie compusa pentru condition coverage ---
        if isinstance(transactions_count, bool) or not isinstance(transactions_count, int):
            raise TypeError("transactions_count trebuie sa fie de tip int")
        if transactions_count < 0:
            raise ValueError("transactions_count trebuie sa fie non-negativ")

        # --- daily_withdrawn – conditie compusa pentru condition coverage ---
        if isinstance(daily_withdrawn, bool) or not isinstance(daily_withdrawn, (int, float)):
            raise TypeError("daily_withdrawn trebuie sa fie de tip numeric")
        if daily_withdrawn < 0:
            raise ValueError("daily_withdrawn trebuie sa fie non-negativ")

        self.owner: str = owner.strip()
        self.balance: float = float(balance)
        self.account_type: str = account_type
        self.transactions_count: int = transactions_count
        self.daily_withdrawn: float = float(daily_withdrawn)  # atribut public

    # -------------------------------------------------------------------------
    # Operatii principale
    # -------------------------------------------------------------------------

    def deposit(self, amount: float) -> float:
        """
        Depune o suma in cont.

        Interval valid: 0 < amount < MAX_DEPOSIT (ambele capete excluse).

        Args:
            amount: suma de depus

        Returns:
            Soldul actualizat dupa depunere.

        Raises:
            TypeError : daca amount nu este numeric
            ValueError: daca amount <= 0 sau amount >= MAX_DEPOSIT
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Suma trebuie sa fie numerica")
        if amount <= 0:
            raise ValueError("Suma de depus trebuie sa fie pozitiva")
        if amount >= self.MAX_DEPOSIT:
            raise ValueError(
                f"Suma depaseste limita maxima permisa ({self.MAX_DEPOSIT})"
            )
        self.balance += amount
        self.transactions_count += 1
        return self.balance

    def withdraw(self, amount: float) -> float:
        """
        Retrage o suma din cont.

        Verificari succesive (reflectate explicit in CFG – D1..D4):
          D1: amount este numeric
          D2: amount > 0
          D3: limita zilnica nu este depasita
          D4: soldul nu scade sub limita de descoperit

        Args:
            amount: suma de retras

        Returns:
            Soldul actualizat dupa retragere.

        Raises:
            TypeError : daca amount nu este numeric
            ValueError: daca amount <= 0, limita zilnica depasita
                        sau descoperit de cont depasit
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):   # D1
            raise TypeError("Suma trebuie sa fie numerica")
        if amount <= 0:                                                          # D2
            raise ValueError("Suma de retras trebuie sa fie pozitiva")
        if self.daily_withdrawn + amount > self.MAX_DAILY_WITHDRAWAL:           # D3
            raise ValueError(
                f"Limita zilnica de retragere depasita "
                f"(maxim {self.MAX_DAILY_WITHDRAWAL})"
            )
        new_balance = self.balance - amount
        overdraft_limit = self.OVERDRAFT_LIMIT[self.account_type]
        if new_balance < overdraft_limit:                                        # D4
            raise ValueError(
                f"Fonduri insuficiente. "
                f"Limita de descoperit pentru acest cont: {overdraft_limit}"
            )
        self.balance = new_balance
        self.daily_withdrawn += amount
        self.transactions_count += 1
        return self.balance

    def transfer(self, target: "BankAccount", amount: float) -> dict:
        """
        Transfera o suma catre alt cont.

        Args:
            target: contul destinatar (alta instanta BankAccount)
            amount: suma de transferat

        Returns:
            Dict cu statusul operatiei:
            {"status": "success", "amount": ..., "from_owner": ..., "to_owner": ...}

        Raises:
            TypeError : daca target nu este BankAccount
            ValueError: daca target este acelasi cont sau amount este invalid
        """
        if not isinstance(target, BankAccount):
            raise TypeError("Destinatarul trebuie sa fie un BankAccount")
        if target is self:
            raise ValueError("Nu se poate transfera in acelasi cont")
        self.withdraw(amount)
        target.deposit(amount)
        return {
            "status": "success",
            "amount": amount,
            "from_owner": self.owner,
            "to_owner": target.owner,
        }

    def apply_interest(self) -> float:
        """
        Aplica dobanda pe soldul curent.

        Dobanda se aplica doar daca soldul este strict pozitiv.
        Rezultatul este rotunjit la 2 zecimale.

        Returns:
            Dobanda calculata si adaugata (0.0 daca balance <= 0).
        """
        if self.balance <= 0:
            return 0.0
        rate = self.INTEREST_RATE[self.account_type]
        interest = round(self.balance * rate, 2)
        self.balance += interest
        return interest

    def is_eligible_for_loan(self, loan_amount: float) -> bool:
        """
        Verifica eligibilitatea pentru un credit.

        Conditii evaluate succesiv:
          D1: loan_amount numeric
          D2: loan_amount > 0
          D3: conditie compusa – sold pozitiv SI tranzactii suficiente
              (balance > 0 AND transactions_count >= MIN_TRANSACTIONS_FOR_LOAN)
          D4: loan_amount <= balance * LOAN_MULTIPLIER[account_type]

        Conditia D3 este compusa (OR logic) pentru a oferi material
        de condition coverage testabil separat.

        Args:
            loan_amount: suma solicitata pentru credit

        Returns:
            True daca toate conditiile sunt indeplinite, False altfel.

        Raises:
            TypeError : daca loan_amount nu este numeric
            ValueError: daca loan_amount <= 0
        """
        if not isinstance(loan_amount, (int, float)) or isinstance(loan_amount, bool):  # D1
            raise TypeError("Suma creditului trebuie sa fie numerica")
        if loan_amount <= 0:                                                              # D2
            raise ValueError("Suma creditului trebuie sa fie pozitiva")

        # D3 – conditie compusa: sold insuficient SAU prea putine tranzactii
        # Sub-conditia D3a: self.balance <= 0
        # Sub-conditia D3b: self.transactions_count < self.MIN_TRANSACTIONS_FOR_LOAN
        if self.balance <= 0 or self.transactions_count < self.MIN_TRANSACTIONS_FOR_LOAN:  # D3
            return False

        max_loan = self.balance * self.LOAN_MULTIPLIER[self.account_type]
        if loan_amount > max_loan:                                                         # D4
            return False
        return True

    # -------------------------------------------------------------------------
    # Metode utilitare
    # -------------------------------------------------------------------------

    def get_balance(self) -> float:
        """Returneaza soldul curent."""
        return self.balance

    def get_transaction_count(self) -> int:
        """Returneaza numarul total de tranzactii efectuate."""
        return self.transactions_count

    def reset_daily_limit(self) -> None:
        """Reseteaza contorul zilnic de retrageri (apelat la sfarsit de zi)."""
        self.daily_withdrawn = 0.0

    # -------------------------------------------------------------------------
    # Reprezentari text
    # -------------------------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"BankAccount(owner={self.owner!r}, "
            f"balance={self.balance:.2f}, "
            f"type={self.account_type!r})"
        )

    def __repr__(self) -> str:
        return (
            f"BankAccount("
            f"owner={self.owner!r}, "
            f"balance={self.balance!r}, "
            f"account_type={self.account_type!r})"
        )
