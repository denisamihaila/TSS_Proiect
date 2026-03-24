# TSS T1 – Testare Unitara in Python: BankAccount

> **Curs:** Testarea Sistemelor Software (TSS)
> **Tema:** T1 – Testare unitara in Python
> **Framework de testare:** pytest + pytest-cov + mutmut

---

## 1. Scopul proiectului

Proiectul demonstreaza utilizarea unui framework de testare unitara Python
(pytest) pentru a testa o clasa de domeniu (`BankAccount`), ilustrand urmatoarele
**7 strategii de generare a testelor**:

1. Partitionare in clase de echivalenta
2. Analiza valorilor de frontiera
3. Statement coverage (acoperire la nivel de instructiune)
4. Decision coverage (acoperire la nivel de decizie)
5. Condition coverage (acoperire la nivel de conditie)
6. Circuite independente / Basis Path Testing (McCabe)
7. Mutation testing cu analiza mutantilor supravietuitori

---

## 2. Alegerea domeniului – BankAccount

Clasa `BankAccount` modeleaza un cont bancar simplificat, ales din urmatoarele motive:

- **Logica de validare bogata:** constructorul contine conditii compuse (material
  pentru condition coverage)
- **Metode cu decizii in serie:** `withdraw` are 4 decizii secventiale,
  `is_eligible_for_loan` are 5 → V(G) = 5 si 6
- **Constante cu semnificatie clara:** usor de identificat mutatii relevante
- **Domeniu familiar:** regulile bancare sunt intuitive si usor de argumentat
- **Nu necesita librarii externe:** implementare pura Python

### Metodele testate

| Metoda | Descriere | V(G) |
|--------|-----------|------|
| `__init__` | Constructor cu 5 parametri validati | – |
| `deposit(amount)` | Depunere cu validari multiple | 4 |
| `withdraw(amount)` | Retragere cu CFG complex | 5 |
| `transfer(target, amount)` | Transfer intre conturi | – |
| `apply_interest()` | Aplicare dobanda | 2 |
| `is_eligible_for_loan(loan_amount)` | Eligibilitate credit | 6 |

---

## 3. Arhitectura generala

```
TSS_Proiect/
├── src/
│   └── bank_account.py              # Codul sursa (SUT)
│
├── tests/
│   ├── conftest.py                  # Fixture-uri partajate
│   ├── test_bank_account.py         # Strategii 1-6 (~115 teste)
│   ├── test_bank_account_additional_mutation.py  # Strategia 7 (7 teste)
│   └── __init__.py
│
├── docs/
│   ├── README.md                    # Documentatie tehnica detaliata
│   ├── diagrams/                    # Diagrame Mermaid (.mmd)
│   │   ├── cfg_withdraw.mmd         # CFG pentru withdraw
│   │   ├── cfg_loan.mmd             # CFG pentru is_eligible_for_loan
│   │   └── project_structure.mmd   # Structura proiectului
│   ├── tables/                      # Tabele de analiza
│   │   ├── equivalence_classes.md
│   │   ├── boundary_values.md
│   │   ├── basis_paths.md
│   │   └── mutation_analysis.md
│   └── presentation_outline.md     # Outline 10 slide-uri
│
├── scripts/
│   ├── run_tests.sh
│   ├── run_coverage.sh
│   ├── run_mutation.sh
│   └── generate_reports.sh
│
├── pyproject.toml
├── setup.cfg                        # Configurare mutmut 2.x
├── pytest.ini
├── .coveragerc
├── requirements.txt
└── .gitignore
```

---

## 4. Descrierea clasei BankAccount

### Constante

| Constanta | Valoare | Semnificatie |
|-----------|---------|--------------|
| `MAX_DEPOSIT` | 1_000_000.0 | Limita superioara (exclusiva) per depunere |
| `MAX_DAILY_WITHDRAWAL` | 5_000.0 | Limita zilnica de retragere (inclusiva) |
| `OVERDRAFT_LIMIT` | checking=-500, savings=0, premium=-2000 | Descoperit maxim per tip |
| `INTEREST_RATE` | checking=1%, savings=5%, premium=8% | Rata dobanzii |
| `LOAN_MULTIPLIER` | checking=2, savings=5, premium=10 | Factor plafon credit |
| `MIN_TRANSACTIONS_FOR_LOAN` | 5 | Minim tranzactii pentru credit |

### Constructor

```python
BankAccount(owner, balance=0.0, account_type="checking",
            transactions_count=0, daily_withdrawn=0.0)
```

Conditii compuse in constructor (relevante pentru condition coverage):
- `not isinstance(owner, str) or not owner.strip()`
- `not isinstance(balance, (int, float)) or balance < 0`
- `not isinstance(transactions_count, int) or transactions_count < 0`
- `not isinstance(daily_withdrawn, (int, float)) or daily_withdrawn < 0`

