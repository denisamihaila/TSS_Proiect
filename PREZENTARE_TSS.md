# Plan prezentare TSS – 10 slide-uri

Prezentarea este gândită ca material principal pentru susținerea orală.
README-ul rămâne documentația completă, iar slide-urile sintetizează cât mai
mult din el în limita celor 10 slide-uri cerute.

Design: temă dark navy (#0F172A) cu accente blue/teal/green/amber, fonturi
Calibri, tabele și vizualizări dedicate fiecărui subiect.

---

## Slide 1 – Titlu

**Badge:** Testarea Sistemelor Software  
**Titlu principal:** TSS T1  
**Subtitlu:** Testare unitară în Python

Informații incluse:

- Proiect: `FitnessClassBooking`
- Metodă: `evaluate_client_package(session_history, package_sessions, has_membership)`
- Framework: pytest 9.0.3 | coverage.py 7.13.5 | mutmut 2.5.1 | Cosmic Ray
- Card-uri laterale cu metrici: **99 teste principale**, **100% coverage**, **0 mutanți survived**

---

## Slide 2 – Cerințe T1 și mapare pe implementare

Informații incluse:

- **Tabel strategii** (stânga): fiecare strategie cerută mapată pe fișierul de teste
  - Clase de echivalență → `test_equivalence_partitioning.py`
  - Valori de frontieră → `test_boundary_value_analysis.py`
  - Coverage instrucțiune/decizie/condiție → `test_coverage.py`
  - Circuite independente → `test_independent_circuits.py`
  - Mutation testing → `test_mutation.py`
- **Tabel cerințe structurale** (dreapta): elementele din metodă care permit testarea structurală

| Cerință | Implementare |
| --- | --- |
| ≥ 3 parametri | `session_history`, `package_sessions`, `has_membership` |
| Instrucțiune repetitivă | `for session_status in session_history` |
| `if` cu `else` | `if session_status == "attended": … else: …` |
| `if` fără `else` | `if has_membership: …` |
| Condiție simplă | `if has_membership` |
| Condiție compusă | `remaining_sessions == 0 and no_show == 0` |

- **Notă amber**: Python – `bool` este subclasă a `int` → validarea separată este obligatorie

---

## Slide 3 – Funcționalitatea testată

Informații incluse:

- Semnătura constructorului și a metodei testate (cod box vizual)
- **Tabel statusuri** (stânga):

| Status | Semnificație | Consumă ședință? |
| --- | --- | --- |
| `attended` | Clientul a participat | Da (verde) |
| `no_show` | Absent fără anunț | Da (roșu) |
| `cancelled` | Anulat la timp | Nu (amber) |

- **Exemplu de calcul** (dreapta):
  - Input: `["attended","attended","cancelled","no_show"]`, `package=5`, `has_membership=True`
  - `used_sessions=3`, `remaining=2`, `cancelled=1`
  - `cost = 5×50×0.80 = 200.0`, `status = active`
- **Card-uri statusuri finale**: `active` | `completed_successfully` | `completed_with_absences`

---

## Slide 4 – Validări și reguli de business

Informații incluse:

- **Tabel constructor** (stânga):
  - `class_name` ∈ {dance, pilates, yoga, zumba}
  - `instructor`: șir nevid după `strip()`
  - `price_per_session`: număr pozitiv; `bool` respins explicit
- **Tabel metodă** (dreapta):
  - `session_history`: de tip `list`
  - `package_sessions`: `int` în `[1, 20]`; `bool` respins explicit
  - `has_membership`: strict `bool`
  - Statusuri necunoscute → `ValueError`
  - Consum > pachet → `ValueError`
- **Bloc amber** – Caz special Python: `bool` subclasă de `int`:
  - `price_per_session=False` → ValueError
  - `package_sessions=True` → ValueError
  - `package_sessions=False` → ValueError
  - `has_membership=1` → ValueError
- **Vizualizare frontiere** `package_sessions`: 0 (invalid) | 1 | 2 | ··· | 19 | 20 | 21 (invalid)
- Discount membership 20%: `total_cost = package_sessions × price_per_session × 0.80`

---

## Slide 5 – Proiectarea suitei principale de teste

Informații incluse:

| Fișier | Strategie | Nr. teste | Rol principal |
| --- | --- | ---: | --- |
| `test_equivalence_partitioning.py` | Clase de echivalență | 22 | Domenii valide/invalide |
| `test_boundary_value_analysis.py` | Valori de frontieră | 16 | Limite la 1, 20 și depășiri |
| `test_coverage.py` | Instrucțiune/Decizie/Condiție | 40 | Execuția tuturor ramurilor |
| `test_independent_circuits.py` | Circuite independente | 10 | Drumuri reprezentative |
| `test_mutation.py` | Teste orientate pe mutanți | 11 | Întărire mutation testing |

- **Total: 99 teste** (highlight verde)
- **Card-uri rezumat**:
  - Funcțional: 22+16 = 38 (Echivalență + Frontiere)
  - Structural: 40+10 = 50 (Coverage + Circuite)
  - Mutation: 11 (Orientate pe mutanți)

---

## Slide 6 – Testare funcțională: Echivalență și Frontiere

Informații incluse:

- **Clase valide** (stânga):
  - `class_name` ∈ {dance, pilates, yoga, zumba}
  - Instructor nevid (ex: 'Ana Pop')
  - Preț pozitiv
  - Historic valid: goală sau cu statusuri corecte
  - `package_sessions` ∈ [1, 20]
  - `has_membership`: True sau False
- **Clase invalide** (dreapta):
  - `class_name`: 'spinning', None, 123
  - Instructor: '', '   ', 42
  - Preț: 0, -10, True, False, 'cincizeci'
  - `session_history`: None, tuple, string
  - `package_sessions`: 0, 21, True, False, 5.0
  - `has_membership`: 1, 0, 'yes', None
  - Status: 'present', 'absent'
  - Consum > pachet: 6 attended cu package=5
- **Vizualizare frontiere package_sessions**:
  `0 (invalid) | 1 (min valid) | 2 (min+1) | ··· | 19 (max−1) | 20 (max valid) | 21 (invalid)`
- **Frontiere price_per_session**:
  - `< 0` → ValueError | `= 0` → ValueError | `> 0` → Valid | `bool` → ValueError

---

## Slide 7 – Testare structurală, CFG și Coverage

Informații incluse:

- **Ramuri testate explicit** (12 ramuri):
  1. Validări constructor
  2. Validări metodă
  3. Loop: status `attended`
  4. Loop: status `no_show`
  5. Loop: status `cancelled`
  6. Status invalid în buclă
  7. Depășire pachet
  8. With membership
  9. Without membership
  10. Status: `active`
  11. Status: `completed_successfully`
  12. Status: `completed_with_absences`
- **Tabel coverage**:

| Metrică | Valoare | Status |
| --- | --- | --- |
| Statements | 43 / 43 | 100% |
| Missing | 0 | — |
| Branches | 26 / 26 | 100% |
| Partial branches | 0 | — |
| Overall | fitness_class_booking.py | 100% |

- **Notă**: Coverage 100% arată execuția completă, dar mutation testing completează imaginea
- **Diagrame** (Draw.io):
  - `cfg_diagrama.drawio.png` – Control Flow Graph al metodei
  - `cause_effect_graph.png` – Relații condiții → reguli → rezultate

---

## Slide 8 – Mutation Testing: mutmut și Cosmic Ray

Informații incluse:

- **mutmut 2.5.1** (WSL Ubuntu 24.04.1):
  - Mutanți verificați: 95/95
  - Killed: **80** (verde)
  - Suspicious: **15** (amber)
  - Survived: **0** (verde)
  - Timeout / Skipped: 0 / 0
  - Notă: Suspicious ≠ Survived – rulări lente, nu mutanți supraviețuitori
- **Cosmic Ray** (analiză suplimentară):
  - Mutanți generați: 166
  - Killed: 157
  - Survived: **9** (amber)
  - Rată supraviețuire: 5.42%
  - Scor kill: **94.58%** (verde)
  - Notă: operatori diferiți față de mutmut → verificare complementară
- **test_mutation.py** (11 teste) verifică explicit:
  - costul pe pachetul complet, nu pe ședințele folosite
  - discount de exact 20%
  - `cancelled` nu consumă ședință
  - statusul final depinde de `remaining_sessions` ȘI `no_show`
  - mesaje de eroare stabile

---

## Slide 9 – Utilizarea AI și suita asistată

Informații incluse:

- **Activități AI** (ChatGPT/Codex):
  - Revizuirea suitei proprii
  - Identificarea cazurilor-limită (bool vs int)
  - Propunerea testelor pentru mutanți
  - Construirea suitei independente `teste_ai/`
  - Compararea suitelor
  - Formularea interpretărilor pentru coverage și mutation testing
- **Suita AI** – `teste_ai/` (70 teste):

| Fișier | Nr. | Stil |
| --- | ---: | --- |
| `test_ai_generated_booking.py` | 13 | Scenarii business cu `dataclass` |
| `test_ai_equivalence_and_validation.py` | 21 | Parametrizări echivalență+validare |
| `test_ai_boundary_and_structural.py` | 22 | Limite, ramuri, rotunjire |
| `test_ai_paths_and_mutation_focus.py` | 14 | Proprietăți, drumuri, mutații |

- **Tabel comparativ**:

| Criteriu | Suita proprie | Suita AI |
| --- | --- | --- |
| Număr teste | 99 | 70 |
| Organizare | Pe tehnici de testare | Pe scenarii, validări, proprietăți |
| Stil | Explicit, didactic | Compact, parametrizat |
| Scop | Demonstrarea strategiilor cerute | Perspectivă independentă |
| Coverage | 100% (confirmat) | Confirmă comportamentul |

- **Studii de caz AI**: bool vs int | egalitate string via `==` nu `is` | statusuri construite dinamic

---

## Slide 10 – Rezultate finale și livrabile

Informații incluse:

- **6 card-uri metrici**:
  - 99 – teste principale
  - 70 – teste AI
  - 100% – statement coverage
  - 100% – branch coverage
  - 0 – mutanți survived (mutmut)
  - 94.58% – kill rate (Cosmic Ray)
- **Livrabile**:
  - `README.md` – documentație completă (710 linii)
  - `fitness_class_booking.py` – clasa testată
  - `test_*.py` (5 fișiere) – suita principală 99 teste
  - `teste_ai/` (4 fișiere) – suita AI 70 teste
  - `cfg_diagrama.drawio.png`, `cause_effect_graph.png`
  - `screenshots/` (7 capturi) + `logs/` + `cosmic_ray/`
  - `TSS_T1_FitnessClassBooking.pptx` – prezentarea
- **Concluzie**: Proiectul respectă cerința T1 – testare funcțională + structurală +
  mutation testing + analiză asistată de AI. Suita este stabilă și bine focalizată
  pe contractul public al clasei.
