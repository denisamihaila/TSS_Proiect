# PREZENTARE_TSS – Conținut detaliat pentru cele 10 slide-uri

Documentul urmărește structura README.md și propune ce să apară pe fiecare
slide, în ce ordine și cu ce nivel de detaliu. Toate datele sunt preluate
direct din proiect.

---

## Slide 1 – Titlu și context

**Titlu mare:** TSS T1 – Testare unitară în Python
**Subtitlu:** FitnessClassBooking · `evaluate_client_package`

### Bloc informații generale

| | |
|---|---|
| Disciplina | Testarea Sistemelor Software |
| Tema | T1 – Testare unitară în Python |
| Clasa testată | `FitnessClassBooking` |
| Metoda principală | `evaluate_client_package(session_history, package_sessions, has_membership)` |
| Framework testare | pytest 9.0.3 |
| Coverage | coverage.py 7.13.5 |
| Mutation testing | mutmut 2.5.1 |
| Mediu rulare | Windows 11 Pro · Python 3.13.3 · WSL Ubuntu 24.04.1 |

### Metrici cheie (4 card-uri vizuale)

| Metric | Valoare |
|---|---|
| Teste principale | **100 passed** |
| Statement + Branch coverage | **100%** |
| Mutanți survived (mutmut) | **0** |

---

## Slide 2 – Aplicația testată și funcționalitatea metodei

**Titlu:** Clasa FitnessClassBooking – Ce testăm și de ce
**Subtitlu:** Evaluarea stării unui pachet de ședințe de fitness

### Descrierea clasei și metodei

**`FitnessClassBooking`** este o clasă Python care modelează o clasă de
fitness dintr-un sistem de rezervări. Constructorul primește tipul clasei
(`class_name`), instructorul și prețul per ședință, și validează aceste
date la creare.

**`evaluate_client_package`** este metoda principală testată. Primește
istoricul ședințelor unui client (`session_history`), numărul de ședințe
din pachetul cumpărat (`package_sessions`) și dacă clientul are membership
(`has_membership`). Pe baza acestora calculează câte ședințe au fost
consumate, câte au rămas, costul total al pachetului (cu sau fără discount)
și statusul final al pachetului.

### Semnăturile metodelor

```python
booking = FitnessClassBooking(class_name, instructor, price_per_session)

result = booking.evaluate_client_package(session_history, package_sessions, has_membership)
```

### Statusurile din `session_history`

| Status | Semnificație | Consumă ședință? |
|---|---|---|
| `attended` | Clientul a participat | **Da** |
| `no_show` | Absent fără anunț prealabil | **Da** |
| `cancelled` | Anulat la timp | **Nu** |

### Exemplu complet de calcul

**Input:**
```
["attended", "attended", "cancelled", "no_show"],  package_sessions=5,  has_membership=True
```
**Output:**
```
attended=2 · no_show=1 · cancelled=1
used_sessions=3 · remaining=2
total_cost = 5 × 50 × 0.80 = 200.0
status = "active"
```

### Statusul final al pachetului

| Status | Condiție |
|---|---|
| `active` | `remaining_sessions > 0` |
| `completed_successfully` | `remaining_sessions == 0` și `no_show == 0` |
| `completed_with_absences` | `remaining_sessions == 0` și `no_show > 0` |

---

## Slide 3 – Cerințele temei T1 și structura metodei

**Titlu:** Cerințele temei T1 – Strategii și structură
**Subtitlu:** Toate strategiile cerute sunt acoperite · Framework: pytest

### Strategii de testare cerute

| Strategie | Fișier de teste | Nr. teste |
|---|---|---:|
| Partiționare în clase de echivalență | `test_equivalence_partitioning.py` | 23 |
| Analiza valorilor de frontieră | `test_boundary_value_analysis.py` | 16 |
| Acoperire instrucțiune / decizie / condiție | `test_coverage.py` | 40 |
| Circuite independente | `test_independent_circuits.py` | 10 |
| Analiză mutanți + teste suplimentare | `test_mutation.py` | 11 |
| **TOTAL** | | **100** |

