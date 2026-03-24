# Tabele: Partitionare in Clase de Echivalenta

## deposit(amount)

| ID    | Clasa                  | Conditie                          | Tip     | Valoare exemplu | Rezultat asteptat   |
|-------|------------------------|-----------------------------------|---------|-----------------|---------------------|
| CE-D1 | Suma valida            | 0 < amount < 1_000_000            | Valida  | 500.0           | sold actualizat     |
| CE-D2 | Suma non-pozitiva      | amount <= 0                       | Invalida| -100.0, 0.0     | ValueError          |
| CE-D3 | Suma peste limita      | amount >= 1_000_000               | Invalida| 1_000_000.0     | ValueError          |
| CE-D4 | Tip invalid            | not isinstance(amount, (int,float))| Invalida| "500", None    | TypeError           |

**Teste asociate:** `TestDepositEquivalenceClasses`

---

## withdraw(amount)

| ID    | Clasa                     | Conditie                                  | Tip     | Valoare exemplu | Rezultat asteptat     |
|-------|---------------------------|-------------------------------------------|---------|-----------------|-----------------------|
| CE-W1 | Retragere valida          | amount > 0, fonduri ok, sub limita zilnica | Valida  | 500.0           | sold actualizat       |
| CE-W2 | Suma non-pozitiva         | amount <= 0                               | Invalida| 0.0, -50.0      | ValueError            |
| CE-W3 | Fonduri insuficiente      | balance - amount < overdraft_limit        | Invalida| 2000.0 (savings)| ValueError            |
| CE-W4 | Limita zilnica depasita   | daily_withdrawn + amount > 5_000          | Invalida| 5_001.0         | ValueError            |
| CE-W5 | Tip invalid               | not isinstance(amount, ...)               | Invalida| "100"           | TypeError             |

**Teste asociate:** `TestWithdrawEquivalenceClasses`

---

## __init__ (constructor)

| Parametru          | ID      | Clasa                | Conditie                             | Tip     | Valoare exemplu | Rezultat        |
|--------------------|---------|----------------------|--------------------------------------|---------|-----------------|-----------------|
| owner              | CE-O1   | Valid                | isinstance(str) and strip()!=""      | Valida  | "Ion Popescu"   | creat OK        |
| owner              | CE-O2   | Gol                  | owner == ""                          | Invalida| ""              | ValueError      |
| owner              | CE-O3   | Whitespace           | owner.strip() == ""                  | Invalida| "   "           | ValueError      |
| owner              | CE-O4   | Non-string           | not isinstance(owner, str)           | Invalida| 123             | ValueError      |
| balance            | CE-B1   | Valid                | balance >= 0                         | Valida  | 0.0, 500.0      | creat OK        |
| balance            | CE-B2   | Negativ              | balance < 0                          | Invalida| -100.0          | ValueError      |
| balance            | CE-B3   | Non-numeric          | not isinstance(balance, (int,float)) | Invalida| "abc"           | ValueError      |
| account_type       | CE-AT1  | Valid                | account_type in valid_types          | Valida  | "checking"      | creat OK        |
| account_type       | CE-AT2  | Invalid              | account_type not in valid_types      | Invalida| "platinum"      | ValueError      |
| transactions_count | CE-TC1  | Valid                | isinstance(int) and >= 0             | Valida  | 0, 5            | creat OK        |
| transactions_count | CE-TC2  | Negativ              | transactions_count < 0               | Invalida| -1              | ValueError      |
| transactions_count | CE-TC3  | Non-int              | not isinstance(..., int)             | Invalida| 1.5             | ValueError      |
| daily_withdrawn    | CE-DW1  | Valid                | isinstance(numeric) and >= 0         | Valida  | 0.0             | creat OK        |
| daily_withdrawn    | CE-DW2  | Negativ              | daily_withdrawn < 0                  | Invalida| -10.0           | ValueError      |
| daily_withdrawn    | CE-DW3  | Non-numeric          | not isinstance(...)                  | Invalida| "abc"           | ValueError      |

**Teste asociate:** `TestInitEquivalenceClasses`

---

## apply_interest()

| ID    | Clasa              | Conditie       | Tip     | Setup exemplu         | Rezultat asteptat           |
|-------|--------------------|--------------  |---------|-----------------------|-----------------------------|
| CE-I1 | Sold pozitiv       | balance > 0    | Valida  | balance=1000, checking| interest=10.0, balance=1010 |
| CE-I2 | Sold zero/negativ  | balance <= 0   | -       | balance=0.0           | interest=0.0                |

**Dobanda per tip:** checking=1%, savings=5%, premium=8%

---

## is_eligible_for_loan(loan_amount)

| ID    | Clasa                    | Conditie                           | Tip     | Setup exemplu                    | Rezultat |
|-------|--------------------------|------------------------------------|---------|----------------------------------|----------|
| CE-L1 | Eligibil                 | toate conditiile OK                | Valida  | balance=1000, tx=5, amount=500   | True     |
| CE-L2 | Sold insuficient         | balance <= 0                       | Invalida| balance=0, tx=10, amount=100     | False    |
| CE-L3 | Prea putine tranzactii   | transactions_count < 5             | Invalida| balance=1000, tx=2, amount=100   | False    |
| CE-L4 | Suma prea mare           | loan_amount > balance * multiplier | Invalida| balance=1000, tx=5, amount=3000  | False    |
| CE-L5 | Tip invalid              | not isinstance(loan_amount, ...)   | Invalida| loan_amount="500"                | TypeError|
| CE-L6 | Suma non-pozitiva        | loan_amount <= 0                   | Invalida| loan_amount=0.0                  | ValueError|

**Multiplicator per tip:** checking=2, savings=5, premium=10

---

## transfer(target, amount)

| ID    | Clasa                   | Conditie                          | Tip     | Rezultat   |
|-------|-------------------------|-----------------------------------|---------|------------|
| CE-T1 | Transfer valid          | target BankAccount diferit, suma ok| Valida | True       |
| CE-T2 | Target invalid          | not isinstance(target, BankAccount)| Invalida| TypeError |
| CE-T3 | Transfer catre sine     | target is self                    | Invalida| ValueError |
| CE-T4 | Fonduri insuficiente    | withdraw esueaza                  | Invalida| ValueError |