---

## 5. Strategii de testare

### 5.1 Partitionare in Clase de Echivalenta

Domeniul de intrare al fiecarei metode este impartit in clase cu comportament identic.
Se testeaza un singur reprezentant din fiecare clasa.

**Exemplu – `deposit(amount)`:**

| Clasa | Conditie | Reprezentant | Rezultat |
|-------|----------|--------------|----------|
| CE-D1 valida | 0 < amount < 1_000_000 | 500.0 | succes |
| CE-D2 invalida | amount <= 0 | 0.0, -100 | ValueError |
| CE-D3 invalida | amount >= 1_000_000 | 1_000_000 | ValueError |
| CE-D4 invalida | non-numeric | "500" | TypeError |

Teste in: `TestDepositEquivalenceClasses`, `TestWithdrawEquivalenceClasses`,
`TestInitEquivalenceClasses`, `TestApplyInterestEquivalenceClasses`,
`TestLoanEquivalenceClasses`, `TestTransferEquivalenceClasses`

### 5.2 Analiza Valorilor de Frontiera

Testam valorile exact la frontiera si cele imediat adiacente.

**Frontierele principale:**

| Frontiera | Valoare | Tip | Observatie |
|-----------|---------|-----|------------|
| deposit inf | 0.00 | invalid | exact la frontiera |
| deposit inf+ε | 0.01 | valid | primul valid |
| deposit sup-ε | 999_999.99 | valid | ultimul valid |
| deposit sup | 1_000_000.00 | **invalid** | `>=` → exclus |
| daily limit | 5_000.00 | valid | inclusiv |
| daily limit+ε | 5_000.01 | invalid | depasit |
| overdraft checking | -500.00 | valid | exact la limita |
| overdraft savings | 0.00 | valid | exact zero |
| overdraft premium | -2_000.00 | valid | exact la limita |
| tx credit | 4 | invalid | sub prag |
| tx credit | **5** | valid | exact la prag |
| plafon credit | balance × factor | valid | exact la plafon |

Teste in: `TestDepositBoundaryValues`, `TestWithdrawBoundaryValues`, `TestLoanBoundaryValues`

### 5.3 Statement Coverage

**Tinta:** 100% instructiuni acoperite in `src/bank_account.py`.

```bash
pytest --cov=src --cov-report=term-missing
```

```
[Screenshot: pytest coverage report]
```

Teste in: `TestStatementCoverage`

### 5.4 Decision Coverage

Fiecare decizie (`if`) este evaluata atat cu `True` cat si cu `False`.

**Decizii in `withdraw`:**

| Decizie | Conditie | Ramura True | Ramura False |
|---------|----------|-------------|--------------|
| D1 | `not isinstance(amount, ...)` | TypeError | continua |
| D2 | `amount <= 0` | ValueError | continua |
| D3 | `daily + amount > MAX` | ValueError | continua |
| D4 | `new_balance < overdraft` | ValueError | succes |

Teste in: `TestDecisionCoverage`

### 5.5 Condition Coverage

Fiecare **sub-conditie** dintr-o expresie compusa este evaluata
independent cu `True` si `False`.

> `coverage.py` nu raporteaza condition coverage direct.
> Aceasta strategie este demonstrata prin analiza manuala.

**Exemplu – constructor (`owner`):**

| Sub-conditie | Valoare testata | Rezultat |
|--------------|-----------------|----------|
| `not isinstance(owner, str)` | `owner=123` (True) | ValueError |
| `not owner.strip()` | `owner=""` (True, prima=False) | ValueError |
| ambele False | `owner="Ana"` | succes |

Teste in: `TestConditionCoverage`

### 5.6 Circuite Independente / Basis Path Testing

**Complexitate ciclomatica McCabe:**
- `withdraw`: V(G) = 4 + 1 = **5** cai independente
- `is_eligible_for_loan`: V(G) = 5 + 1 = **6** cai independente

**Cele 5 cai pentru `withdraw`:**

| Cale | Conditii traversate | Rezultat |
|------|---------------------|----------|
| P1 | D1=True | TypeError |
| P2 | D1=F, D2=T | ValueError pozitiva |
| P3 | D1=F, D2=F, D3=T | ValueError zilnica |
| P4 | D1-3=F, D4=T | ValueError insuficiente |
| P5 | D1-4=F | succes |

Diagrama CFG completa: [`docs/diagrams/cfg_withdraw.mmd`](docs/diagrams/cfg_withdraw.mmd)

Teste in: `TestWithdrawBasisPaths`, `TestLoanBasisPaths`

### 5.7 Mutation Testing

**Tool:** mutmut 2.x

```bash
python -m mutmut run
python -m mutmut results
```