### Distribuția celor 100 de teste pe categorii

| Categorie | Strategii acoperite | Fișiere | Nr. teste |
|---|---|---|---:|
| Testare funcțională | Echivalență + Frontiere | 2 fișiere | **39** |
| Testare structurală | Coverage + Circuite independente | 2 fișiere | **50** |
| Mutation-focused | Teste orientate pe mutanți | 1 fișier | **11** |
| **Total** | | | **100** |

### Ce returnează metoda — obiectul verificat de teste

```python
{
    "attended":          int,   # numărul de ședințe la care clientul a participat
    "no_show":           int,   # numărul de absențe nemotivate
    "cancelled":         int,   # numărul de anulări la timp
    "used_sessions":     int,   # ședințe consumate din pachet (attended + no_show)
    "remaining_sessions":int,   # ședințe rămase în pachet
    "total_cost":        float, # costul pachetului întreg, cu sau fără discount
    "status":            str,   # "active" / "completed_successfully" / "completed_with_absences"
}
```

Testele verifică fiecare câmp din acest dicționar — atât individual,
cât și combinat — pentru a confirma că logica metodei este corectă.

---

## Slide 4 – Validări și reguli de business

**Titlu:** Validări și reguli de business
**Subtitlu:** Orice intrare invalidă aruncă `ValueError` cu mesaj stabil

### Validări constructor `__init__`

| Parametru | Regulă |
|---|---|
| `class_name` | `str` și în `{dance, pilates, yoga, zumba}` |
| `instructor` | `str` nevid după `strip()` — `"   "` este invalid |
| `price_per_session` | număr pozitiv; `bool` respins explicit |

### Validări metodă `evaluate_client_package`

| Parametru | Regulă |
|---|---|
| `session_history` | trebuie să fie `list` |
| `package_sessions` | `int` în `[1, 20]`; `bool` respins explicit |
| `has_membership` | strict `bool` — `1` și `0` nu sunt acceptate |
| statusuri din istoric | doar `attended`, `no_show`, `cancelled` |
| consum vs pachet | `used_sessions` ≤ `package_sessions` |

### Cazul special bool / int

| Apel | Fără verificare explicită | Cu verificare explicită |
|---|---|---|
| `price_per_session=False` | acceptat ca `0` | `ValueError` |
| `package_sessions=True` | acceptat ca `1` | `ValueError` |
| `package_sessions=False` | acceptat ca `0` | `ValueError` |
| `has_membership=1` | acceptat ca `True` | `ValueError` |

### Formula costului

```
total_cost = package_sessions × price_per_session          (fără membership)
total_cost = package_sessions × price_per_session × 0.80   (cu membership 20%)
```

Costul se calculează pe **pachetul întreg**, nu pe ședințele folosite.

---

## Slide 5 – Partiționare în clase de echivalență

**Titlu:** Partiționare în clase de echivalență — 23 teste
**Subtitlu:** Grupuri de valori cu comportament identic · câte un reprezentant per clasă

### Clase valide

| Parametru | Clasa validă | Exemplu reprezentativ |
|---|---|---|
| `class_name` | oricare din cele 4 valori | `"dance"`, `"yoga"`, `"zumba"` (toate testate) |
| `instructor` | orice `str` nevid după `strip()` | `"Ana Pop"` |
| `price_per_session` | orice număr pozitiv non-bool | `50.0`, `0.01` |
| `session_history` | `list` goală sau cu statusuri corecte | `[]`, `["attended", "cancelled"]` |
| `package_sessions` | `int` în `[1, 20]` | `5`, `1`, `20` |
| `has_membership` | `True` sau `False` | `True`, `False` |
| output `status` | oricare din cele 3 statusuri | `active`, `completed_successfully`, `completed_with_absences` |

