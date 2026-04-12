# T1 – Testare Unitară Python: `FitnessClassBooking`

**Materia:** Testarea Sistemelor Software (TSS)  
**Tema:** T1 – Testare unitară în Python  
**Framework:** `unittest` + `pytest` + `coverage` + `mutmut`  
**Python:** 3.10+

---

## 1. Descrierea clasei

`FitnessClassBooking` gestionează rezervările pentru o ședință de fitness.

| Metodă | Descriere |
|--------|-----------|
| `__init__(class_name, instructor, max_spots, price_per_session)` | Inițializează sesiunea; validează toți parametrii |
| `book_spot(client_name) → str` | Rezervă un loc: `"confirmed"` / `"waitlist"` / `"rejected"` |
| `cancel_booking(client_name) → bool` | Anulează rezervare; promovează automat din waitlist |
| `calculate_cost(sessions, has_membership) → float` | Calculează costul cu reduceri cumulative |
| `get_availability() → dict` | Returnează `{"free": X, "booked": Y, "waitlist": Z}` |

**Tipuri de clase valide:** `"dance"`, `"pilates"`, `"yoga"`, `"zumba"`  
**Capacitate:** 1–30 locuri confirmate + max 5 pe waitlist

---

## 2. Tabelul claselor de echivalență

### `__init__`

| Class ID | Descriere | Input reprezentativ | Output așteptat |
|----------|-----------|---------------------|-----------------|
| EC01 | class_name valid | `"yoga"` | obiect creat |
| EC02 | class_name invalid | `"crossfit"` | `ValueError` |
| EC03 | instructor non-empty | `"Ana Pop"` | obiect creat |
| EC04 | instructor gol | `""` | `ValueError` |
| EC05 | max_spots în [1,30] | `10` | obiect creat |
| EC06 | max_spots sub domeniu | `0` | `ValueError` |
| EC07 | max_spots peste domeniu | `31` | `ValueError` |
| EC08 | price > 0 | `15.0` | obiect creat |
| EC09 | price <= 0 | `0.0` | `ValueError` |

### `book_spot`

| Class ID | Descriere | Input reprezentativ | Output așteptat |
|----------|-----------|---------------------|-----------------|
| EC10 | client valid, loc liber | `"Alice"`, 0 din 5 ocupate | `"confirmed"` |
| EC11 | client_name gol | `""` | `ValueError` |
| EC12 | clasa plină, waitlist disponibil | `"Bob"`, 5/5 ocupate, 0 pe WL | `"waitlist"` |
| EC13 | clasa plină, waitlist plin | `"Charlie"`, 5/5 + 5 WL | `"rejected"` |

### `cancel_booking`

| Class ID | Descriere | Input reprezentativ | Output așteptat |
|----------|-----------|---------------------|-----------------|
| EC14 | client confirmat | `"Alice"` (în confirmed) | `True` |
| EC15 | client pe waitlist | `"Bob"` (în waitlist) | `True` |
| EC16 | client negăsit | `"Nobody"` | `False` |

### `calculate_cost`

| Class ID | Descriere | Input reprezentativ | Output așteptat |
|----------|-----------|---------------------|-----------------|
| EC17 | sessions valid, fără membership | `sessions=5, False` | `50.0` |
| EC18 | sessions = 0 | `sessions=0` | `ValueError` |
| EC19 | sessions > 20 | `sessions=21` | `ValueError` |
| EC20 | cu membership, sessions < 10 | `sessions=5, True` | `40.0` |
| EC21 | fără membership, sessions ≥ 10 | `sessions=10, False` | `90.0` |
| EC22 | cu membership, sessions ≥ 10 | `sessions=10, True` | `72.0` |

### `get_availability`

| Class ID | Descriere | Stare | Output așteptat |
|----------|-----------|-------|-----------------|
| EC23 | clasa goală | 0 rezervări | `{free:5, booked:0, waitlist:0}` |
| EC24 | parțial rezervată | 3 din 5 | `{free:2, booked:3, waitlist:0}` |
| EC25 | complet rezervată | 5 din 5 | `{free:0, booked:5, ...}` |

---

## 3. Tabelul valorilor de frontieră

| Metodă | Frontiera | Valoare sub | Valoare la | Valoare peste |
|--------|-----------|-------------|------------|---------------|
| `__init__` | max_spots ≥ 1 | `0` → ValueError | `1` → valid | `2` → valid |
| `__init__` | max_spots ≤ 30 | `29` → valid | `30` → valid | `31` → ValueError |
| `book_spot` | booked < max_spots | max-1 booked → "confirmed" | max booked → "waitlist" | — |
| `book_spot` | len(waitlist) < 5 | 4 pe WL → "waitlist" | 5 pe WL → "rejected" | — |
| `calculate_cost` | sessions ≥ 1 | `0` → ValueError | `1` → valid | `2` → valid |
| `calculate_cost` | sessions ≤ 20 | `19` → valid | `20` → valid | `21` → ValueError |
| `calculate_cost` | sessions ≥ 10 (discount) | `9` → fără discount | `10` → cu discount | `11` → cu discount |

---

## 4. Graf de flux de control (CFG)

### `book_spot` – V(G) = 4

