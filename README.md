# T1 – Testare Unitară Python: `FitnessClassBooking`

**Materia:** Testarea Sistemelor Software (TSS)  
**Tema:** T1 – Testare unitară în Python  
**Framework:** `unittest` + `pytest 9.0.3` + `coverage 7.13.5` + `mutmut 2.5.1`  
**Python:** 3.13.3

---

## 1. Descrierea clasei

`FitnessClassBooking` gestionează rezervările pentru o ședință de fitness.
Suportă locuri confirmate, o listă de așteptare de maximum 5 persoane și
anulări cu promovare automată din waitlist.

| Metodă | Descriere |
|--------|-----------|
| `__init__(class_name, instructor, max_spots, price_per_session)` | Inițializează sesiunea; validează toți parametrii |
| `book_spot(client_name) → str` | Rezervă un loc: `"confirmed"` / `"waitlist"` / `"rejected"` |
| `cancel_booking(client_name) → bool` | Anulează rezervare; promovează automat din waitlist |
| `calculate_cost(sessions, has_membership) → float` | Calculează costul unei ședințe din abonament cu reduceri aditiv (membership 20% + volum 10%) |

**Tipuri de clase valide:** `"dance"`, `"pilates"`, `"yoga"`, `"zumba"`  
**Capacitate:** 1–30 locuri confirmate + max 5 pe waitlist  
**Validări `max_spots`:** trebuie să fie `int` pur (nu `float`, nu `bool`); `True` și `False` sunt respinse explicit prin verificarea `isinstance(max_spots, bool)`

### Fragmente de cod relevante

#### 1) Validarea din `__init__`

```python
if class_name not in self.VALID_CLASSES:
    raise ValueError(...)
if not isinstance(instructor, str) or not instructor or not instructor.strip():
    raise ValueError(...)
if isinstance(max_spots, bool) or not isinstance(max_spots, int) or max_spots < 1 or max_spots > 30:
    raise ValueError(...)
if not isinstance(price_per_session, (int, float)) or price_per_session <= 0:
    raise ValueError(...)
```

Acesta este cel mai important bloc de validare: de aici vin mai multe clase de
echivalență, valorile de frontieră și cele 4 decizii din CFG-ul pentru
`__init__`. Verificarea `isinstance(max_spots, bool)` există ca să respingă
explicit `True` și `False`, chiar dacă `bool` este subclasă de `int`.

#### 2) Fluxul de rezervare din `book_spot`

```python
if self.booked_spots < self.max_spots:
    self._confirmed.append(client)
    self.booked_spots += 1
    return "confirmed"
elif len(self.waitlist) < self.MAX_WAITLIST_SIZE:
    self.waitlist.append(client)
    return "waitlist"
else:
    return "rejected"
```

Acest fragment arată clar cele 3 rezultate posibile: loc confirmat, mutare pe
waitlist sau refuz. E foarte util de pus în raport fiindcă se vede imediat
tranziția între ramuri și limita de 5 persoane din waitlist.

#### 3) Calculul costului în `calculate_cost`

```python
cost = sessions * self.price_per_session

discount = 0.0
if has_membership:
    discount += 0.20
if sessions >= 10:
    discount += 0.10

return round(cost * (1 - discount), 2)
```

Aici se vede logica de business: reducerile sunt aditive, nu se aplică pe rând
una peste alta, iar rezultatul este rotunjit la două zecimale. Acesta este
exact locul vizat și de testele de mutation testing.

#### 4) Un test relevant de boundary value analysis

```python
def test_init_price_just_above_zero_is_valid(self) -> None:
    b = FitnessClassBooking("yoga", "Instructor", 5, 0.01)
    self.assertAlmostEqual(b.price_per_session, 0.01)
```

Acest test arată cum verifici frontiera pentru `price_per_session > 0`: `0.0`
trebuie respins, iar `0.01` trebuie acceptat. Este și testul care omoară
mutantul `M22`.

