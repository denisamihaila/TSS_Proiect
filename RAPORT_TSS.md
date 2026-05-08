# Raport TSS - T1 Testare unitara in Python

## 1. Context

Tema aleasa este T1: testare unitara in Python pentru functionalitatile unei
clase. Proiectul testeaza clasa `FitnessClassBooking`, iar functionalitatea
principala analizata este metoda:

```python
evaluate_client_package(session_history, package_sessions, has_membership)
```

Metoda evalueaza un pachet de sedinte pentru un client al unei sali de fitness.
Istoricul poate contine:

- `attended`: clientul a participat, sedinta se consuma;
- `no_show`: clientul nu a venit si nu a anuntat, sedinta se consuma;
- `cancelled`: clientul a anulat la timp, sedinta nu se consuma.

## 2. Cerinta structurala a profesoarei

Metoda respecta criteriile cerute:

| Criteriu | Implementare |
| --- | --- |
| minim 3 parametri | `session_history`, `package_sessions`, `has_membership` |
| instructiune repetitiva | `for session_status in session_history` |
| un `if` cu `else` | `if session_status == "attended": ... else: ...` |
| un `if` fara `else` | `if has_membership: ...` |
| conditie simpla | `has_membership` |
| conditie compusa | `remaining_sessions == 0 and no_show == 0` |

## 3. Specificatia metodei

Date de intrare:

- `session_history`: lista de statusuri pentru sedintele clientului;
- `package_sessions`: numarul total de sedinte cumparate, intre 1 si 20;
- `has_membership`: `True` daca se aplica reducerea de membership.

Date de iesire:

- `attended`: sedinte la care clientul a participat;
- `no_show`: sedinte pierdute prin neprezentare;
- `cancelled`: sedinte anulate la timp;
- `used_sessions`: `attended + no_show`;
- `remaining_sessions`: sedinte ramase;
- `total_cost`: costul pachetului, rotunjit la 2 zecimale;
- `status`: `active`, `completed` sau `completed_clean`.

Reguli de business:

- `attended` si `no_show` consuma sedinte;
- `cancelled` nu consuma sedinte;
- daca exista membership, costul total se reduce cu 20%;
- daca toate sedintele sunt consumate fara `no_show`, statusul este
  `completed_clean`;
- daca toate sedintele sunt consumate cu cel putin un `no_show`, statusul este
  `completed`;
- daca mai exista sedinte disponibile, statusul este `active`.

## 4. Partitionare in clase de echivalenta

Clase valide:

| ID | Clasa | Exemplu | Rezultat |
| --- | --- | --- | --- |
| EC1 | istoric gol valid | `([], 5, False)` | `active` |
| EC2 | istoric mixt valid | `(["attended", "no_show", "cancelled"], 5, True)` | calcule corecte + discount |
| EC3 | pachet complet fara no-show | `(["attended"], 1, False)` | `completed_clean` |
| EC4 | pachet complet cu no-show | `(["no_show"], 1, False)` | `completed` |

Clase invalide:

| ID | Clasa | Exemplu | Rezultat |
| --- | --- | --- | --- |
| EC5 | `session_history` nu este lista | `"attended"` | `ValueError` |
| EC6 | `package_sessions` nu este int | `"5"` | `ValueError` |
| EC7 | `has_membership` nu este bool | `"yes"` | `ValueError` |
| EC8 | status necunoscut | `["late"]` | `ValueError` |
| EC9 | sedinte consumate peste pachet | `(["attended", "no_show"], 1, False)` | `ValueError` |

Teste: `test_equivalence_partitioning.py`.

## 5. Analiza valorilor de frontiera

Frontiere pentru `package_sessions`:

| Caz | Valoare | Rezultat |
| --- | --- | --- |
| sub limita | `0` | `ValueError` |
| limita inferioara | `1` | valid |
| imediat peste limita | `2` | valid |
| imediat sub limita superioara | `19` | valid |
| limita superioara | `20` | valid |
| peste limita | `21` | `ValueError` |

Frontiera pentru finalizarea pachetului:

| Caz | Exemplu | Rezultat |
| --- | --- | --- |
| inainte de finalizare | 2 sedinte consumate din 3 | `active` |
| exact la finalizare, fara no-show | 3 attended din 3 | `completed_clean` |
| peste pachet | 4 consumate din 3 | `ValueError` |

Teste: `test_boundary_value_analysis.py`.

## 6. Testare structurala

Au fost urmarite:

- acoperire la nivel de instructiune;
- acoperire la nivel de decizie;
- acoperire la nivel de conditie;
- circuite independente.

Decizii principale:

| ID | Decizie |
| --- | --- |
| D1 | validarea parametrilor metodei |
| D2 | existenta unui element in `session_history` |
| D3 | validarea statusului curent |
| D4 | `session_status == "attended"` |
| D5 | `used_sessions > package_sessions` |
| D6 | `has_membership` |
| D7 | `remaining_sessions == 0 and no_show == 0` |

Diagrama CFG noua:

- `evaluate_client_package_cfg.drawio.svg`
- `evaluate_client_package_cfg.drawio.png`

Teste:

- `test_coverage.py`
- `test_independent_circuits.py`

## 7. Analiza mutanti

Mutmut a fost rulat in WSL cu runner explicit:

```bash
python -m mutmut run --paths-to-mutate fitness_class_booking.py \
                     --tests-dir . \
                     --runner "python -m pytest -q"
```

Rezultat final:

- mutanti supravietuitori: 0;
- mutanti suspiciosi: 7.

Testele suplimentare din `test_mutation.py` omoara mutanti comportamentali
neechivalenti relevanti:

- schimbarea incrementarii `no_show += 1` in `no_show = 1`;
- schimbarea incrementarii `cancelled += 1` in `cancelled = 1`;
- eliminarea/alterarea discountului de membership;
- schimbarea rotunjirii costului.

## 8. Rezultate finale

Comenzi rulate:

```bash
python -m pytest -q
python -m coverage run --branch -m pytest
python -m coverage report -m --include="fitness_class_booking.py"
```

Rezultate:

- teste: 66 passed;
- coverage pe `fitness_class_booking.py`: 100%;
- branch coverage pe `fitness_class_booking.py`: 100%;
- mutanti supravietuitori: 0.

Output-urile comenzilor sunt salvate in `logs/`.

## 9. Concluzie

Versiunea refacuta este mai focalizata decat varianta initiala: in loc de mai
multe metode si foarte multe teste distribuite pe functionalitati diferite,
proiectul testeaza o singura metoda suficient de bogata pentru a ilustra toate
strategiile cerute la curs.
