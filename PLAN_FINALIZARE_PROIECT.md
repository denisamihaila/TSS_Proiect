# Plan finalizare proiect TSS

Acest document contine ordinea recomandata pentru verificarea si finalizarea
proiectului refacut pe metoda `evaluate_client_package`.

## 1. [DONE] Verifica metoda principala

Deschide `fitness_class_booking.py` si verifica metoda:

```python
evaluate_client_package(session_history, package_sessions, has_membership)
```

Verifica daca metoda are logica dorita:

- `session_history`;
- `package_sessions`;
- `has_membership`;
- `attended`;
- `no_show`;
- `cancelled`;
- statusuri: `active`, `completed_successfully`, `completed_with_absences`.

Verifica explicit cerinta profesoarei:

- minim 3 parametri: `session_history`, `package_sessions`, `has_membership`;
- instructiune repetitiva: `for session_status in session_history`;
- `if` cu `else`: `if session_status == "attended": ... else: ...`;
- `if` fara `else`: `if has_membership: ...`;
- conditie simpla: `if has_membership`;
- conditie compusa: `if remaining_sessions == 0 and no_show == 0`.

## 2. [DONE] Ruleaza testele

Din folderul proiectului:

```bash
python -m pytest -q
```

Rezultat asteptat:

```text
99 passed
```

Pentru capturi mai detaliate:

```bash
python -m pytest -v
```

## 3. [DONE] Verifica testele functionale

Deschide in ordinea aceasta:

1. `test_equivalence_partitioning.py`
2. `test_boundary_value_analysis.py`

Verifica exemplele principale:

- istoric gol;
- istoric mixt;
- pachet complet fara `no_show`;
- pachet complet cu `no_show`;
- valori invalide;
- frontierele `0`, `1`, `2`, `19`, `20`, `21`.

## 4. [DONE] Verifica testele structurale

Deschide:

1. `test_coverage.py`
2. `test_independent_circuits.py`

Urmareste daca sunt acoperite:

- statement coverage;
- decision coverage;
- condition coverage;
- circuite independente.

Nu este nevoie sa memorezi fiecare test, dar este bine sa poti explica 2-3
exemple reprezentative.

## 5. [DONE] Verifica testele de mutatie

Deschide `test_mutation.py`.

Uita-te in special la testele pentru:

- mai multe `no_show`;
- mai multe `cancelled`;
- discount membership;
- rotunjire cost;
- mesaje de eroare stabile.

Acestea sunt bune de mentionat la prezentare, deoarece arata de ce au fost
adaugate teste suplimentare.

## 6. [DONE] Ruleaza coverage

Ruleaza:

```bash
python -m coverage run --branch -m pytest
python -m coverage report -m --include="fitness_class_booking.py"
```

Rezultat asteptat:

```text
fitness_class_booking.py  100%
```

Pentru raport HTML:

```bash
python -m coverage html --include="fitness_class_booking.py"
```

Verifica apoi:

```text
htmlcov/index.html
```

## 7. [DONE] Ruleaza mutmut in WSL

In WSL, din folderul proiectului:

```bash
python -m mutmut run --paths-to-mutate fitness_class_booking.py --tests-dir . --runner "python -m pytest -q"
python -m mutmut results
```

Rezultat asteptat:

```text
95/95
Killed: 80
Timeout: 0
Suspicious: 15
Survived: 0
Skipped: 0
```

Se poate verifica si logul deja generat:

```text
logs/mutmut_results.txt
```

## 8. Verifica README-ul

Deschide `README.md` si citeste-l cap-coada.

Verifica daca:

- nu mai descrie metodele vechi ca functionalitati active;
- explica metoda noua;
- include cerinta profesoarei;
- include comenzile de rulare;
- include rezultatele finale;
- mentioneaza raportul, prezentarea, logurile si CFG-ul.

## 9. Verifica raportul

Deschide `RAPORT_TSS.md`.

Citeste-l ca document final si verifica:

- daca explicatia metodei este clara;
- daca tabelele sunt corecte;
- daca strategiile de testare sunt explicate;
- daca rezultatele corespund rularilor locale.

Din acest fisier poti construi raportul Word final.

## 10. Verifica prezentarea

Deschide `PREZENTARE_TSS.md`.

Foloseste-l ca ordine pentru PowerPoint:

1. Titlu
2. Cerinta
3. De ce ai refacut proiectul
4. Functionalitatea aleasa
5. Semnatura metodei
6. Reguli de business
7. Cerinta profesoarei bifata
8. Testare functionala
9. Valori de frontiera
10. Testare structurala
11. CFG
12. Coverage
13. Mutmut
14. Rezultate finale
15. Concluzie

## 11. [DONE] Verifica diagrama CFG

Deschide:

```text
evaluate_client_package_cfg.drawio.png
```

Daca arata bine, foloseste-o in raport si in PowerPoint. Daca pare prea
incarcata pentru slide, pune versiunea completa in raport si foloseste in
prezentare doar o varianta simplificata verbal.

## 12. [DONE] Refa capturile

Dupa ce totul este verificat, fa capturi noi pentru:

1. `python -m pytest -q`
2. `python -m coverage run --branch -m pytest`
3. `python -m coverage report -m --include="fitness_class_booking.py"`
4. `python -m coverage html --include="fitness_class_booking.py"`
5. `mutmut run ...`
6. `mutmut results`

Capturile finale realizate:

1. `01_pytest_99_passed.png`
2. `02_coverage_run_99_passed.png`
3. `03_coverage_report_100_percent.png`
4. `04_coverage_html_generated.png`
5. `05_mutmut_run.png`
6. `06_mutmut_results.png`

Pune capturile noi in folderul:

```text
screenshots/
```

## 13. Refa Word si PowerPoint

Ordine recomandata:

1. transforma `RAPORT_TSS.md` in raport Word;
2. transforma `PREZENTARE_TSS.md` in PowerPoint;
3. adauga capturile noi;
4. adauga diagrama CFG;
5. sterge orice urma din metodele vechi.

## 14. Ultima verificare inainte de predare

Ruleaza:

```bash
python -m pytest -q
python -m coverage run --branch -m pytest
python -m coverage report -m --include="fitness_class_booking.py"
```

In WSL:

```bash
python -m mutmut run --paths-to-mutate fitness_class_booking.py --tests-dir . --runner "python -m pytest -q"
python -m mutmut results
```

Cauta referinte la metodele vechi:

```bash
rg "book_spot|cancel_booking|calculate_cost|max_spots|waitlist"
```

Este acceptabil sa apara doar in documente care mentioneaza ca metodele vechi
au fost eliminate. Nu ar trebui sa apara in codul principal sau in teste.

## Ordinea scurta

```text
cod -> teste -> coverage -> mutmut -> README -> raport -> prezentare -> capturi -> verificare finala
```
