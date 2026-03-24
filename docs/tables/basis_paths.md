# Basis Path Testing – Circuite Independente

## Metoda `withdraw(amount)`

### Complexitate ciclomatica McCabe

```
V(G) = numar_decizii + 1 = 4 + 1 = 5
```

Decizii identificate in cod (marcate cu comentarii `# D1` ... `# D4`):

| ID | Linie | Decizie                                               |
|----|-------|-------------------------------------------------------|
| D1 | ~137  | `not isinstance(amount, (int, float))`                |
| D2 | ~139  | `amount <= 0`                                         |
| D3 | ~141  | `self._daily_withdrawn + amount > MAX_DAILY_WITHDRAWAL` |
| D4 | ~146  | `new_balance < overdraft_limit`                       |

### Graful de control al fluxului (CFG)

```
[START]
  |
  v
 [D1]--True--> [raise TypeError]
  |False
  v
 [D2]--True--> [raise ValueError "pozitiva"]
  |False
  v
 [D3]--True--> [raise ValueError "zilnica"]
  |False
  v
 [compute new_balance, overdraft_limit]
  |
  v
 [D4]--True--> [raise ValueError "insuficiente"]
  |False
  v
 [update state]
  |
  v
 [return balance]
```

### Cele 5 cai independente (baza)

| Cale | Decizii                          | Conditii de intrare               | Rezultat       | Test asociat                                    |
|------|----------------------------------|-----------------------------------|----------------|-------------------------------------------------|
| P1   | D1=True                          | amount="abc"                      | TypeError      | `test_withdraw_basis_path_p1_type_error`        |
| P2   | D1=False, D2=True                | amount=0.0                        | ValueError     | `test_withdraw_basis_path_p2_nonpositive_amount`|
| P3   | D1=F, D2=F, D3=True              | amount=5_001 (dep.zilnic=0)       | ValueError     | `test_withdraw_basis_path_p3_daily_limit_exceeded`|
| P4   | D1=F, D2=F, D3=F, D4=True       | savings, amount>balance           | ValueError     | `test_withdraw_basis_path_p4_overdraft_exceeded`|
| P5   | D1=F, D2=F, D3=F, D4=False      | amount=300, balance=1000          | succes         | `test_withdraw_basis_path_p5_success`           |

---

## Metoda `is_eligible_for_loan(loan_amount)`

### Complexitate ciclomatica McCabe

```
V(G) = numar_decizii + 1 = 5 + 1 = 6
```

Decizii identificate in cod (marcate cu comentarii `# D1` ... `# D5`):

| ID | Linie | Decizie                                                       |
|----|-------|---------------------------------------------------------------|
| D1 | ~195  | `not isinstance(loan_amount, (int, float))`                   |
| D2 | ~197  | `loan_amount <= 0`                                            |
| D3 | ~199  | `self.balance <= 0`                                           |
| D4 | ~201  | `self.transactions_count < self.MIN_TRANSACTIONS_FOR_LOAN`    |
| D5 | ~204  | `loan_amount > max_loan`                                      |

### Graful de control al fluxului (CFG)

```
[START]
  |
  v
 [D1]--True--> [raise TypeError]
  |False
  v
 [D2]--True--> [raise ValueError]
  |False
  v
 [D3]--True--> [return False  // sold insuficient]
  |False
  v
 [D4]--True--> [return False  // prea putine tranzactii]
  |False
  v
 [compute max_loan = balance * LOAN_MULTIPLIER[account_type]]
  |
  v
 [D5]--True--> [return False  // suma prea mare]
  |False
  v
 [return True]
```

### Cele 6 cai independente (baza)

| Cale | Decizii                                   | Conditii de intrare             | Rezultat | Test asociat                                     |
|------|-------------------------------------------|---------------------------------|----------|--------------------------------------------------|
| P1   | D1=True                                   | loan_amount=[100]               | TypeError| `test_loan_basis_path_p1_type_error`             |
| P2   | D1=F, D2=True                             | loan_amount=-50                 | ValueError| `test_loan_basis_path_p2_nonpositive_amount`    |
| P3   | D1=F, D2=F, D3=True                       | balance=0, tx=10                | False    | `test_loan_basis_path_p3_zero_balance`           |
| P4   | D1=F, D2=F, D3=F, D4=True                 | balance=1000, tx=3              | False    | `test_loan_basis_path_p4_insufficient_transactions`|
| P5   | D1=F, D2=F, D3=F, D4=F, D5=True           | balance=1000, tx=5, amount=3000 | False    | `test_loan_basis_path_p5_amount_exceeds_max`     |
| P6   | D1=F, D2=F, D3=F, D4=F, D5=False          | balance=1000, tx=5, amount=1500 | True     | `test_loan_basis_path_p6_all_conditions_met`     |

---

## Note metodologice

- **Basis path testing** (McCabe, 1976) garanteaza ca fiecare instructiune
  si fiecare ramura este executata cel putin o data.
- V(G) = E - N + 2P (E=muchii, N=noduri, P=componente conexe),
  sau echivalent: V(G) = numar_predicate + 1.
- Testele de baza formeaza un set **minim** care acopera toate caile
  independente. Celelalte teste din suita adauga robustete suplimentara.
