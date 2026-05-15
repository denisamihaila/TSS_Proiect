# PREZENTARE_TSS – Structura detaliată a celor 10 slide-uri

Acest fișier conține conținutul complet pentru PowerPoint-ul de 10 slide-uri.
Toate datele sunt preluate din README.md și din fișierele proiectului.
Fiecare slide are titlu, subtitlu, tabelele gata scrise și punctele de vorbit.

---

## Slide 1 – Titlu și context general

**Titlu principal:** TSS T1 – Testare unitară în Python
**Subtitlu:** FitnessClassBooking · evaluate_client_package

### Conținut

| | |
|---|---|
| Disciplina | Testarea Sistemelor Software |
| Tema | T1 – Testare unitară în Python |
| Fișier principal | `fitness_class_booking.py` |
| Metodă testată | `evaluate_client_package(session_history, package_sessions, has_membership)` |
| Framework | pytest 9.0.3 |
| Coverage | coverage.py 7.13.5 |
| Mutation testing | mutmut 2.5.1 · Cosmic Ray |

### Metrici cheie (card-uri vizuale)

| Metrică | Valoare |
|---|---|
| Teste principale | **100 passed** |
| Coverage | **100%** (statement + branch) |
| Mutanți survived (mutmut) | **0** |
| Kill rate (Cosmic Ray) | **94.58%** |
| Teste AI | **70 passed** |

### Mesaj de susținere
Proiectul este concentrat pe o singură funcționalitate, dar aceasta conține
suficiente ramuri, validări și rezultate pentru a demonstra toate strategiile
cerute la curs.

---

## Slide 2 – Cerințele temei T1 și mapare pe implementare

**Titlu:** Cerințele temei T1 și mapare pe cod
**Subtitlu:** Toate strategiile cerute sunt acoperite · Framework: pytest

### Tabel strategii de testare

| Strategie cerută | Fișier de teste |
|---|---|
| Partiționare în clase de echivalență | `test_equivalence_partitioning.py` |
| Analiza valorilor de frontieră | `test_boundary_value_analysis.py` |
| Acoperire instrucțiune / decizie / condiție | `test_coverage.py` |
| Circuite independente | `test_independent_circuits.py` |
| Analiză pe baza unui generator de mutanți | `test_mutation.py` |
| Teste suplimentare pentru mutanți neechivalenți | `test_mutation.py` |

### Tabel cerințe structurale ale metodei

| Cerință | Implementare în cod |
|---|---|
| Minimum 3 parametri | `session_history`, `package_sessions`, `has_membership` |
| Instrucțiune repetitivă | `for session_status in session_history` |
| `if` cu `else` | `if session_status == "attended": … else: …` |
| `if` fără `else` | `if has_membership: …` |
| Condiție simplă | `if has_membership` |
| Condiție compusă | `remaining_sessions == 0 and no_show == 0` |

### Notă importantă
**Python: `bool` este subclasă a `int`** → `True` și `False` ar trece ca `1`
și `0` prin validări numerice dacă nu sunt respinse explicit. Implementarea
conține verificare separată pentru `bool` la toți parametrii numerici.

---

## Slide 3 – Clasa FitnessClassBooking și funcționalitatea testată

**Titlu:** Clasa FitnessClassBooking – Funcționalitate testată
**Subtitlu:** Evaluarea stării unui pachet de ședințe de fitness cumpărat de un client

### Semnăturile metodelor (cod)

```python
# Constructor
booking = FitnessClassBooking(class_name, instructor, price_per_session)

# Metoda principală testată
result = booking.evaluate_client_package(session_history, package_sessions, has_membership)
```

### Statusuri acceptate în `session_history`

| Status | Semnificație | Consumă ședință din pachet? |
|---|---|---|
| `attended` | Clientul a participat la ședință | **Da** |
| `no_show` | Clientul nu s-a prezentat și nu a anunțat | **Da** |
| `cancelled` | Clientul a anulat la timp | **Nu** |

### Exemplu complet de calcul

**Input:**
```python
booking = FitnessClassBooking("yoga", "Ana Pop", 50)
result = booking.evaluate_client_package(
    ["attended", "attended", "cancelled", "no_show"], 5, True
)
```

**Output:**
```python
{
    "attended": 2,        # 2 participări
    "no_show": 1,         # 1 absență
    "cancelled": 1,       # 1 anulare (nu consumă)
    "used_sessions": 3,   # attended + no_show
    "remaining_sessions": 2,  # 5 - 3
    "total_cost": 200.0,  # 5 × 50 × 0.80 (discount 20%)
    "status": "active",   # mai are ședințe rămase
}
```