```
N1 [intrare]
 │
 ▼
N2: if not client_name or not client_name.strip()
 │ True                     │ False
 ▼                           ▼
N3: raise ValueError       N4: client = strip()
                             │
                             ▼
                           N5: if booked_spots < max_spots
                            │ True          │ False
                            ▼               ▼
                    N6: return          N7: if len(waitlist) < 5
                    "confirmed"          │ True      │ False
                                         ▼           ▼
                                   N8: return   N9: return
                                   "waitlist"   "rejected"
```

**V(G) = nr_decizii + 1 = 3 + 1 = 4**  
Circuite: PATH_BS_1 (ValueError), PATH_BS_2 (confirmed), PATH_BS_3 (waitlist), PATH_BS_4 (rejected)

### `calculate_cost` – V(G) = 3

```
N1: cost = sessions × price
 │
 ▼
N2: if has_membership
 │ True      │ False
 ▼           │
N3: ×0.80    │
 │           │
 └─────┬─────┘
       ▼
     N4: if sessions >= 10
      │ True      │ False
      ▼           │
   N5: ×0.90      │
      │           │
      └─────┬─────┘
            ▼
          N6: return round(cost, 2)
```

**V(G) = nr_decizii + 1 = 2 + 1 = 3**  
Circuite: PATH_CC_1 (bază), PATH_CC_2 (membership), PATH_CC_3 (volum)

### `cancel_booking` – V(G) = 4

```
N1: name = strip(client_name)
 │
 ▼
N2: if name in _confirmed
 │ True                    │ False
 ▼                         ▼
N3: remove; booked -= 1  N6: elif name in waitlist
 │                         │ True       │ False
 ▼                         ▼            ▼
N4: if waitlist         N7: remove   N8: return False
 │ True    │ False      return True
 ▼         │
N5: promote│
 └────┬────┘
      ▼
  return True
```

**V(G) = 3 + 1 = 4**  
Circuite: PATH_CB_1 (confirmed, no WL), PATH_CB_2 (confirmed + promote), PATH_CB_3 (waitlist), PATH_CB_4 (not found)

---

## 5. Tabelul analizei mutanților

| Mutant ID | Original | Mutant | Locație | Echivalent? | Ucis de test |
|-----------|----------|--------|---------|-------------|--------------|
| M1 | `booked_spots < max_spots` | `booked_spots <= max_spots` | `book_spot` | **Nu** | `test_kill_M1_full_class_next_booking_must_be_waitlist` |
| M2 | `len(waitlist) < 5` | `len(waitlist) <= 5` | `book_spot` | **Nu** | `test_kill_M2_full_waitlist_next_booking_must_be_rejected` |
| M3 | `sessions >= 10` | `sessions > 10` | `calculate_cost` | **Nu** | `test_kill_M3_exactly_10_sessions_must_apply_volume_discount` |
| M4 | `cost *= 0.80` | `cost *= 0.90` | `calculate_cost` | **Nu** | `test_kill_M4_membership_discount_must_be_20_percent` |
| M5 | `booked_spots -= 1` | `booked_spots = booked_spots - 1` | `cancel_booking` | **Da** | — (echivalent) |
| M6 | `cost *= 0.90` | `cost = cost * 0.90` | `calculate_cost` | **Da** | — (echivalent) |

**Justificare echivalență M5, M6:** `+=`/`-=`/`*=` pe tipuri imutabile (`int`, `float`) produc
același rezultat ca operatorul explicit `= ... + / - / *`. Nicio secvență de apeluri nu poate
distinge comportamentul observabil al celor două variante.

---

## 6. Cum se rulează

### Windows (pytest + coverage)
```powershell
# Instalare
pip install pytest coverage

# Teste (toate fișierele)
python -m pytest test_*.py -v

# Coverage statement + branch
python -m coverage run --branch -m pytest test_*.py
python -m coverage report -m --include="fitness_class_booking.py"
python -m coverage html --include="fitness_class_booking.py"
# Deschide htmlcov/index.html
```

### WSL (mutmut)
```bash
# Creează și activează venv în WSL (necesar pentru mutmut<3)
python3 -m venv ~/tss_venv
source ~/tss_venv/bin/activate

# Instalare
pip install pytest "mutmut<3"

# Navighează la proiect
cd /mnt/c/Users/<user>/Documents/GitHub/TSS_Proiect

# Rulează analiza mutanților
python -m mutmut run --paths-to-mutate fitness_class_booking.py --tests-dir .
python -m mutmut results
python -m mutmut show <ID>
```

### Script complet (bash/WSL)
```bash
chmod +x run_coverage.sh
./run_coverage.sh
```

---

## 7. Structura proiectului

```
TSS_Proiect/
├── fitness_class_booking.py          # Clasa de testat
├── test_equivalence_partitioning.py  # Strategia 1: clase de echivalență
├── test_boundary_value_analysis.py   # Strategia 2: valori de frontieră (BVA)
├── test_coverage.py                  # Strategiile 3-5: stmt/decision/condition
├── test_independent_circuits.py      # Strategia 6: McCabe / basis path testing
├── test_mutation.py                  # Strategiile 7-8: analiză mutanți
├── run_coverage.sh                   # Script de rulare complet
└── README.md                         # Acest fișier
```

---

*Proiect universitar TSS – T1 Testare unitară Python | `unittest` + `pytest` + `coverage` + `mutmut`*
