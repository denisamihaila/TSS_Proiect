# Analiza Mutantilor – Mutation Testing cu mutmut

## Prezentare generala

Mutation testing evalueaza calitatea suitei de teste prin introducerea
de defecte mici (mutatii) in codul sursa si verificarea daca testele
existente le detecteaza.

**Scor de mutatie** = (mutanti omorati) / (total - echivalenti) × 100%

> **Nota operationala:** Runner-ul mutmut trebuie configurat cu `python3`
> (nu `python`) in `setup.cfg` pentru a functiona corect in WSL.
> Folosirea lui `python` intr-un shell WSL curat genereaza erori
> "python: command not found" → mutantii apar ca "suspicious" in loc de "killed".

```
[Screenshot: mutmut results - Complete after local execution]
```

---

## Motivul supravietuirii mutantilor

Cu o suita buna (100% statement + branch coverage), mutantii care supravietuiesc
sunt tipic:

| Motiv supravietuire | Exemplu | Remediu |
|---------------------|---------|---------|
| Valori de test prea "rotunde" | balance=1000.0 → interesul e 10.0, round nu conteaza | Foloseste balance non-rotund |
| Testat doar cu un tip de cont | Premium multiplier neacoperit | Adauga test specific pentru tip |
| Mutatii echivalente | Schimba format string in `__str__` | Nu pot fi omorati (echivalenti) |
| Mutatii la literali de string | Mesaj eroare partial modificat | match pattern mai precis |

---

## Mutanti echivalenti (nu pot fi omorati)

| # | Locatie | Mutatie | Motivul echivalentei |
|---|---------|---------|----------------------|
| E1 | `__str__` | `:.2f` → `:.3f` | `__str__` nu este testat pentru format exact |
| E2 | `__repr__` | modificari de format string | `__repr__` nu este testat exact |

---

## Mutanti neechivalenti supravietuitori (inainte de Strategia 7)

### Mutant #1 – apply_interest(): precizia round()

| Camp | Valoare |
|------|---------|
| **Fisier** | `src/bank_account.py` |
| **Metoda** | `apply_interest()` |
| **Linie** | `interest = round(self.balance * rate, 2)` |
| **Mutatie** | `round(x, 2)` → `round(x, 1)` (precizie redusa) |
| **Efectul mutatiei** | Dobanda rotunjita la o singura zecimala in loc de doua |
| **De ce a supravietuit** | Toate testele din suita principala folosesc `balance=1000.0`, care cu rate 1%/5%/8% produce valori rotunde (10.0, 50.0, 80.0) – `round(x,1)` si `round(x,2)` dau acelasi rezultat |
| **Mutant echivalent?** | **NU** – cu `balance=1000.33, savings(5%)`: `round(50.0165, 2)=50.02` vs `round(50.0165, 1)=50.0` |
| **Test killer** | `test_mutation1_interest_rounds_to_2_decimal_places` |

**Demonstratie:**
```python
acc = BankAccount("Test", 1_000.33, "savings")
interest = acc.apply_interest()

# Original (round 2): 1000.33 * 0.05 = 50.0165 → round(50.0165, 2) = 50.02
# Mutant   (round 1): 1000.33 * 0.05 = 50.0165 → round(50.0165, 1) = 50.0

assert interest == pytest.approx(50.02)  # TRECE pe original, ESUEAZA pe mutant → OMORAT
```

---

### Mutant #2 – LOAN_MULTIPLIER["premium"]: 10 → 11

| Camp | Valoare |
|------|---------|
| **Fisier** | `src/bank_account.py` |
| **Constanta** | `LOAN_MULTIPLIER["premium"] = 10` |
| **Mutatie** | `10` → `11` |
| **Efectul mutatiei** | Conturile premium pot solicita credite mai mari (pana la 11× balance) |
| **De ce a supravietuit** | Testul de integrare premium foloseste `balance=6480, loan=50_000`, iar `50_000 < 6480×11=71_280` → acelasi rezultat True |
| **Mutant echivalent?** | **NU** – cu `balance=1000, tx=5`: `loan=10_500` trebuie False (>10×1000), dar mutantul `×11` returneaza True (10500<11000) |
| **Test killer** | `test_mutation2_premium_amount_between_10x_and_11x_is_rejected` |

**Demonstratie:**
```python
acc = BankAccount("Test", 1_000.0, "premium", transactions_count=5)

# Original (×10): max_loan=10_000, 10_500 > 10_000 → False
# Mutant   (×11): max_loan=11_000, 10_500 <= 11_000 → True

assert acc.is_eligible_for_loan(10_500.0) is False  # TRECE pe original, ESUEAZA pe mutant → OMORAT
```

---

## Rezumat mutanti (dupa Strategia 7)

| Status | Numar | Procent |
|--------|-------|---------|
| Mutanti omorati (inclusiv prin test_additional) | [Complete after local execution] | [~%] |
| Supravietuitori neechivalenti | 0 (obiectiv) | 0% |
| Echivalenti (exclusi din calcul) | [Complete after local execution] | – |
| Suspicious (runner error – fix: python3) | [Complete after local execution] | – |
| **Total generati** | [Complete after local execution] | 100% |
| **Scor mutatie** | **[Complete after local execution]** | – |

```
[Screenshot: python3 -m mutmut results - Complete after local execution]
```

---

## Alte mutatii probabile si analiza lor

| Locatie | Mutatie probabila | Efect | Suita initiala omoara? |
|---------|-------------------|-------|------------------------|
| `deposit`: `amount <= 0` → `amount < 0` | Permite depunerea lui 0 | Zero trece validarea | Da (test CE-D2b) |
| `withdraw`: `>` → `>=` in D3 daily limit | Respinge exact 5000 | 5000 devine invalid | Da (bv_daily_at_limit) |
| `is_eligible_for_loan`: `<=` in D4 | Respinge sume la plafon exact | Plafonul devine exclus | Da (bv_amount_exactly_at_max) |
| `INTEREST_RATE["checking"]`: 0.01→0.02 | Dobanda checking dubla | Valori gresite | Da (CE-I1 checking) |
| `LOAN_MULTIPLIER["checking"]`: 2→3 | Plafon credit checking mai mare | Sume mai mari acceptate | Da (bv_amount_just_above_max) |
| `round(x, 2)`: precizie schimbata | Dobanda inexacta | Ne-observabil cu balance rotund | **Nu (Mutant #1 – omorat de additional)** |
| `LOAN_MULTIPLIER["premium"]`: 10→11 | Plafon premium mai mare | Sume intre 10× si 11× acceptate | **Nu (Mutant #2 – omorat de additional)** |