### Statusul final al pachetului

| Status | Condiție |
|---|---|
| `active` | `remaining_sessions > 0` |
| `completed_successfully` | `remaining_sessions == 0` și `no_show == 0` |
| `completed_with_absences` | `remaining_sessions == 0` și `no_show > 0` |

### Constante ale clasei
- `VALID_CLASSES = {"dance", "pilates", "yoga", "zumba"}`
- `MAX_PACKAGE_SESSIONS = 20`
- `MEMBERSHIP_DISCOUNT = 0.20`

---

## Slide 4 – Validări și reguli de business

**Titlu:** Validări și reguli de business
**Subtitlu:** Orice intrare invalidă aruncă `ValueError` – testele verifică mesajele publice

### Validări constructor `__init__`

| Parametru | Regulă |
|---|---|
| `class_name` | Trebuie să fie `str` și în `{dance, pilates, yoga, zumba}` |
| `instructor` | Trebuie să fie `str` nevid după `strip()` → `"   "` este invalid |
| `price_per_session` | Număr pozitiv; `bool` respins explicit; zero și negativ invalide |

### Validări metodă `evaluate_client_package`

| Parametru | Regulă |
|---|---|
| `session_history` | Trebuie să fie de tip `list` |
| `package_sessions` | `int` în intervalul `[1, 20]`; `bool` respins explicit |
| `has_membership` | Strict `bool` – `1` sau `0` nu sunt acceptate |
| Fiecare status din istoric | Trebuie să fie `attended`, `no_show` sau `cancelled` |
| Consum vs pachet | `used_sessions` nu poate depăși `package_sessions` |

### Caz special Python: `bool` este subclasă a `int`

Fără verificare explicită, aceste apeluri ar trece validările numerice:

| Apel | Comportament fără verificare | Comportament cu verificare |
|---|---|---|
| `price_per_session=False` | acceptat ca `0` | `ValueError` |
| `package_sessions=True` | acceptat ca `1` | `ValueError` |
| `package_sessions=False` | acceptat ca `0` | `ValueError` |
| `has_membership=1` | acceptat ca `True` | `ValueError` |

### Frontiere `package_sessions`

```
  0        1    2   ···   19   20       21
[INVALID] [MIN]             [MAX] [INVALID]
```

Valorile `0`, `21`, `True`, `False` produc `ValueError("invalid package data")`.

### Formula cost cu membership
```
total_cost = package_sessions × price_per_session × (1 − 0.20)
```
Costul se calculează pe **pachetul întreg**, nu pe ședințele folosite.

---

## Slide 5 – Proiectarea suitei principale de teste

**Titlu:** Suita principală de teste – 100 teste
**Subtitlu:** Organizate explicit pe tehnicile cerute în tema T1

### Tabel complet

| Fișier | Strategie | Nr. teste | Rol principal |
|---|---|---:|---|
| `test_equivalence_partitioning.py` | Clase de echivalență | 23 | Domenii valide și invalide pentru constructor și metodă |
| `test_boundary_value_analysis.py` | Valori de frontieră | 16 | Limite la `0`, `1`, `2`, `19`, `20`, `21`; prețuri limită |
| `test_coverage.py` | Instrucțiune / Decizie / Condiție | 40 | Execuția tuturor ramurilor și condițiilor atomice |
| `test_independent_circuits.py` | Circuite independente | 10 | 10 drumuri reprezentative prin CFG |
| `test_mutation.py` | Teste orientate pe mutanți | 11 | Întărirea suitei pentru omoarea mutanților neechivalenți |
| **TOTAL** | | **100** | |

### Rezumat pe categorii

| Categorie | Fișiere | Total teste |
|---|---|---:|
| Testare funcțională | echivalență + frontiere | 23 + 16 = **39** |
| Testare structurală | coverage + circuite | 40 + 10 = **50** |
| Mutation-focused | test_mutation | **11** |

### De ce `setUp` în unele fișiere?
`test_equivalence_partitioning.py` și `test_boundary_value_analysis.py` folosesc
`setUp` pentru a crea un singur obiect `self.booking = make_booking()` reutilizat
în toate testele clasei — evită repetarea constructorului.

---

## Slide 6 – Testare funcțională: Echivalență și Frontiere

**Titlu:** Testare funcțională – Clase de echivalență și Valori de frontieră
**Subtitlu:** 23 teste echivalență + 16 teste frontiere