---

## 2. Tabelul claselor de echivalență

### `__init__`

| Class ID | Descriere | Input reprezentativ | Output așteptat |
|----------|-----------|---------------------|-----------------|
| EC01 | class_name valid | `"yoga"` | obiect creat |
| EC02 | class_name invalid | `"crossfit"` | `ValueError` |
| EC03 | instructor non-empty | `"Ana Pop"` | obiect creat |
| EC04 | instructor gol | `""` | `ValueError` |
| EC05 | instructor whitespace-only | `"   "` | `ValueError` |
| EC06 | max_spots în [1, 30] | `10` | obiect creat |
| EC07 | max_spots sub domeniu | `0` | `ValueError` |
| EC08 | max_spots peste domeniu | `31` | `ValueError` |
| EC09 | max_spots float | `1.0` | `ValueError` |
| EC10 | max_spots bool False (prins de verificarea bool) | `False` | `ValueError` |
| EC11 | price > 0 | `15.0` | obiect creat |
| EC12 | price ≤ 0 | `0.0` | `ValueError` |
| EC26 | instructor tip invalid (int) | `123` | `ValueError` |
| EC27 | price_per_session tip invalid (str) | `"10"` | `ValueError` |
| EC28 | max_spots bool True (subclasă int, dar bool) | `True` | `ValueError` |

### `book_spot`

| Class ID | Descriere | Input reprezentativ | Output așteptat |
|----------|-----------|---------------------|-----------------|
| EC13 | client valid, loc liber | `"Alice"`, 0 din 5 ocupate | `"confirmed"` |
| EC14 | client_name gol | `""` | `ValueError` |
| EC15 | clasa plină, waitlist disponibil | `"Bob"`, 5/5 ocupate, 0 pe WL | `"waitlist"` |
| EC16 | clasa plină, waitlist plin | `"Charlie"`, 5/5 + 5 WL | `"rejected"` |
| EC29 | client_name tip invalid (int) | `123` | `ValueError` |

### `cancel_booking`

| Class ID | Descriere | Input reprezentativ | Output așteptat |
|----------|-----------|---------------------|-----------------|
| EC17 | client confirmat | `"Alice"` (în confirmed) | `True` |
| EC18 | client pe waitlist | `"Bob"` (în waitlist) | `True` |
| EC19 | client negăsit | `"Nobody"` | `False` |

### `calculate_cost`

| Class ID | Descriere | Input reprezentativ | Output așteptat |
|----------|-----------|---------------------|-----------------|
| EC20 | sessions valid, fără membership | `sessions=5, False` | `50.0` |
| EC21 | sessions = 0 (sub domeniu) | `sessions=0` | `ValueError` |
| EC22 | sessions > 20 (peste domeniu) | `sessions=21` | `ValueError` |
| EC23 | cu membership, sessions < 10 | `sessions=5, True` | `40.0` |
| EC24 | fără membership, sessions ≥ 10 | `sessions=10, False` | `90.0` |
| EC25 | cu membership, sessions ≥ 10 | `sessions=10, True` | `70.0` |
| EC30 | sessions tip invalid (str) | `"5"` | `ValueError` |

---

## 3. Tabelul valorilor de frontieră

| Metodă | Parametru / Frontiera | Sub frontieră | La frontieră | Peste frontieră |
|--------|-----------------------|---------------|--------------|-----------------|
| `__init__` | max_spots ≥ 1 | `0` → ValueError | `1` → valid | `2` → valid |
| `__init__` | max_spots ≤ 30 | `29` → valid | `30` → valid | `31` → ValueError |
| `__init__` | price_per_session > 0 | `-0.01` → ValueError | `0.0` → ValueError | `0.01` → valid |
| `book_spot` | booked < max_spots | max−1 booked → `"confirmed"` | max booked → `"waitlist"` | — |
| `book_spot` | len(waitlist) < 5 | 4 pe WL → `"waitlist"` | 5 pe WL → `"rejected"` | — |
| `calculate_cost` | sessions ≥ 1 | `0` → ValueError | `1` → valid | `2` → valid |
| `calculate_cost` | sessions ≤ 20 | `19` → valid | `20` → valid | `21` → ValueError |
| `calculate_cost` | sessions ≥ 10 (discount) | `9` → fără discount | `10` → cu discount | `11` → cu discount |

