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
100 passed
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
Killed: 85
Timeout: 0
Suspicious: 10
Survived: 0
Skipped: 0
```

Se poate verifica si logul deja generat:

```text
logs/mutmut_results.txt
```

## 8. [DONE] Verifica Cosmic Ray

Artefactele Cosmic Ray sunt pastrate in:

```text
cosmic_ray/
```

Rezultatul documentat:

```text
Mutanti generati/finalizati: 166
Mutanti supravietuitori: 9
Rata supravietuire: 5.42%
Scor aproximativ omorare mutanti: 94.58%
```

Copia completa `copy_project/` nu trebuie pastrata in proiectul final,
deoarece contine teste duplicate si poate strica rularea implicita `pytest`.

## 9. Verifica README-ul

Deschide `README.md` si citeste-l cap-coada.

Verifica daca:

- nu mai descrie metodele vechi ca functionalitati active;
- explica metoda noua;
- include cerinta profesoarei;
- include comenzile de rulare;
- include rezultatele finale;
- mentioneaza prezentarea, logurile, capturile si diagramele.

## 10. [DONE] Verifica documentatia finala

Documentatia finala este in `README.md`.

Citeste README-ul ca document final si verifica:

- daca explicatia metodei este clara;
- daca tabelele sunt corecte;
- daca strategiile de testare sunt explicate;
- daca rezultatele corespund rularilor locale.

Nu mai este necesar un raport separat in Markdown.

## 11. Verifica prezentarea

Deschide `PREZENTARE_TSS.md`.

Foloseste-l ca ordine pentru PowerPoint:

1. Titlu
2. Cerinta si alegerea functionalitatii
3. Modelul de business
4. Structura metodei si validari
5. Testare functionala
6. Testare structurala si diagrame
7. Coverage
8. Mutmut + Cosmic Ray
9. Suita AI si comparatia
10. Rezultate finale si concluzie

## 12. [DONE] Verifica diagramele

Deschide:

```text
cfg_diagrama.drawio.png
cause_effect_graph.png
```

Daca arata bine, foloseste-le in README si in PowerPoint. Daca diagrama CFG
pare prea incarcata pentru slide, pune versiunea completa in README si
foloseste in prezentare doar o varianta simplificata verbal.

## 13. [DONE] Refa capturile

Dupa ce totul este verificat, fa capturi noi pentru:

1. `python -m pytest -q`
2. `python -m coverage run --branch -m pytest`
3. `python -m coverage report -m --include="fitness_class_booking.py"`
4. `python -m coverage html --include="fitness_class_booking.py"`
5. `mutmut run ...`
6. `mutmut results`

Capturile care trebuie refacute pentru starea curenta a proiectului:

1. `01_pytest_100_passed.png`
2. `02_coverage_run_100_passed.png`
3. `03_coverage_report_100_percent.png`
4. `04_coverage_html.png`
5. `05_mutmut.png`
6. `06_mutmut_results.png`
7. `07_pytest_ai_70_passed.png`

Pune capturile noi in folderul:

```text
screenshots/
```

## 14. [DONE] Finalizeaza README si PowerPoint

Ordine recomandata:

1. pastreaza documentatia completa in `README.md`;
2. transforma `PREZENTARE_TSS.md` in PowerPoint de 10 slide-uri;
3. adauga capturile noi;
4. adauga diagramele `cfg_diagrama.drawio.png` si `cause_effect_graph.png`;
5. sterge orice urma din metodele vechi sau din raportul separat.

## 15. Ultima verificare inainte de predare

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
cod -> teste -> coverage -> mutmut -> cosmic ray -> README -> raport -> prezentare -> capturi -> verificare finala
```