### Clase valide (ce trebuie să funcționeze)

- `class_name` ∈ `{dance, pilates, yoga, zumba}` — toate 4 testate explicit
- `instructor`: șir nevid, inclusiv cu un singur caracter (`"A"`)
- `price_per_session`: orice număr pozitiv (ex: `0.01`, `50.0`)
- `session_history`: listă goală sau cu statusuri valide (`attended`, `no_show`, `cancelled`)
- `package_sessions`: orice `int` în `[1, 20]`
- `has_membership`: `True` sau `False`
- Istoric cu toate tipurile de status simultan
- Pachete active, finalizate cu succes, finalizate cu absențe

### Clase invalide (ce trebuie să arunce `ValueError`)

- `class_name`: `"spinning"`, `None`, `123`, `"YOGA"` (case-sensitive)
- `instructor`: `""`, `"   "`, `42`, `None`
- `price_per_session`: `0`, `-10`, `True`, `False`, `"cincizeci"`
- `session_history`: `None`, `("attended",)` (tuple), `"attended"` (string)
- `package_sessions`: `0`, `21`, `True`, `False`, `5.0`
- `has_membership`: `1`, `0`, `"yes"`, `None`
- Status necunoscut: `"late"`, `"present"`, `"absent"`
- Consum depășit: `["attended"] × 4` cu `package_sessions=3`

### Frontierele `package_sessions` — vizualizare

| Valoare | Clasificare |
|---:|---|
| `0` | **Invalid** – sub limita minimă |
| `1` | **Valid** – valoare minimă |
| `2` | **Valid** – min + 1 |
| `19` | **Valid** – max − 1 |
| `20` | **Valid** – valoare maximă |
| `21` | **Invalid** – peste limita maximă |

### Frontierele `price_per_session`

| Valoare | Rezultat |
|---|---|
| `< 0` | `ValueError` |
| `= 0` | `ValueError` |
| `0.01` | Valid (minim pozitiv) |
| `bool` | `ValueError` |

### Frontiera `used_sessions` vs `package_sessions`

| Situație | Rezultat |
|---|---|
| `used < package` | pachet activ |
| `used == package` | pachet finalizat |
| `used > package` | `ValueError("used sessions cannot exceed package sessions")` |

---

## Slide 7 – Testare structurală: Coverage și Circuite independente

**Titlu:** Testare structurală – Coverage 100% și Circuite independente
**Subtitlu:** 40 teste coverage + 10 circuite · 43 instrucțiuni · 26 ramuri · 100%

### Ramuri testate explicit (acoperire decizie)

| # | Ramură | Test reprezentativ |
|---|---|---|
| 1 | Validare constructor – `class_name` invalid | `test_sc_constructor_invalid_class_raises` |
| 2 | Validare constructor – `instructor` invalid | `test_sc_constructor_invalid_instructor_raises` |
| 3 | Validare constructor – `price` invalid | `test_sc_constructor_invalid_price_raises` |
| 4 | Validare metodă – parametri invalizi | `test_dc_package_validation_true` |
| 5 | Status invalid în buclă | `test_sc_invalid_session_status_raises` |
| 6 | Ramura `attended` | `test_dc_attended_branch_true` |
| 7 | Ramura `no_show` | `test_dc_attended_branch_false_no_show` |
| 8 | Ramura `cancelled` | `test_dc_cancelled_branch_true` |
| 9 | Depășire pachet | `test_dc_used_sessions_over_package_true` |
| 10 | With membership | `test_dc_membership_true` |
| 11 | Without membership | `test_dc_membership_false` |
| 12 | Status `completed_successfully` | `test_dc_completed_successfully_condition_true` |
| 13 | Status `completed_with_absences` | `test_dc_completed_successfully_condition_false_absences` |
| 14 | Status `active` | `test_dc_completed_successfully_condition_false_active` |

### Acoperire condiții atomice (coverage condiție)

Condiția compusă `remaining_sessions == 0 and no_show == 0` este acoperită
pe toate combinațiile:

| `remaining == 0` | `no_show == 0` | Status | Test |
|---|---|---|---|
| True | True | `completed_successfully` | `test_cc_compound_status_both_atomic_conditions_true` |
| True | False | `completed_with_absences` | `test_cc_compound_status_remaining_true_no_show_false` |
| False | — | `active` | `test_cc_compound_status_remaining_false` |

### Rezultat coverage.py

```
Name                       Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------
fitness_class_booking.py      43      0     26      0   100%
```

