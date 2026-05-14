# TSS T1 - Testare unitara in Python

Proiect realizat pentru tema **T1 - Testare unitara in Python** la materia
Testarea Sistemelor Software.

Proiectul foloseste `unittest`, `pytest`, `coverage.py`, `mutmut` si, ca
analiza suplimentara, `Cosmic Ray` pentru testarea unei clase Python. Domeniul
ales este o clasa de fitness, iar functionalitatea principala testata este
metoda:

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

## Diagrame

Proiectul include doua diagrame generate cu tool-uri dedicate:

- `cfg_diagrama.drawio.png` - diagrama CFG pentru metoda
  `evaluate_client_package`;
- `cause_effect_graph.png` - graful cauza-efect pentru regulile de business
  ale metodei.

Diagrama CFG descrie validarea parametrilor, bucla prin `session_history`,
calculul costului si stabilirea statusului final.

## Rulare

Instalare dependente:

```bash
python -m pip install pytest coverage "mutmut<3" cosmic-ray
```

Rulare rapida a suitei:

```bash
python -m pytest -q
```

Configuratia `pytest.ini` limiteaza rularea implicita la suita principala de
99 de teste. Testele AI pot fi rulate separat:

```bash
python -m pytest -q teste_ai
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
mutatie se recomanda WSL. Rularea finala a fost facuta in distributia
`Ubuntu` din WSL.

Comanda folosita:

```bash
python -m mutmut run --paths-to-mutate fitness_class_booking.py \
  --tests-dir . \
  --runner "python -m pytest -q test_equivalence_partitioning.py test_boundary_value_analysis.py test_coverage.py test_independent_circuits.py test_mutation.py"
python -m mutmut results
```

Rezultat final:

```text
95/95 mutanti verificati
Killed: 80
Timeout: 0
Suspicious: 15
Survived: 0
Skipped: 0
```

Categoria `Suspicious` inseamna ca testele au rulat mai lent pentru acei
mutanti, dar nu suficient de lent pentru a fi incadrati la `Timeout`. Mutmut nu
a raportat mutanti in categoria `Survived`.

## Cosmic Ray

Cosmic Ray a fost folosit ca analiza suplimentara de mutation testing.
Artefactele relevante sunt pastrate in folderul `cosmic_ray/`; copia completa
a proiectului nu este necesara.

Rezultat Cosmic Ray:

```text
Mutanti generati/finalizati: 166
Mutanti supravietuitori: 9
Rata supravietuire: 5.42%
Scor aproximativ omorare mutanti: 94.58%
```

Mutantii supravietuitori sunt documentati in
`cosmic_ray/cosmic-ray-survivors.txt`. O parte dintre acestia sunt probabil
echivalenti sau foarte apropiati de comportamentul original, de exemplu
comparatii mutate in variante care nu schimba rezultatul pentru domeniul valid
al metodei.

## Capturi De Ecran

Capturile finale sunt in folderul `screenshots/`:

| Fisier | Continut |
| --- | --- |
| `01_pytest_99_passed.png` | rulare `python -m pytest -q` cu `99 passed` |
| `02_coverage_run_99_passed.png` | rulare coverage cu `99 passed` |
| `03_coverage_report_100_percent.png` | raport coverage cu 100% pe `fitness_class_booking.py` |
| `04_coverage_html_generated.png` | generarea raportului HTML coverage |
| `05_mutmut_run.png` | sumar mutmut: 95 mutanti, 80 killed, 15 suspicious, 0 survived |
| `06_mutmut_results.png` | lista mutantilor `Suspicious` raportati de mutmut |

## Materiale Pentru Predare

- `RAPORT_TSS.md` - raport scris pentru proiect;
- `PREZENTARE_TSS.md` - schelet de prezentare;
- `cfg_diagrama.drawio.png` - diagrama CFG;
- `cause_effect_graph.png` - graful cauza-efect;
- `cosmic_ray/` - artefactele Cosmic Ray;
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
|-- cfg_diagrama.drawio.png
|-- cause_effect_graph.png
|-- cosmic_ray/
|-- RAPORT_TSS.md
|-- PREZENTARE_TSS.md
|-- logs/
|-- screenshots/
|-- run_coverage.sh
`-- README.md
```