---

## 4. Graf de flux de control (CFG) și complexitate ciclomatică

### `__init__` – V(G) = 5

```
N1 [intrare]
 │
 ▼
N2: if class_name not in VALID_CLASSES
 │ True             │ False
 ▼                  ▼
N3: raise      N4: if not isinstance(instructor, str)
ValueError           or not instructor or not instructor.strip()
 │              │ True             │ False
 │              ▼                  ▼
 │         N5: raise          N6: if isinstance(max_spots, bool)
 │         ValueError              or not isinstance(max_spots, int)
 │                                 or max_spots < 1 or > 30
 │              │               │ True        │ False
 │              │               ▼             ▼
 │              │         N7: raise      N8: if price_per_session <= 0
 │              │         ValueError     │ True        │ False
 │              │              │         ▼             ▼
 │              │              │    N9: raise     N10: assignments
 │              │              │    ValueError
 └──────────────┴──────────────┴──────────────────────┘
                                                       │
                                                    [Nexit]
```

**V(G) = 4 + 1 = 5** | Circuite: PATH_INIT_1..5

### `book_spot` – V(G) = 4

```
N1 → N2: if not isinstance(client_name, str) or not client_name or not client_name.strip()
          │ True                  │ False
          ▼                       ▼
     N3: raise ValueError    N4: client = strip()
                                  │
                             N5: if booked_spots < max_spots
                              │ True          │ False
                              ▼               ▼
                       N6: "confirmed"   N7: if len(waitlist) < 5
                                          │ True        │ False
                                          ▼             ▼
                                    N8: "waitlist"  N9: "rejected"
```

**V(G) = 3 + 1 = 4** | Circuite: PATH_BS_1..4

### `cancel_booking` – V(G) = 4

```
N1: name = strip(client_name)  →  N2: if name in _confirmed
                                   │ True                   │ False
                                   ▼                        ▼
                          N3: remove; booked -= 1     N6: elif name in waitlist
                                   │                   │ True       │ False
                              N4: if waitlist          ▼            ▼
                               │ True    │ False  N7: remove   N8: return False
                               ▼         │        return True
                          N5: promote    │
                               └────┬───┘
                                    ▼
                                return True
```

**V(G) = 3 + 1 = 4** | Circuite: PATH_CB_1..4

### `calculate_cost` – V(G) = 4

```
N1 [intrare]
 │
 ▼
N2: if sessions < 1 or sessions > 20   ← D_guard
 │ True             │ False
 ▼                  ▼
N3: raise      N4: cost = sessions × price
ValueError          │
 │                  ▼
 │             N5: if has_membership   ← D7
 │              │ True    │ False
 │              ▼         │
 │         N6: discount   │
 │             += 0.20    │
 │              └────┬────┘
 │                   ▼
 │             N7: if sessions >= 10   ← D8
 │              │ True    │ False
 │              ▼         │
 │         N8: discount   │
 │             += 0.10    │
 │              └────┬────┘
 │                   ▼
 │             N9: return round(cost × (1−discount), 2)
 │                   │
 └───────────────────┘
                     │
                  [Nexit]
```

**V(G) = 3 + 1 = 4** | Circuite: PATH_CC_1..4