### Clase invalide (fiecare produce `ValueError`)

| Parametru | Clasa 1 | Clasa 2 | Clasa 3 | Clasa 4 |
|---|---|---|---|---|
| `class_name` | tip greșit: `123`, `None` | valoare necunoscută: `"boxing"` | — | — |
| `instructor` | tip greșit: `42`, `None` | gol/spații: `""`, `"   "` | — | — |
| `price_per_session` | tip `bool`: `True`, `False` | non-numeric: `"50"` | nepozitiv: `0`, `-10` | — |
| `session_history` | non-list: `"attended"`, `("a",)` | — | — | — |
| `package_sessions` | tip `bool`: `True`, `False` | non-int: `"5"`, `5.0` | sub limită: `0` | peste limită: `21`, `25` |
| `has_membership` | non-bool: `1`, `0`, `"yes"`, `None` | — | — | — |
| status în istoric | tip greșit: `None`, `42` | valoare necunoscută: `"late"` | — | — |
| consum | `used_sessions > package_sessions` | — | — | — |

### Notă despre bool și int în Python

`price_per_session` și `package_sessions` au câte o clasă invalidă separată
pentru `bool` față de restul valorilor numerice invalide. Motivul: în Python
`bool` este subclasă a lui `int`, deci `True` și `False` ar trece de
`isinstance(..., int)` fără o verificare explicită pusă înaintea ei.

### Test reprezentativ pentru clasa validă mixtă

```python
result = self.booking.evaluate_client_package(
    ["attended", "no_show", "cancelled"], 5, True
)
# attended=1, no_show=1, cancelled=1
# used=2, remaining=3
# total_cost = 5×50×0.80 = 200.0
# status = "active"
```

---

## Slide 6 – Analiza valorilor de frontieră

**Titlu:** Analiza valorilor de frontieră — 16 teste
**Subtitlu:** Valorile de la limita dintre clase valide și invalide — erorile apar cel mai des aici

### Frontierele `package_sessions` — intervalul `[1, 20]`

| Valoare | Clasificare | Ce verifică testul |
|---|---|---|
| `0` | **Invalid** – sub minimă | aruncă `ValueError` |
| `1` | **Valid** – minimă | `remaining=1`, `status="active"` |
| `2` | **Valid** – min+1 | `used=1`, `remaining=1` |
| `19` | **Valid** – max−1 | `remaining=18`, `total_cost=950.0` |
| `20` | **Valid** – maximă | `remaining=19`, `total_cost=1000.0` |
| `21` | **Invalid** – peste maximă | aruncă `ValueError` |

### Frontierele `price_per_session` — condiție `> 0`

| Valoare | Rezultat |
|---|---|
| `-0.01` | `ValueError` — imediat sub zero |
| `0.0` | `ValueError` — exact zero |
| `0.01` | valid — imediat deasupra zero |

### Frontierele `instructor` — lungime după `strip()`

| Valoare | Rezultat |
|---|---|
| `""` | `ValueError` — gol |
| `"A"` | valid — un singur caracter |

### Frontiera de consum — momentul completării pachetului

```python
# cu 1 ședință înainte de final → activ
evaluate_client_package(["attended", "attended"], 3, False)
# remaining=1, status="active"

# consum exact, fără no_show → completed_successfully
evaluate_client_package(["attended", "attended", "attended"], 3, False)
# remaining=0, no_show=0, status="completed_successfully"

# consum exact, cu no_show → completed_with_absences
evaluate_client_package(["attended", "attended", "no_show"], 3, False)
# remaining=0, no_show=1, status="completed_with_absences"

# depășire cu 1 → ValueError
evaluate_client_package(["attended"] * 4, 3, False)
```

---

## Slide 7 – Acoperire structurală: instrucțiune, decizie, condiție

**Titlu:** Acoperire structurală — 40 teste
**Subtitlu:** Statement · Decision · Condition coverage → 43 instrucțiuni · 26 ramuri · **100%**