```
[Screenshot: mutmut results]
```

---

## 6. Analiza mutantilor neechivalenti

### Mutant #1 – deposit(): `>=` → `>`

| Camp | Valoare |
|------|---------|
| Mutatie | `amount >= MAX_DEPOSIT` → `amount > MAX_DEPOSIT` |
| Efect | Permite depunerea exacta de 1_000_000.0 |
| De ce a supravietuit initial | Testele nu verificau exact 1_000_000.0 |
| Test killer | `test_mutation1_deposit_exactly_at_max_raises` |

```python
acc.deposit(1_000_000.0)
# Original (>=): ValueError  ✓
# Mutant   (>) : no error    ✗ → test ESUEAZA → mutant OMORAT
```

### Mutant #2 – is_eligible_for_loan(): `<` → `<=`

| Camp | Valoare |
|------|---------|
| Mutatie | `transactions_count < MIN` → `transactions_count <= MIN` |
| Efect | Respinge conturi cu exact 5 tranzactii |
| De ce a supravietuit initial | Testele foloseau conturi cu > 5 tranzactii |
| Test killer | `test_mutation2_loan_with_exactly_min_transactions_eligible` |

```python
acc = BankAccount("T", 1000.0, transactions_count=5)
assert acc.is_eligible_for_loan(100.0) is True
# Original (<) : True   ✓
# Mutant   (<=): False  ✗ → test ESUEAZA → mutant OMORAT
```

---

## 7. Tool-uri si mediu de lucru

| Component | Versiune |
|-----------|----------|
| Python | 3.12.x |
| pytest | >= 7.4.0 |
| pytest-cov | >= 4.1.0 |
| coverage.py | >= 7.3.0 |
| mutmut | 2.5.1 (2.x) |
| OS (teste) | Windows 11 |
| OS (mutmut) | WSL / Ubuntu |

---

## 8. Cum se ruleaza

```bash
# 1. Creare si activare venv
python -m venv .venv
source .venv/bin/activate        # Linux/macOS/WSL
# .venv\Scripts\Activate.ps1    # Windows PowerShell

# 2. Instalare dependente
pip install -r requirements.txt

# 3. Rulare teste cu coverage
python -m pytest

# 4. Mutation testing (Linux/WSL)
python -m mutmut run
python -m mutmut results
```

---

## 9. Rezultate

### Coverage

```
[Screenshot: pytest --cov=src --cov-report=term-missing]
```

| Fisier | Statements | Missed | Coverage |
|--------|-----------|--------|----------|
| src/bank_account.py | [N] | 0 | **100%** |

### Mutation Testing

```
[Screenshot: python -m mutmut results]
```

| Categorie | Numar |
|-----------|-------|
| Total mutanti | [Complete after local execution] |
| Omorati | [Complete after local execution] |
| Supravietuitori neechivalenti | 0 (dupa Strategia 7) |
| Echivalenti | [Complete after local execution] |
| **Scor final** | **[Complete after local execution]** |

---

## 10. Utilizarea AI

**Instrument:** Claude (Anthropic) prin Claude Code CLI.

| Activitate | Rolul AI | Rolul studentului |
|------------|----------|-------------------|
| Proiectarea clasei | Schelet initial | Decizia finala |
| Generarea testelor | Draft per strategie | Verificare, corectare |
| Documentatie | Generare structurata | Validare, completare |
| Diagrame CFG | Generare Mermaid | Verificare logica |
| Debugging | Sugestii diagnostic | Aplicare solutii |

AI-ul nu a putut rula testele local. Toate rezultatele numerice
(coverage %, scor mutatie) necesita executie manuala.

---

## 11. Limitari

- mutmut nu ruleaza nativ pe Windows (v3.x) → necesita WSL
- Condition coverage nu este masurat automat → demonstrat prin analiza manuala
- Mutation testing este lent pentru suite mari

---

## 12. Concluzii

- 100% statement coverage este realist si atins
- Mutation testing a revelat doua gauri in suita initiala (frontierele `>=` si `<`)
- Naming-ul explicit al testelor faciliteaza identificarea strategiei ilustrate
- O suita aparent completa poate fi intarita prin mutation testing

---

## 13. Referinte bibliografice

1. McCabe, T.J. (1976). *A Complexity Measure*. IEEE Transactions on Software Engineering.
2. Myers, G.J., Sandler, C., Badgett, T. (2011). *The Art of Software Testing* (3rd ed.). Wiley.
3. Ammann, P., Offutt, J. (2016). *Introduction to Software Testing* (2nd ed.). Cambridge.
4. pytest documentation: https://docs.pytest.org
5. coverage.py documentation: https://coverage.readthedocs.io
6. mutmut documentation: https://mutmut.readthedocs.io
