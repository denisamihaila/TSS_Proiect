# TSS T1 - Testare unitara in Python

Proiect realizat pentru tema **T1 - Testare unitara in Python** la materia
Testarea Sistemelor Software.

Proiectul foloseste `unittest`, `pytest`, `coverage.py` si `mutmut` pentru
testarea unei clase Python. Domeniul ales este o clasa de fitness, iar
functionalitatea principala testata este metoda:

```python
evaluate_client_package(session_history, package_sessions, has_membership)
```

## Clasa Testata

Fisier principal: `fitness_class_booking.py`

```python
class FitnessClassBooking:
    def __init__(
        self,
        class_name: str,
        instructor: str,
        price_per_session: float,
    ) -> None:
        ...

    def evaluate_client_package(
        self,
        session_history: list[str],
        package_sessions: int,
        has_membership: bool,
    ) -> dict:
        ...
```

Constructorul valideaza:

- `class_name`: una dintre valorile `dance`, `pilates`, `yoga`, `zumba`;
- `instructor`: sir nevid dupa `strip()`;
- `price_per_session`: numar pozitiv, cu `bool` respins explicit.

Metoda `evaluate_client_package` evalueaza pachetul de sedinte al unui client.

Statusuri acceptate in `session_history`:

- `attended` - clientul a participat; sedinta se consuma;
- `no_show` - clientul nu a venit si nu a anuntat; sedinta se consuma;
- `cancelled` - clientul a anulat la timp; sedinta nu se consuma.

Metoda returneaza:

- numarul de sedinte participate;
- numarul de `no_show`;
- numarul de anulari;
- sedintele consumate;
- sedintele ramase;
- costul total al pachetului;
- statusul final al pachetului.

Statusuri posibile:

- `active` - clientul mai are sedinte disponibile;
- `completed_successfully` - clientul a consumat toate sedintele fara
  niciun `no_show`;
- `completed_with_absences` - clientul a consumat toate sedintele, dar are
  cel putin un `no_show`.

## Cerinta Structurala

Metoda respecta cerinta pentru testarea unitara:

| Cerinta | Unde apare |
| --- | --- |
| minim 3 parametri | `session_history`, `package_sessions`, `has_membership` |
| instructiune repetitiva | `for session_status in session_history` |
| `if` cu `else` | `if session_status == "attended": ... else: ...` |
| `if` fara `else` | `if has_membership: ...` |
| conditie simpla | `if has_membership` |
| conditie compusa | `if remaining_sessions == 0 and no_show == 0` |

## Exemplu

```python
booking = FitnessClassBooking("yoga", "Ana Pop", 50)

result = booking.evaluate_client_package(
    ["attended", "attended", "cancelled", "no_show"],
    5,
    True,
)
```

Rezultat:

```python
{
    "attended": 2,
    "no_show": 1,
    "cancelled": 1,
    "used_sessions": 3,
    "remaining_sessions": 2,
    "total_cost": 200.0,
    "status": "active",
}
```

## Strategii De Testare

Toate strategiile cerute pentru T1 sunt aplicate pe aceeasi functionalitate.

| Fisier | Strategie | Nr. teste |
| --- | --- | ---: |
| `test_equivalence_partitioning.py` | partitionare in clase de echivalenta | 22 |
| `test_boundary_value_analysis.py` | analiza valorilor de frontiera | 16 |
| `test_coverage.py` | acoperire la nivel de instructiune, decizie si conditie | 40 |
| `test_independent_circuits.py` | circuite independente / basis path testing | 10 |
| `test_mutation.py` | teste suplimentare orientate pe mutanti neechivalenti | 11 |

Suita activa are **99 de teste**.

## Rezultate Verificate

Ultima verificare locala pe versiunea curenta:

```text
99 passed
```

Coverage pentru fisierul principal:

```text
Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
fitness_class_booking.py      43      0     26      0   100%
----------------------------------------------------------------------
TOTAL                         43      0     26      0   100%
```

## Diagrama CFG

Diagrama de flux de control pentru metoda testata este disponibila in doua
formate:

- `evaluate_client_package_cfg.drawio.svg`
- `evaluate_client_package_cfg.drawio.png`

Diagrama descrie fluxul metodei `evaluate_client_package`, inclusiv validarea
parametrilor, bucla prin `session_history`, calculul costului si stabilirea
statusului final.

## Rulare

Instalare dependente:

```bash
python -m pip install pytest coverage "mutmut<3"
```

Rulare rapida a suitei:

```bash
python -m pytest -q
```

Rulare doar fisierele folosite in proiect:

```bash
python -m pytest -q \
  test_equivalence_partitioning.py \
  test_boundary_value_analysis.py \
  test_coverage.py \
  test_independent_circuits.py \
  test_mutation.py
```

Coverage:

```bash
python -m coverage run --branch -m pytest -q \
  test_equivalence_partitioning.py \
  test_boundary_value_analysis.py \
  test_coverage.py \
  test_independent_circuits.py \
  test_mutation.py
python -m coverage report -m --include="fitness_class_booking.py"
python -m coverage html --include="fitness_class_booking.py"
```

Script complet:

```bash
bash run_coverage.sh
```

Scriptul salveaza output-urile in:

- `logs/pytest_output.txt`;
- `logs/coverage_report.txt`;
- `logs/mutmut_results.txt`.

Variabile utile pentru script:

```bash
RUN_MUTMUT=0 bash run_coverage.sh     # fara mutmut
RUN_MUTMUT=1 bash run_coverage.sh     # mutmut obligatoriu
RUN_MUTMUT=auto bash run_coverage.sh  # implicit
```

## Mutmut

`mutmut` nu ruleaza nativ pe Windows in mediul curent; pentru analiza de
mutatie se recomanda WSL.

Comanda folosita:

```bash
python -m mutmut run --paths-to-mutate fitness_class_booking.py \
  --tests-dir . \
  --runner "python -m pytest -q test_equivalence_partitioning.py test_boundary_value_analysis.py test_coverage.py test_independent_circuits.py test_mutation.py"
python -m mutmut results
```

Logul `logs/mutmut_results.txt` trebuie regenerat din WSL dupa stabilirea
versiunii finale a testelor.

## Materiale Pentru Predare

- `RAPORT_TSS.md` - raport scris pentru proiect;
- `PREZENTARE_TSS.md` - schelet de prezentare;
- `evaluate_client_package_cfg.drawio.svg` si `.png` - diagrama CFG;
- `logs/` - output-uri pentru pytest, coverage si mutmut;
- `screenshots/` - loc pentru capturile finale ale comenzilor.

Fisierele vechi `raport_ai.docx` si `TSS_T1_FitnessClassBooking.pptx` pot
contine informatii dintr-o varianta anterioara a proiectului si trebuie
actualizate manual inainte de predare.

## Structura Proiectului

```text
TSS_Proiect/
|-- fitness_class_booking.py
|-- test_equivalence_partitioning.py
|-- test_boundary_value_analysis.py
|-- test_coverage.py
|-- test_independent_circuits.py
|-- test_mutation.py
|-- evaluate_client_package_cfg.drawio.svg
|-- evaluate_client_package_cfg.drawio.png
|-- RAPORT_TSS.md
|-- PREZENTARE_TSS.md
|-- logs/
|-- screenshots/
|-- run_coverage.sh
`-- README.md
```