### Nivel 1 — Acoperire instrucțiune

Fiecare din cele **43 de instrucțiuni** este executată cel puțin o dată.

```
fitness_class_booking.py   Stmts=43   Miss=0   Branch=26   BrPart=0   Cover=100%
```

### Nivel 2 — Acoperire decizie

Fiecare `if` este executat pe ramura **True** și pe ramura **False**.

| Decizie din cod | Ramura True | Ramura False |
|---|---|---|
| Validare parametri metodă | `True`: `"yes"` ca `has_membership` → `ValueError` | `False`: `[], 1, False` → continuă |
| Validare status în buclă | `True`: `["unknown"]` → `ValueError` | `False`: `["cancelled"]` → procesat |
| `if session_status == "attended"` | `True`: `["attended"]` → `attended += 1` | `False`: `["no_show"]` → else |
| `if used_sessions > package_sessions` | `True`: 2 attended, package=1 → `ValueError` | `False`: consum valid → continuă |
| `if has_membership` | `True`: `([], 2, True)` → cost×0.80=80.0 | `False`: `([], 2, False)` → cost=100.0 |
| `if remaining==0 and no_show==0` | `True`: 1 attended, package=1 → `completed_successfully` | `False`: intră în else |
| `if remaining==0` (în else) | `True`: no_show, package=1 → `completed_with_absences` | `False`: remaining>0 → `active` |

### Nivel 3 — Acoperire condiție

Fiecare condiție atomică dintr-o expresie compusă este testată independent.

**Condiția compusă pentru statusul final:** `remaining_sessions == 0 and no_show == 0`

| `remaining == 0` | `no_show == 0` | Status rezultat |
|---|---|---|
| True | True | `completed_successfully` |
| True | False | `completed_with_absences` |
| False | — *(short-circuit)* | `active` |

**Condiția compusă pentru `price_per_session`** — trei condiții atomice, fiecare testată separat:
- `isinstance(price_per_session, bool)` → testată cu `True` ca preț
- `not isinstance(price_per_session, (int, float))` → testată cu `"50"` ca preț
- `price_per_session <= 0` → testată cu `0.0` ca preț

---

## Slide 8 – Circuite independente și diagrame

**Titlu:** Circuite independente — 10 drumuri prin CFG
**Subtitlu:** Un circuit = un drum complet de la intrare la ieșire prin graful de control

### Cele 9 decizii principale (D1–D9)

| | Condiție |
|---|---|
| D1 | Validarea parametrilor metodei |
| D2 | Validarea statusului în buclă |
| D3 | `session_status == "attended"` |
| D4 | `session_status == "no_show"` |
| D5 | `session_status == "cancelled"` |
| D6 | `used_sessions > package_sessions` |
| D7 | `has_membership` |
| D8 | `remaining_sessions == 0 and no_show == 0` |
| D9 | `remaining_sessions == 0` |

### Cele 10 circuite independente

| Cale | Descriere scurtă |
|---|---|
| Path 1 | D1→True: parametri invalizi → excepție imediată |
| Path 2 | D1→False, istoric gol, D6→F, D7→F, D8→F, D9→F: **activ** |
| Path 3 | D2→True: status invalid în buclă → excepție |
| Path 4 | D3→True: `attended`×2, D8→True: **completed_successfully** |
| Path 5 | D4→True: `no_show`, D9→True: **completed_with_absences** |
| Path 6 | D5→True: `cancelled`, D6→F, D9→F: **activ**, 0 consumate |
| Path 7 | Mixt + D7→True: discount aplicat, **activ** |
| Path 8 | D6→True: consum > pachet → excepție |
| Path 9 | D3→True + D7→True: membership, cost pe pachet complet, **activ** |
| Path 10 | D3→True×2 + D7→True + D8→True: **completed_successfully** cu discount |

### Diagrame realizate cu Draw.io

