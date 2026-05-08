# TSS T1 - Testare unitara in Python

Proiectul foloseste `unittest` si `pytest` pentru testarea unei clase Python.
Tema aleasa este o clasa de fitness, iar functionalitatea testata este o
singura metoda: `evaluate_client_package`.

## Clasa testata

Fisier principal: `fitness_class_booking.py`

```python
class FitnessClassBooking:
    def evaluate_client_package(
        self,
        session_history: list[str],
        package_sessions: int,
        has_membership: bool,
    ) -> dict:
        ...
```

Metoda evalueaza pachetul de sedinte al unui client.

Statusuri acceptate in `session_history`:

- `attended` - clientul a participat; sedinta se consuma
- `no_show` - clientul nu a venit si nu a anuntat; sedinta se consuma
- `cancelled` - clientul a anulat la timp; sedinta nu se consuma

Metoda returneaza numarul de sedinte participate, numarul de `no_show`,
numarul de anulari, sedintele consumate, sedintele ramase, costul total si
statusul pachetului.

Statusuri posibile:

- `active` - clientul mai are sedinte disponibile
- `completed` - clientul a consumat toate sedintele, dar are cel putin un `no_show`
- `completed_clean` - clientul a consumat toate sedintele fara niciun `no_show`

## Cerinta profesoarei

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

## Strategii de testare

Proiectul pastreaza strategiile cerute pentru T1, aplicate pe aceeasi metoda.

| Fisier | Strategie |
| --- | --- |
| `test_equivalence_partitioning.py` | partitionare in clase de echivalenta |
| `test_boundary_value_analysis.py` | analiza valorilor de frontiera |
| `test_coverage.py` | acoperire la nivel de instructiune, decizie si conditie |
| `test_independent_circuits.py` | circuite independente / basis path testing |
| `test_mutation.py` | teste suplimentare orientate pe mutanti neechivalenti |

Suita activa are 66 de teste.

## Diagrama CFG

Diagrama de flux de control pentru metoda testata este disponibila in doua
formate:

- `evaluate_client_package_cfg.drawio.svg`
- `evaluate_client_package_cfg.drawio.png`

Diagramele vechi pentru `book_spot`, `cancel_booking`, `calculate_cost` si
`__init__` au fost eliminate deoarece nu mai corespundeau versiunii curente.

## Rulare

```bash
python -m pytest -q
```

Coverage:

```bash
python -m coverage run --branch -m pytest
python -m coverage report -m --include="fitness_class_booking.py"
```

Mutmut:

```bash
mutmut run --paths-to-mutate fitness_class_booking.py \
           --tests-dir . \
           --runner "python -m pytest -q"
mutmut results
```

Ultima rulare locala in WSL:

- mutanti supravietuitori: 0
- mutanti suspiciosi: 7

Mutantii suspiciosi observati sunt schimbari care au produs teste lente in
mutmut, dar nu au ramas in categoria `Survived`.

## Materiale pentru predare

- `RAPORT_TSS.md` - raport scris, actualizat pentru noua metoda;
- `PREZENTARE_TSS.md` - schelet de prezentare tip slide-uri;
- `logs/` - output-uri reale pentru pytest, coverage si mutmut;
- `screenshots/README.md` - explica de ce capturile vechi au fost eliminate.

Fisierele vechi `raport_ai.docx` si `TSS_T1_FitnessClassBooking.pptx` nu au
fost editate automat. Continutul nou pentru ele este in fisierele Markdown de
mai sus.

Script complet:

```bash
bash run_coverage.sh
```

## Structura proiectului

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
|-- run_coverage.sh
|-- README.md
`-- screenshots/
```