| Circuit | Cale | Condiții | Rezultat |
|---------|------|----------|---------|
| PATH_CC_1 | N1→N2(T)→N3→Nexit | D_guard=T (sessions=0) | ValueError |
| PATH_CC_2 | N1→N2(F)→N4→N5(F)→N7(F)→N9→Nexit | D_guard=F, D7=F, D8=F | cost de bază |
| PATH_CC_3 | N1→N2(F)→N4→N5(T)→N6→N7(F)→N9→Nexit | D_guard=F, D7=T, D8=F | −20% membership |
| PATH_CC_4 | N1→N2(F)→N4→N5(F)→N7(T)→N8→N9→Nexit | D_guard=F, D7=F, D8=T | −10% volum |

---

## 5. Acoperire la nivel de condiție (condition coverage)

### Condiție compusă `__init__` – max_spots

`isinstance(max_spots, bool) OR not isinstance(max_spots, int) OR max_spots < 1 OR max_spots > 30`

| Condiție atomică | True | False |
|------------------|------|-------|
| `isinstance(max_spots, bool)` | `True` (bool) → ValueError | `5` (int) → continuă |
| `not isinstance(max_spots, int)` | `1.0` (float) → ValueError | `5` (int) → continuă |
| `max_spots < 1` | `0` → ValueError | `5` → continuă |
| `max_spots > 30` | `31` → ValueError | `5` → valid |

### Condiție compusă `book_spot` – validare client_name

`not isinstance(client_name, str) OR not client_name OR not client_name.strip()`

| Condiție atomică | True | False |
|------------------|------|-------|
| `not isinstance(client_name, str)` | `123` (int) → ValueError | `"Alice"` → C1a evaluată |
| `not client_name` | `""` → ValueError (short-circuit) | `"Alice"` → C1b evaluată |
| `not client_name.strip()` | `"   "` → ValueError | `"Bob"` → continuă |

### Combinații `calculate_cost` (D7 × D8)

| has_membership | sessions ≥ 10 | Rezultat |
|----------------|---------------|---------|
| False | False | cost de bază (discount 0%) |
| True | False | −20% membership |
| False | True | −10% volum |
| True | True | −30% aditiv (20% + 10% din prețul de bază) |

---

### Diagrame CFG (PNG)

Imaginile de mai jos sunt exporturi din Draw.io / diagrams.net [4] și reprezintă
varianta grafică finală a CFG-urilor.

#### `__init__`
<p align="center">
  <img src="init_cfg.drawio.png" alt="CFG __init__" width="920">
</p>

#### `book_spot`
<p align="center">
  <img src="book_spot_cfg.drawio.png" alt="CFG book_spot" width="920">
</p>

#### `cancel_booking`
<p align="center">
  <img src="cancel_booking_cfg.drawio.png" alt="CFG cancel_booking" width="920">
</p>

#### `calculate_cost`
<p align="center">
  <img src="calculate_cost_cfg.drawio.png" alt="CFG calculate_cost" width="920">
</p>

---

## 6. Raport mutmut – analiză reală

**Comandă:** `mutmut run --paths-to-mutate fitness_class_booking.py --tests-dir . --runner "python -m pytest"`  
**Mediu:** WSL Ubuntu 24.04.1 LTS / Python 3.12.3 / mutmut 2.5.1

| Categorie | Număr |
|-----------|-------|
| Total mutanți generați | 86 |
| Uciși | 65 |
| Suspicioși | 13 |
| Supraviețuitori | 8 |
| Scor inițial | 65/86 ≈ 75.6% |

### Rezumat mutmut

`mutmut results` raportează acum:

- `Suspicious (13)`: `M3, M5, M8, M10-M12, M15, M22, M29, M34-M36, M74`
- `Survived (8)`: `M9, M14, M21, M26, M39, M49, M70, M75`

### Clasificarea mutanților supraviețuitori (8)