- **43 instrucțiuni** – toate acoperite (Miss = 0)
- **26 ramuri** – toate acoperite (BrPart = 0)
- **100% coverage** statement și branch

### Diagrame realizate cu Draw.io

| Diagramă | Fișier | Conținut |
|---|---|---|
| Control Flow Graph (CFG) | `cfg_diagrama.drawio.png` | Fluxul complet al metodei `evaluate_client_package` |
| Cause-Effect Graph | `cause_effect_graph.png` | Relații între condiții de intrare și rezultate |

### Cele 10 circuite independente (drumuri prin CFG)

| Cale | Descriere |
|---|---|
| Path 1 | Parametri invalizi → `ValueError` imediat |
| Path 2 | Istoric gol → pachet activ |
| Path 3 | Status invalid în buclă → `ValueError` |
| Path 4 | Doar `attended` → `completed_successfully` |
| Path 5 | Doar `no_show` → `completed_with_absences` |
| Path 6 | Doar `cancelled` → pachet activ, 0 consumate |
| Path 7 | Istoric mixt cu membership → activ |
| Path 8 | Depășire pachet → `ValueError` |
| Path 9 | `attended` + membership → activ |
| Path 10 | Pachet complet cu membership → `completed_successfully` |

---

## Slide 8 – Mutation Testing: mutmut și Cosmic Ray

**Titlu:** Mutation Testing – mutmut și Cosmic Ray
**Subtitlu:** Două instrumente complementare cu operatori diferiți

### Rezultate mutmut 2.5.1 (rulat în WSL Ubuntu 24.04.1)

| Categorie | Valoare |
|---|---:|
| Mutanți verificați | 95 / 95 |
| **Killed** | **85** |
| **Survived** | **0** |
| Suspicious | 10 |
| Timeout | 0 |
| Skipped | 0 |

**Interpretare Suspicious:** nu este echivalent cu Survived. Categoria
`Suspicious` indică rulări mai lente decât baseline-ul, fără timeout fatal.
Rezultatul important este **0 survived**.

### Rezultate Cosmic Ray (analiză suplimentară)

| Categorie | Valoare |
|---|---:|
| Mutanți generați | 166 |
| **Killed** | **157** |
| **Survived** | **9** |
| Rată supraviețuire | 5.42% |
| **Scor kill** | **94.58%** |

**Interpretare:** Cosmic Ray generează mai mulți mutanți cu operatori diferiți
față de mutmut → verificare complementară și independentă a robusteții suitei.
Cei 9 supraviețuitori sunt mutații aproape echivalente cu comportamentul original.

### Comparație instrumente

| Tool | Mutanți | Killed | Survived | Scor |
|---|---:|---:|---:|---|
| mutmut | 95 | 85 | 0 | 100% (0 survived) |
| Cosmic Ray | 166 | 157 | 9 | 94.58% |

### Ce verifică `test_mutation.py` (11 teste)

Testele sunt scrise specific pentru a omorî mutanți neechivalenți:

- Costul se calculează pe **pachetul complet**, nu pe ședințele folosite
  → ex: 1 `attended` din pachet de 5 costă `5 × 50 = 250`, nu `1 × 50`
- Membership aplică reducere de **exact 20%** (nu 10%, nu 30%)
- `cancelled` **nu consumă** ședință din pachet
- `no_show` **consumă** ședință și blochează `completed_successfully`
- Statusul final depinde de `remaining_sessions` **ȘI** `no_show` simultan
- Rotunjirea costului la 2 zecimale: `round(1/3, 2) == 0.33`
- Mesajele publice de eroare sunt stabile și exacte (testate cu `assertRaisesRegex`)

---

## Slide 9 – Utilizarea AI și suita asistată

**Titlu:** Utilizarea AI – ChatGPT/Codex ca instrument de verificare
**Subtitlu:** Perspectivă independentă · Nu înlocuiește validarea manuală

### Cum a fost utilizat AI

| Activitate | Descriere |
|---|---|
| Revizuire suitei proprii | Verificare completitudine ramuri, condiții, cazuri invalide |
| Identificare cazuri-limită | `bool` vs `int` în Python, string equality `==` vs `is` |
| Teste suplimentare | Propuneri pentru mutanți neechivalenți |
| Suită independentă | Construirea `teste_ai/` cu stil diferit față de suita proprie |
| Comparație suite | Analiză diferențe organizare și acoperire |
| Interpretare rezultate | Formularea interpretărilor pentru coverage și mutation testing |

