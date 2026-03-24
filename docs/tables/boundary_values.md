# Tabele: Analiza Valorilor de Frontiera

## deposit(amount) – frontiere

Interval valid: **0 < amount < 1_000_000** (ambele capete excluse)

| Valoare      | Relatia cu frontiera          | Tip    | Rezultat asteptat        | Test asociat                              |
|--------------|-------------------------------|--------|--------------------------|-------------------------------------------|
| -0.01        | Sub frontiera inferioara      | Invalid| ValueError               | `test_deposit_bv_just_below_zero`         |
| 0.00         | **Exact la frontiera inf.**   | Invalid| ValueError               | `test_deposit_bv_exactly_zero`            |
| **0.01**     | Primul valid (inf+epsilon)    | Valid  | sold = 0.01              | `test_deposit_bv_just_above_zero`         |
| 999_999.99   | Ultimul valid (sup-epsilon)   | Valid  | sold = 999_999.99        | `test_deposit_bv_just_below_max`          |
| **1_000_000.00** | **Exact la frontiera sup.** | Invalid| ValueError (>= check)    | `test_deposit_bv_exactly_max`             |
| 1_000_000.01 | Deasupra frontierei sup.      | Invalid| ValueError               | `test_deposit_bv_just_above_max`          |

---

## withdraw(amount) – frontiera limitei zilnice

Limita: **MAX_DAILY_WITHDRAWAL = 5_000** (inclusiva)

| Total retras in zi | Relatia cu frontiera         | Tip    | Rezultat asteptat  | Test asociat                               |
|--------------------|------------------------------|--------|--------------------|--------------------------------------------|
| 4_999.99           | Sub limita                   | Valid  | succes             | `test_withdraw_bv_daily_just_below_limit`  |
| **5_000.00**       | **Exact la limita**          | Valid  | succes             | `test_withdraw_bv_daily_exactly_at_limit`  |
| 5_000.01           | Peste limita                 | Invalid| ValueError         | `test_withdraw_bv_daily_just_above_limit`  |

---

## withdraw(amount) – frontiera overdraft (per tip de cont)

### checking – limita descoperit: **-500**

| Rezultat balance   | Relatia cu frontiera overdraft | Tip    | Rezultat asteptat  | Test asociat                                      |
|--------------------|-------------------------------|--------|--------------------|---------------------------------------------------|
| -499.99            | Deasupra limitei              | Valid  | succes             | `test_withdraw_bv_overdraft_checking_just_above_limit` |
| **-500.00**        | **Exact la limita**           | Valid  | succes             | `test_withdraw_bv_overdraft_checking_exactly_at_limit` |
| -500.01            | Sub limita                    | Invalid| ValueError         | `test_withdraw_bv_overdraft_checking_below_limit`      |

### savings – limita descoperit: **0** (fara descoperit)

| Rezultat balance   | Relatia cu frontiera overdraft | Tip    | Rezultat asteptat  | Test asociat                                    |
|--------------------|-------------------------------|--------|--------------------|--------------------------------------------------|
| 0.01               | Deasupra zero                 | Valid  | succes             | `test_withdraw_bv_overdraft_savings_just_above_zero`  |
| **0.00**           | **Exact zero**                | Valid  | succes             | `test_withdraw_bv_overdraft_savings_exactly_zero`     |
| -0.01              | Sub zero                      | Invalid| ValueError         | `test_withdraw_bv_overdraft_savings_below_zero`       |

### premium – limita descoperit: **-2_000**

| Rezultat balance   | Relatia cu frontiera overdraft | Tip    | Rezultat asteptat  | Test asociat                                      |
|--------------------|-------------------------------|--------|--------------------|---------------------------------------------------|
| -1_999.99          | Deasupra limitei              | Valid  | succes             | `test_withdraw_bv_overdraft_premium_just_above_limit` |
| **-2_000.00**      | **Exact la limita**           | Valid  | succes             | `test_withdraw_bv_overdraft_premium_exactly_at_limit` |
| -2_000.01          | Sub limita                    | Invalid| ValueError         | `test_withdraw_bv_overdraft_premium_below_limit`      |

---

## is_eligible_for_loan – frontiera transactions_count

Prag: **MIN_TRANSACTIONS_FOR_LOAN = 5** (inclusiv)

| transactions_count | Relatia cu pragul             | Tip    | Rezultat asteptat  | Test asociat                              |
|--------------------|-------------------------------|--------|--------------------|-------------------------------------------|
| 4                  | Sub prag (prag-1)             | Invalid| False              | `test_loan_bv_transactions_just_below_min`|
| **5**              | **Exact la prag**             | Valid  | True               | `test_loan_bv_transactions_exactly_at_min`|
| 6                  | Deasupra pragului (prag+1)    | Valid  | True               | `test_loan_bv_transactions_just_above_min`|

---

## is_eligible_for_loan – frontiera loan_amount vs plafon

Plafon: **balance * LOAN_MULTIPLIER** (inclusiv)

Exemplu: balance=1000, checking (multiplier=2) → max_loan=2000

| loan_amount  | Relatia cu plafonul    | Tip    | Rezultat asteptat  | Test asociat                           |
|--------------|------------------------|--------|--------------------|----------------------------------------|
| 1_999.99     | Sub plafon             | Valid  | True               | `test_loan_bv_amount_just_below_max`   |
| **2_000.00** | **Exact la plafon**    | Valid  | True               | `test_loan_bv_amount_exactly_at_max`   |
| 2_000.01     | Deasupra plafonului    | Invalid| False              | `test_loan_bv_amount_just_above_max`   |

---

## is_eligible_for_loan – frontiera balance

| balance  | Relatia cu frontiera | Tip    | Rezultat asteptat          | Test asociat                         |
|----------|----------------------|--------|----------------------------|--------------------------------------|
| 0.00     | Exact zero           | Invalid| False (balance <= 0)       | `test_loan_bv_balance_exactly_zero`  |
| 0.01     | Peste zero           | Valid  | True (daca loan OK)        | `test_loan_bv_balance_just_above_zero`|