| Grup | Mutanți | Tip | Acțiune |
|------|---------|-----|---------|
| Mutanți de text / mesaj | M9, M14, M21, M39, M70 | Modifică doar mesajele `ValueError` sau textul explicativ | Documentați, nu omorâți |
| Quasi-echivalent | M26, M49 | Diferență observabilă doar pe inputuri foarte specifice | Documentat |
| Echivalent algebric | M75 | `discount += 0.20` vs `discount = 0.20` în contextul actual | Documentat |

**Scor final (mutanți comportamentali neechivalenți): 3/3 = 100%**

### Tabel detaliat mutanți comportamentali

| Mutant | Original | Modificare mutmut | Efect bug | Test care îl omoară |
|--------|----------|--------------------|-----------|---------------------|
| M12 | `not instructor or not instructor.strip()` | `or` → `and` | Instructor `"   "` trece validarea | `test_kill_M12_whitespace_only_instructor_must_raise_value_error` |
| M22 | `price_per_session <= 0` | `<= 0` → `<= 1` | Prețuri valide ≤ 1.0 aruncă ValueError | `test_init_price_just_above_zero_is_valid` (BVA) |
| M76 | `round(cost, 2)` | `2` → `3` | Costul returnat cu 3 zecimale | `test_kill_M76_cost_rounds_to_two_decimal_places` |

---

## 7. Configurație hardware și software

### Laptopuri folosite

| Model | Procesor | Memorie | Stocare |
|-------|----------|---------|---------|
| HP Victus 16 | Intel Core i7-12700H | 16 GB RAM DDR5 4800 MHz (SK hynix) | 512 GB SSD (Samsung) |
| HP Laptop 15 | Intel Core i7-1165G7 | 16 GB RAM DDR4 2933 MHz | 512 GB SSD (Micron OEM) |

### OS și mediu de lucru

| Componentă | Versiune / detalii |
|-----------|--------------------|
| Windows | Windows 11 25H2, build 26200.8246 |
| WSL | 2.6.3.0 |
| Kernel WSL | 6.6.87.2-microsoft-standard-WSL2 |
| Distro Linux | Ubuntu 24.04.1 LTS (Noble Numbat) |
| VS Code | 1.116.0 |
| Python în WSL | 3.12.3 |
| pip în WSL | 24.0 |
| pytest în WSL | 9.0.2 |
| coverage.py în WSL | 7.13.5 |
| mutmut în WSL | 2.5.1 |

Versiunile de mai sus au fost preluate local din PowerShell și din venv-ul WSL
`/home/alex/tss_venv`.

Nu a fost folosită o mașină virtuală clasică; mediul Linux a fost accesat prin
WSL2.

## 8. Cum se rulează

Comenzile de mai jos urmează documentația oficială pentru pytest [1],
coverage.py [2] și mutmut [3].

### Teste (Windows / WSL / Linux - pytest)

```bash
# Instalare dependențe
pip install pytest coverage

# Rulare toate testele
python -m pytest test_*.py -v

# Coverage instrucțiuni + ramuri
python -m coverage run --branch -m pytest test_*.py
python -m coverage report -m --include="fitness_class_booking.py"
python -m coverage html --include="fitness_class_booking.py"
# Deschide htmlcov/index.html în browser
```

### Analiză mutanți (WSL + mutmut)

```bash
# Instalare mutmut 2.x în WSL (ca root sau cu --break-system-packages)
pip install --break-system-packages --ignore-installed "mutmut<3"

# Creare symlink python dacă lipsește
ln -sf /usr/bin/python3 /usr/local/bin/python

# Navigare la proiect
cd <path_catre_TSS_Proiect>  # ex: /mnt/c/Users/alexn/Documents/GitHub/TSS_Proiect

# Rulare analiză mutanți
mutmut run --paths-to-mutate fitness_class_booking.py \
           --tests-dir . \
           --runner "python -m pytest"

# Vizualizare rezultate
mutmut results
mutmut show <ID>
```

### Capturi recomandate

1. Teste unitare

```bash
python -m pytest test_*.py -v
```

2. Coverage in consola