![Control Flow Graph](cfg_diagrama.drawio.png)

![Cause-Effect Graph](cause_effect_graph.png)

*(CFG arată drumurile D1–D9; Cause-Effect arată relațiile între statusuri, membership, cost și statusul final)*

---

## Slide 9 – Mutation Testing: mutmut

**Titlu:** Mutation Testing — mutmut
**Subtitlu:** Testele sunt suficient de precise pentru a detecta modificări greșite ale codului?

### Ce este mutation testing?

Se introduc automat modificări mici (mutanți) în codul sursă și se verifică
dacă testele le detectează. **Mutant ucis** = testul a eșuat → testul e precis.
**Mutant supraviețuitor** = niciun test nu a sesizat modificarea.

### Rezultate mutmut 2.5.1

| Categorie | Valoare |
|---|---:|
| Mutanți verificați | 95 / 95 |
| **Killed** | **85** |
| Suspicious | 10 |
| **Survived** | **0** |
| Timeout / Skipped | 0 / 0 |

> **Suspicious ≠ Survived.** Categoria `Suspicious` înseamnă că rularea unui
> test a durat mai mult decât baseline-ul, fără timeout fatal. Rezultatul
> important este **0 survived**.

### `test_mutation.py` — 11 teste dedicate pentru mutanți neechivalenți

| Ce verifică | De ce contează |
|---|---|
| `total_cost = package_sessions × price` (nu `used_sessions × price`) | Ucide mutanții care înlocuiesc variabila din formulă |
| Discount de exact **20%** (`× 0.80`) | Ucide mutanții care schimbă valoarea constantei |
| `cancelled` **nu** consumă ședință | Ucide mutanții care incrementează `used_sessions` pentru `cancelled` |
| `no_show` blochează `completed_successfully` | Ucide mutanții care ignoră `no_show` în condiția de status |
| Mesaje de eroare stabile (verificate cu `assertRaisesRegex`) | Protejează interfața publică față de mutanți pe șiruri |
| `round(total_cost, 2)` → `0.33` pentru `price=1/3` | Ucide mutanții care elimină rotunjirea |

---

## Slide 10 – Utilizarea AI și rezultate finale

**Titlu:** Utilizarea AI și rezultate finale
**Subtitlu:** ChatGPT/Codex ca instrument de verificare · Nu înlocuiește validarea manuală

### Cum a fost utilizat AI

| Activitate | Ce a produs |
|---|---|
| Revizuirea suitei proprii | Identificarea ramurilor insuficient acoperite |
| Cazuri-limită specifice Python | `bool` vs `int`, string equality `==` vs `is` |
| Suită independentă | `teste_ai/` — 70 teste, stil diferit față de suita proprie |
| Comparație suite | Tabel cu diferențe organizare, stil, acoperire |

### Suita AI vs suita proprie

| Criteriu | Suita proprie | Suita AI |
|---|---|---|
| Număr teste | **100** | 70 |
| Organizare | pe tehnici de testare | pe scenarii și proprietăți |
| Stil | explicit, didactic | compact, parametrizat |
| Scop | demonstrarea strategiilor cerute | perspectivă independentă |

Toate propunerile AI au fost **verificate prin rulare locală** înainte de a fi incluse.

### Rezultate finale — toate metricile

| Tool | Ce măsoară | Rezultat |
|---|---|---|
| pytest | corectitudinea testelor | **100 passed** (+ 70 AI) |
| coverage.py | execuția codului | **100%** — 43 stmt · 26 branch |
| mutmut | rezistența la mutații | **85 killed · 0 survived** / 95 |

### Concluzie

Metoda `evaluate_client_package` a permis ilustrarea tuturor strategiilor
cerute: partiționare, frontiere, acoperire la trei niveluri, circuite
independente și mutation testing cu două instrumente complementare.
Rezultatele confirmă o suită stabilă și bine focalizată pe contractul public
al clasei.
