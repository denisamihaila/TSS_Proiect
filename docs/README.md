# Documentatie Tehnica – TSS T1: Testare Unitara in Python

## Clasa testata: BankAccount

Acest document descrie in detaliu toate deciziile tehnice, strategiile de testare
implementate si modul in care fiecare cerinta a temei T1 este acoperita de cod.

---

## 1. Descrierea clasei BankAccount

### Atribute

| Atribut              | Tip     | Valoare implicita | Descriere                                   |
|----------------------|---------|-------------------|---------------------------------------------|
| `owner`              | `str`   | obligatoriu       | Proprietarul contului (strip-uit la stocare)|
| `balance`            | `float` | `0.0`             | Soldul curent                               |
| `account_type`       | `str`   | `"checking"`      | Tipul contului (checking/savings/premium)   |
| `transactions_count` | `int`   | `0`               | Numarul total de tranzactii efectuate       |
| `_daily_withdrawn`   | `float` | `0.0`             | Suma retrasa in ziua curenta (privat)       |

### Constante de clasa

| Constanta                | Valoare               | Semnificatie                            |
|--------------------------|-----------------------|-----------------------------------------|
| `MAX_DEPOSIT`            | 1_000_000.0           | Limita superioara exclusiva pt depuneri |
| `MAX_DAILY_WITHDRAWAL`   | 5_000.0               | Limita zilnica de retragere (inclusiva) |
| `OVERDRAFT_LIMIT`        | checking=-500, savings=0, premium=-2000 | Limita descoperit   |
| `INTEREST_RATE`          | checking=1%, savings=5%, premium=8%   | Rata dobanzii         |
| `LOAN_MULTIPLIER`        | checking=2, savings=5, premium=10     | Factor plafon credit  |
| `MIN_TRANSACTIONS_FOR_LOAN` | 5                  | Minim tranzactii pentru credit          |

---

## 2. Logica metodelor si decizii de implementare

### `deposit(amount)`

Validari (in ordine):
1. `not isinstance(amount, (int, float))` → TypeError
2. `amount <= 0` → ValueError
3. `amount >= MAX_DEPOSIT` → ValueError (frontiera *inclusiva la dreapta*)

Intervalul valid este **deschis** la ambele capete: `0 < amount < 1_000_000`.

### `withdraw(amount)`

Validari (in ordine, relevante pentru CFG):
1. Tip numeric (D1)
2. Valoare pozitiva (D2)
3. Limita zilnica (D3): `_daily_withdrawn + amount > MAX_DAILY_WITHDRAWAL`
4. Overdraft (D4): `new_balance < OVERDRAFT_LIMIT[account_type]`

Ordinea D3 inainte de D4 este deliberata: limita zilnica este o restrictie
globala independenta de contul specific, deci este verificata prima.

**V(G) = 4 + 1 = 5** → 5 cai independente (basis paths).

### `is_eligible_for_loan(loan_amount)`

Conditii evaluate succesiv:
1. Tip (D1): TypeError
2. Valoare (D2): ValueError
3. `balance <= 0` (D3): False
4. `transactions_count < MIN_TRANSACTIONS_FOR_LOAN` (D4): False
5. `loan_amount > balance * LOAN_MULTIPLIER[account_type]` (D5): False
6. Toate trecute: True

**V(G) = 5 + 1 = 6** → 6 cai independente.

---

## 3. Coverage – ce masoara tool-ul si ce este argumentat manual

### Ce masoara `coverage.py` / `pytest-cov`

- **Statement coverage (line coverage):** fiecare linie de cod executata cel putin o data.
  Tinta: **100%** pentru `src/bank_account.py`.
- **Branch coverage** (cu `--cov-branch`): fiecare ramura True/False a fiecarui `if`.
  Aceasta aproximeaza *decision coverage*, dar nu este identica.

### Ce NU masoara automat

- **Condition coverage:** fiecare sub-conditie dintr-o expresie compusa
  (ex: `A or B` – trebuie ca si A=True independent si B=True independent).
  Coverage.py trateaza intreaga expresie ca o singura ramura.
  → *Demonstrat manual prin analiza testelor din `TestConditionCoverage`.*

- **Basis path testing:** numarul minim de cai prin CFG.
  Coverage.py nu cunoaste conceptul de "cai independente" sau V(G).
  → *Demonstrat manual prin `TestWithdrawBasisPaths` si `TestLoanBasisPaths`,
    cu maparea explicita a fiecarui test la calea corespunzatoare.*

---

## 4. Mutation testing – metodologie

### De ce mutation testing?

100% statement coverage nu garanteaza absenta bug-urilor. Un test care
apeleaza o functie dar nu verifica rezultatul (assert) acopera liniile
dar nu detecteaza erori logice. Mutation testing masoara *puterea* testelor.

### Workflow

```bash
# 1. Rulare mutmut (in WSL cu venv activat)
python -m mutmut run

# 2. Vedere rezumat
python -m mutmut results

# 3. Detalii mutant specific
python -m mutmut show <id>
```

### Interpretare rezultate

- **Killed:** test a detectat diferenta → bine
- **Survived:** niciun test nu detecteaza diferenta → suita slaba
- **Timeout:** testele au rulat prea mult → posibil bucla infinita
- **Suspicious:** mutmut nu a putut rula testele

### Mutanti echivalenti

Un mutant este echivalent daca nu poate fi omorat de niciun test posibil,
deoarece comportamentul observable este identic cu originalul.
Acesti mutanti nu se numara in scorul de mutatie.

---

## 5. Rulare locala – instructiuni

### Prerequisite

```bash
# Crearea si activarea venv (prima data)
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/WSL/macOS:
source .venv/bin/activate

# Instalare dependente
pip install -r requirements.txt
```

### Rulare teste

```bash
# Teste simple
python -m pytest tests/ -v

# Cu coverage
python -m pytest --cov=src --cov-report=term-missing --cov-report=html

# Numai strategia 7
python -m pytest tests/test_bank_account_additional_mutation.py -v
```

### Mutation testing (necesita Linux/WSL cu mutmut 2.x)

```bash
python -m mutmut run
python -m mutmut results
```