**Principiu:** Propunerile AI au fost păstrate **doar după verificare locală**.
Validarea finală = rularea testelor, nu acceptarea automată a răspunsurilor.

### Suita AI – `teste_ai/` (70 teste)

| Fișier | Nr. teste | Stil |
|---|---:|---|
| `test_ai_generated_booking.py` | 13 | Scenarii de business cu `dataclass` |
| `test_ai_equivalence_and_validation.py` | 21 | Parametrizări pentru echivalență și validare |
| `test_ai_boundary_and_structural.py` | 22 | Limite, ramuri structurale și rotunjire |
| `test_ai_paths_and_mutation_focus.py` | 14 | Proprietăți, drumuri și cazuri orientate pe mutații |
| **TOTAL** | **70** | |

Rulare: `python -m pytest -q teste_ai` → **70 passed**

### Comparație suita proprie vs suita AI

| Criteriu | Suita proprie (100 teste) | Suita AI (70 teste) |
|---|---|---|
| Organizare | Pe tehnici de testare | Pe scenarii, validări și proprietăți |
| Stil | Explicit, didactic, corelat cu cerința | Compact, parametrizat, orientat pe scenarii |
| Scop | Demonstrarea strategiilor cerute | Perspectivă suplimentară independentă |
| Coverage | 100% confirmat | Confirmă comportamentul, rulată separat |
| Mutation focus | Fișier dedicat `test_mutation.py` | Teste pentru egalitate string, bool, proprietăți |

### Studii de caz identificate cu ajutorul AI

**Caz 1: `bool` față de `int`**
În Python, `bool` este subclasă a `int`. Testele verifică explicit:
- `price_per_session=False` → `ValueError`
- `package_sessions=True` → `ValueError`
- `has_membership=1` → `ValueError`

**Caz 2: Egalitatea stringurilor**
Testul `test_ai_mutation_status_matching_uses_value_equality_for_dynamic_strings`
construiește statusurile prin operații de string și verifică că metoda le compară
prin valoare (`==`), nu prin identitate (`is`). Util pentru mutanți care înlocuiesc `==` cu `is`.

---

## Slide 10 – Rezultate finale și concluzie

**Titlu:** Rezultate finale și concluzie
**Subtitlu:** TSS T1 – testare funcțională + structurală + mutation testing + AI

### Toate rezultatele

| Metric | Rezultat |
|---|---|
| Teste suită principală | **100 passed** |
| Teste suită AI | **70 passed** |
| Statement coverage | **100%** (43 / 43 instrucțiuni) |
| Branch coverage | **100%** (26 / 26 ramuri) |
| mutmut – killed | **85 / 95** |
| mutmut – survived | **0** |
| mutmut – suspicious | 10 (≠ survived) |
| Cosmic Ray – kill rate | **94.58%** (157 / 166) |
| Cosmic Ray – survived | 9 |

### Livrabile finale

| Fișier / Folder | Conținut |
|---|---|
| `README.md` | Documentație completă (710 linii) |
| `fitness_class_booking.py` | Clasa testată |
| `test_equivalence_partitioning.py` | 23 teste – clase de echivalență |
| `test_boundary_value_analysis.py` | 16 teste – valori de frontieră |
| `test_coverage.py` | 40 teste – coverage instrucțiune/decizie/condiție |
| `test_independent_circuits.py` | 10 teste – circuite independente |
| `test_mutation.py` | 11 teste – orientate pe mutanți |
| `teste_ai/` | 70 teste asistate AI |
| `cfg_diagrama.drawio.png` | Control Flow Graph |
| `cause_effect_graph.png` | Cause-Effect Graph |
| `screenshots/` | 7 capturi cu rulările finale |
| `logs/` | Output-uri text pytest, coverage, mutmut |
| `cosmic_ray/` | Artefacte Cosmic Ray |
| `TSS_T1_FitnessClassBooking.pptx` | Prezentarea PowerPoint |

### Concluzie

Proiectul respectă cerința temei T1: o suită unitară organizată pe tehnicile
studiate la curs, cu rezultate confirmate prin rulări locale.

Metoda `evaluate_client_package` a permis verificarea coerentă a:
- claselor de echivalență și valorilor de frontieră (testare funcțională);
- acoperirii complete a instrucțiunilor și ramurilor (testare structurală);
- circuitelor independente prin graful de flux al controlului;
- rezistenței la mutații prin două instrumente complementare;
- comportamentului față de cazuri specifice Python (`bool` ca subclasă a `int`).

Rezultatele indică o suită stabilă și bine focalizată pe contractul public al clasei.