```bash
python -m coverage run --branch -m pytest test_*.py
python -m coverage report -m --include="fitness_class_booking.py"
```

3. Coverage HTML

```bash
python -m coverage html --include="fitness_class_booking.py"
```

4. Mutation testing

```bash
mutmut run --paths-to-mutate fitness_class_booking.py --tests-dir . --runner "python -m pytest"
mutmut results
mutmut show <ID>
```

### Capturi de ecran

Mai jos sunt capturile reale, in ordinea comenzilor rulate.

**1-2. `python -m pytest test_*.py -v`**

<p align="center">
  <img src="screenshots/01_pytest_verbose_part1.png" alt="pytest verbose part 1" width="1000">
</p>

<p align="center">
  <img src="screenshots/02_pytest_verbose_part2.png" alt="pytest verbose part 2" width="1000">
</p>

**3. `python -m coverage run --branch -m pytest test_*.py`**

<p align="center">
  <img src="screenshots/03_coverage_run_branch.png" alt="coverage run branch" width="1000">
</p>

**4. `python -m coverage report -m --include="fitness_class_booking.py"`**

<p align="center">
  <img src="screenshots/04_coverage_report_fitness_class_booking.png" alt="coverage report" width="1000">
</p>

**5. `mutmut run --paths-to-mutate fitness_class_booking.py --tests-dir . --runner "python -m pytest"` + `mutmut results`**

<p align="center">
  <img src="screenshots/05_mutmut_run_and_results.png" alt="mutmut run and results" width="1000">
</p>

**6. Mutanți supraviețuitori, partea 1**

<p align="center">
  <img src="screenshots/06_mutmut_survivors_part1.png" alt="mutmut survivors part 1" width="1000">
</p>

**7. Mutanți supraviețuitori, partea 2**

<p align="center">
  <img src="screenshots/07_mutmut_survivors_part2.png" alt="mutmut survivors part 2" width="1000">
</p>

**8. Rulare fragment Python din WSL**

<p align="center">
  <img src="screenshots/08_wsl_python_snippet_output.png" alt="wsl python snippet output" width="1000">
</p>

---

## 9. Structura proiectului

```
TSS_Proiect/
├── fitness_class_booking.py          # Clasa de testat (4 metode: __init__ + 3 instance methods)
├── test_equivalence_partitioning.py  # Strategia 1: clase de echivalență (EC01–EC30)
├── test_boundary_value_analysis.py   # Strategia 2: valori de frontieră (BVA01–BVA23)
├── test_coverage.py                  # Strategiile 3–5: instrucțiune / decizie / condiție
├── test_independent_circuits.py      # Strategia 6: basis path testing (McCabe)
├── test_mutation.py                  # Strategiile 7–8: raport mutmut + teste suplimentare
├── run_coverage.sh                   # Script de rulare complet (bash/WSL)
└── README.md                         # Acest fișier
```

**Total teste: 127 | Toate trec (0 eșuate)**

---

## 10. Anexe - documentație oficială

### Linkuri oficiale

- [pytest - official documentation](https://docs.pytest.org/)
- [coverage.py - official documentation](https://coverage.readthedocs.io/)
- [mutmut - official documentation](https://mutmut.readthedocs.io/en/)
- [draw.io / diagrams.net - official website](https://www.diagrams.net/)
- [unittest - Python standard library documentation](https://docs.python.org/3/library/unittest.html)
- [VS Code - documentation](https://code.visualstudio.com/docs)
- [Windows Subsystem for Linux - documentation](https://learn.microsoft.com/windows/wsl/)

### Referințe

[1]: https://docs.pytest.org/
[2]: https://coverage.readthedocs.io/
[3]: https://mutmut.readthedocs.io/en/
[4]: https://www.diagrams.net/

*Proiect universitar TSS – T1 Testare unitară Python | `unittest` + `pytest` + `coverage` + `mutmut`*
