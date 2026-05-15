# TSS T1 - Testare unitară în Python

Lucrare realizată pentru disciplina **Testarea Sistemelor Software**, tema
**T1 - Testare unitară în Python**.

Obiectul testării este clasa `FitnessClassBooking`, care modelează evaluarea
unui pachet de ședințe pentru o clasă de fitness. Funcționalitatea principală
analizată este metoda:

```python
evaluate_client_package(session_history, package_sessions, has_membership)
```

Acest fișier constituie documentația completă a proiectului. Sunt prezentate
cerința, modelul funcțional, strategiile de testare, diagramele, configurația
hardware/software, comenzile de rulare, rezultatele obținute, interpretarea
instrumentelor utilizate și comparația dintre suita proprie de teste și suita
generată/asistată cu ajutorul unui instrument AI.

## 1. Cerința proiectului

Conform temei T1, proiectul trebuie să folosească un framework de testare
unitară din Python și să ilustreze strategiile de generare a testelor discutate
la curs:

- partiționare în clase de echivalență;
- analiza valorilor de frontieră;
- acoperire la nivel de instrucțiune;
- acoperire la nivel de decizie;
- acoperire la nivel de condiție;
- circuite independente;
- analiză pe baza unui generator de mutanți;
- teste suplimentare pentru omorârea unor mutanți neechivalenți.

Proiectul conține și elementele cerute pentru documentare:

- cod sursă și teste unitare;
- README cu documentație completă;
- diagrame realizate cu tool dedicat;
- capturi de ecran cu rularea testelor și rezultatele tool-urilor;
- comparații și interpretări ale rezultatelor;
- secțiune despre utilizarea unui tool AI în testare;
- prezentare PowerPoint de maximum 10 slide-uri.

## 2. Ideea aplicației

Domeniul ales este o aplicație de fitness. Clasa `FitnessClassBooking`
evaluează starea unui pachet de ședințe cumpărat de un client.

Un client poate avea în istoricul ședințelor trei tipuri de status:

| Status | Semnificație | Consumă ședință? |
| --- | --- | --- |
| `attended` | clientul a participat la ședință | da |
| `no_show` | clientul nu s-a prezentat și nu a anunțat | da |
| `cancelled` | clientul a anulat la timp | nu |

Metoda calculează:

- numărul de ședințe participate;
- numărul de absențe de tip `no_show`;
- numărul de anulări;
- numărul de ședințe consumate;
- numărul de ședințe rămase;
- costul total al pachetului;
- statusul final al pachetului.

Statusul final poate fi:

- `active` - pachetul mai are ședințe disponibile;
- `completed_successfully` - pachetul este terminat fără `no_show`;
- `completed_with_absences` - pachetul este terminat, dar există cel puțin un
  `no_show`.

## 3. Clasa testată

Fișier principal:

```text
fitness_class_booking.py
```

Interfața clasei:

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

Constructorul validează:

| Parametru | Regulă |
| --- | --- |
| `class_name` | trebuie să fie unul dintre `dance`, `pilates`, `yoga`, `zumba` |
| `instructor` | trebuie să fie șir nevid după aplicarea `strip()` |
| `price_per_session` | trebuie să fie număr pozitiv; valorile `bool` sunt respinse explicit |

Metoda `evaluate_client_package` validează:

| Parametru | Regulă |
| --- | --- |
| `session_history` | trebuie să fie listă |
| `package_sessions` | trebuie să fie `int`, între `1` și `20`; valorile `bool` sunt respinse explicit |
| `has_membership` | trebuie să fie strict `bool` |
| fiecare status din istoric | trebuie să fie `attended`, `no_show` sau `cancelled` |

O regulă importantă a implementării este validarea separată a tipului `bool`.
În Python, `bool` este subclasă de `int`, deci `True` și `False` pot trece prin
validări numerice dacă nu sunt respinse explicit [5].

## 4. Exemplu de utilizare

```python
booking = FitnessClassBooking("yoga", "Ana Pop", 50)

result = booking.evaluate_client_package(
    ["attended", "attended", "cancelled", "no_show"],
    5,
    True,
)
```

Rezultatul este:

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

Explicație:

- `attended` și `no_show` consumă ședințe, deci sunt consumate `3` ședințe;
- `cancelled` este numărat, dar nu consumă ședință;
- pachetul are `5` ședințe, deci rămân `2`;
- costul inițial este `5 * 50 = 250`;
- clientul are membership, deci se aplică reducerea de `20%`;
- costul final este `250 * 0.8 = 200`.

## 5. Cerințe structurale acoperite de metodă

Metoda principală a fost aleasă astfel încât să conțină explicit elementele
necesare pentru testare structurală.

| Cerință | Unde apare în cod |
| --- | --- |
| minimum 3 parametri | `session_history`, `package_sessions`, `has_membership` |
| instrucțiune repetitivă | `for session_status in session_history` |
| `if` cu `else` | `if session_status == "attended": ... else: ...` |
| `if` fără `else` | `if has_membership: ...` |
| condiție simplă | `if has_membership` |
| condiție compusă | `remaining_sessions == 0 and no_show == 0` |

Această structură permite aplicarea tehnicilor de acoperire la nivel de
instrucțiune, decizie, condiție și circuite independente [6][7].

## 6. Configurație hardware și software

Configurația folosită pentru rulările finale:

| Componentă | Valoare |
| --- | --- |
| Laptop | HP Laptop 15s-fq2xxx |
| Memorie RAM | aproximativ 16 GB |
| Sistem de operare principal | Windows 11 Pro, 64-bit |
| Python pe Windows | Python 3.13.3 |
| Framework testare | pytest 9.0.3 [1] |
| Coverage | coverage.py 7.13.5 [2] |
| WSL pentru mutation testing | Ubuntu 24.04.1 LTS |
| Python în WSL | Python 3.12.3 |
| Mutmut în WSL | mutmut 2.5.1 [3] |
| Cosmic Ray | folosit ca analiză suplimentară; artefactele sunt în `cosmic_ray/` [4] |

Nu a fost folosită o mașină virtuală completă pentru proiect. Pentru `mutmut`
a fost folosit WSL, deoarece în mediul curent `mutmut` nu rulează nativ pe
Windows. Testele obișnuite și coverage-ul au fost rulate pe Windows.

## 7. Structura proiectului

```text
TSS_Proiect/
|-- fitness_class_booking.py
|-- test_equivalence_partitioning.py
|-- test_boundary_value_analysis.py
|-- test_coverage.py
|-- test_independent_circuits.py
|-- test_mutation.py
|-- teste_ai/
|   |-- test_ai_generated_booking.py
|   |-- test_ai_equivalence_and_validation.py
|   |-- test_ai_boundary_and_structural.py
|   `-- test_ai_paths_and_mutation_focus.py
|-- cfg_diagrama.drawio.png
|-- cause_effect_graph.png
|-- cosmic_ray/
|-- logs/
|-- screenshots/
|-- run_coverage.sh
|-- pytest.ini
|-- PREZENTARE_TSS.md
|-- TSS_T1_FitnessClassBooking.pptx
`-- README.md
```

Fișierul `pytest.ini` limitează rularea implicită `python -m pytest -q` la
suita principală de teste, astfel încât testele generate/asistate de AI din
`teste_ai/` pot fi rulate separat.

## 8. Strategii de testare

Suita principală are **100 de teste** și este împărțită pe tehnicile cerute.
Testarea este făcută cu `pytest`, un framework de testare unitară pentru Python
[1].

| Fișier | Strategie | Nr. teste | Rol |
| --- | --- | ---: | --- |
| `test_equivalence_partitioning.py` | partiționare în clase de echivalență | 23 | verifică domenii valide/invalide pentru constructor și metodă |
| `test_boundary_value_analysis.py` | valori de frontieră | 16 | verifică limitele `1`, `20`, prețuri minime și depășiri |
| `test_coverage.py` | acoperire instrucțiune/decizie/condiție | 40 | urmărește execuția tuturor ramurilor relevante |
| `test_independent_circuits.py` | circuite independente | 10 | verifică drumuri reprezentative prin fluxul metodei |
| `test_mutation.py` | teste orientate pe mutanți | 11 | întărește suita pentru mutation testing |

### 8.1 Partiționare în clase de echivalență

Clase valide:

- `class_name` valid: `dance`, `pilates`, `yoga`, `zumba`;
- instructor text nevid;
- preț pozitiv;
- istoric gol sau cu statusuri valide;
- pachet între `1` și `20`;
- `has_membership` strict boolean.

Pentru `class_name`, valorile permise formează un set enumerat. Din acest motiv,
testele includ și un caz explicit pentru `zumba`, adăugat după rularea mutation
testing, astfel încât mutațiile asupra literalilor validați să fie detectate.

Clase invalide:

- `class_name` necunoscut sau de alt tip;
- instructor gol, doar spații sau non-string;
- preț negativ, zero, `bool` sau non-numeric;
- `session_history` non-listă;
- `package_sessions` sub `1`, peste `20`, `bool`, `float` sau non-numeric;
- `has_membership` non-boolean;
- status necunoscut în istoric;
- istoric care consumă mai multe ședințe decât conține pachetul.

### 8.2 Analiza valorilor de frontieră

Frontiere urmărite:

| Element | Valori testate |
| --- | --- |
| număr minim de ședințe | `0`, `1`, `2` |
| număr maxim de ședințe | `19`, `20`, `21` |
| consum exact | număr de `attended`/`no_show` egal cu pachetul |
| depășire consum | istoric care consumă peste pachet |
| preț | `0`, valori mici pozitive, valori negative |

Valorile `0`, `21`, `False` sau `True` pentru `package_sessions` trebuie să
producă `ValueError("invalid package data")`.

### 8.3 Acoperire structurală

Pentru acoperirea structurală s-a urmărit ca fiecare instrucțiune și fiecare
ramură importantă să fie executată:

- validarea constructorului;
- validarea parametrilor metodei;
- validarea fiecărui status din listă;
- ramura `attended`;
- ramura `no_show`;
- ramura `cancelled`;
- ramura de depășire a pachetului;
- ramura cu membership;
- ramura fără membership;
- status final `active`;
- status final `completed_successfully`;
- status final `completed_with_absences`.

### 8.4 Circuite independente

Testele pentru circuite independente urmăresc drumuri distincte prin metoda
`evaluate_client_package`, de exemplu:

- istoric valid gol;
- istoric cu o ședință participată;
- istoric cu anulări;
- istoric mixt;
- pachet finalizat fără absențe;
- pachet finalizat cu absențe;
- date invalide la intrare;
- status invalid în timpul buclei;
- consum peste limita pachetului.

### 8.5 Mutation testing

Pentru mutation testing au fost folosite două perspective:

- `mutmut`, ca tool principal de analiză a mutanților [3];
- `Cosmic Ray`, ca analiză suplimentară independentă [4].

Testele din `test_mutation.py` verifică explicit comportamente care pot omorî
mutanți neechivalenți:

- costul se calculează pe pachetul complet, nu pe ședințele folosite;
- membership aplică reducere de `20%`;
- `attended`, `no_show` și `cancelled` sunt tratate diferit;
- `cancelled` nu consumă ședințe;
- statusul final depinde de `remaining_sessions` și `no_show`;
- mesajele publice de eroare rămân stabile.

## 9. Diagrame

Proiectul include două diagrame finale, realizate cu tool dedicat:

| Diagramă | Fișier | Rol |
| --- | --- | --- |
| Control Flow Graph | `cfg_diagrama.drawio.png` | arată fluxul metodei `evaluate_client_package` |
| Cause-Effect Graph | `cause_effect_graph.png` | arată legătura dintre condiții, reguli de business și rezultate |

Diagrama CFG evidențiază:

- validarea parametrilor;
- bucla prin `session_history`;
- decizia pentru `attended`;
- deciziile pentru `no_show` și `cancelled`;
- verificarea depășirii pachetului;
- calculul costului;
- aplicarea discountului;
- decizia finală de status.

Graful cauză-efect evidențiază relațiile dintre:

- tipurile de status din istoric;
- numărul de ședințe consumate;
- existența membership-ului;
- costul final;
- statusul final al pachetului.

## 10. Comenzi de rulare

Instalarea dependențelor principale:

```bash
python -m pip install pytest coverage "mutmut<3"
```

Rularea suitei principale:

```bash
python -m pytest -q
```

Rularea suitei AI:

```bash
python -m pytest -q teste_ai
```

Rularea coverage:

```bash
python -m coverage run --branch -m pytest -q
python -m coverage report -m --include="fitness_class_booking.py"
python -m coverage html --include="fitness_class_booking.py"
```

Rularea `mutmut` în WSL:

```bash
python -m mutmut run --paths-to-mutate fitness_class_booking.py \
  --tests-dir . \
  --runner "python -m pytest -q test_equivalence_partitioning.py test_boundary_value_analysis.py test_coverage.py test_independent_circuits.py test_mutation.py"
python -m mutmut results
```

Scriptul `run_coverage.sh` poate automatiza rularea testelor și salvarea
output-urilor în `logs/`:

```bash
bash run_coverage.sh
```

Variabile utile:

```bash
RUN_MUTMUT=0 bash run_coverage.sh
RUN_MUTMUT=1 bash run_coverage.sh
RUN_MUTMUT=auto bash run_coverage.sh
```

## 11. Rezultate finale

### 11.1 Pytest

Rulare:

```bash
python -m pytest -q
```

Rezultat:

```text
100 passed
```

Interpretare: toate testele din suita principală trec, iar comportamentul
implementat este stabil pentru cazurile funcționale, structurale și de mutație
testate.

### 11.2 Coverage.py

Rulare:

```bash
python -m coverage run --branch -m pytest -q
python -m coverage report -m --include="fitness_class_booking.py"
```

Rezultat:

```text
Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
fitness_class_booking.py      43      0     26      0   100%
----------------------------------------------------------------------
TOTAL                         43      0     26      0   100%
```

Interpretare:

- toate cele `43` de instrucțiuni sunt acoperite;
- toate cele `26` de ramuri sunt acoperite;
- nu există ramuri parțial acoperite;
- coverage-ul este `100%` pentru fișierul principal.

Coverage-ul de 100% nu demonstrează singur că testele sunt perfecte, dar arată
că suita execută toate zonele importante din cod [2].

### 11.3 Mutmut

Rezultat final:

```text
95/95 mutanți verificați
Killed: 85
Timeout: 0
Suspicious: 10
Survived: 0
Skipped: 0
```

Interpretare:

- `85` de mutanți au fost omorâți de teste;
- nu există mutanți în categoria `Survived`;
- cei `10` mutanți `Suspicious` nu sunt echivalenți cu `Survived`;
- categoria `Suspicious` indică rulări mai lente decât baseline-ul, dar fără
  timeout fatal.

Pentru proiect, rezultatul `0 survived` în `mutmut` este un indicator bun al
puterii suitei principale.

### 11.4 Cosmic Ray

Rezultat:

```text
Mutanți generați/finalizați: 166
Mutanți supraviețuitori: 9
Rată supraviețuire: 5.42%
Scor aproximativ omorâre mutanți: 94.58%
```

Interpretare:

- Cosmic Ray a generat mai multe mutații decât `mutmut`;
- au rămas `9` mutanți supraviețuitori;
- o parte sunt mutații foarte apropiate de comportamentul original pe domeniul
  valid al metodei;
- diferența dintre `mutmut` și Cosmic Ray arată că tool-urile de mutation
  testing pot avea operatori și clasificări diferite.

Artefactele Cosmic Ray sunt păstrate în:

```text
cosmic_ray/
```

## 12. Comparație între tool-uri

| Tool | Ce măsoară | Rezultat | Interpretare |
| --- | --- | --- | --- |
| `pytest` | dacă aserțiunile trec | `100 passed` | suita principală este stabilă |
| `coverage.py` | execuția instrucțiunilor și ramurilor | `100%` | codul principal este acoperit complet |
| `mutmut` | rezistența testelor la mutații | `85 killed`, `0 survived` | testele detectează mutațiile neechivalente generate de mutmut |
| `Cosmic Ray` | mutation testing cu alți operatori | `94.58%` scor aproximativ | confirmă robustețea generală, dar arată câțiva mutanți rămași |

Concluzie: coverage-ul confirmă execuția codului, iar mutation testing-ul
verifică dacă testele sunt suficient de precise pentru a detecta modificări
greșite ale comportamentului [2][3][4].

## 13. Capturi de ecran și loguri

Capturile existente sunt în folderul `screenshots/`. Primele două capturi și
captura `mutmut` au fost făcute înainte de adăugarea testului explicit pentru
`zumba`, deci rezultatele curente sunt notate în tabel:

| Fișier | Conținut |
| --- | --- |
| `01_pytest_99_passed.png` | captură veche pytest; după testul `zumba`, rezultatul curent este `100 passed` |
| `02_coverage_run_99_passed.png` | captură veche coverage; după testul `zumba`, rezultatul curent este `100 passed` |
| `03_coverage_report_100_percent.png` | raport coverage cu `100%` pe `fitness_class_booking.py` |
| `04_coverage_html_generated.png` | generarea raportului HTML coverage |
| `05_mutmut_run.png` | sumar mutmut anterior; rezultatul curent este `95` mutanți, `85 killed`, `10 suspicious`, `0 survived` |
| `06_mutmut_results.png` | lista mutanților `Suspicious` raportați de mutmut |
| `07_pytest_ai_70_passed.png` | rulare `python -m pytest -q teste_ai` cu `70 passed` |

Output-urile text sunt în folderul `logs/`:

| Fișier | Conținut |
| --- | --- |
| `logs/pytest_output.txt` | output pentru pytest, coverage și mutmut |
| `logs/coverage_report.txt` | raport coverage |
| `logs/mutmut_results.txt` | output mutmut run + results |

## 14. Utilizarea unui instrument AI în proiect

În etapa de analiză și extindere a testelor a fost utilizat ChatGPT/Codex ca
instrument de asistență pentru testarea software [8]. Utilizarea acestuia a
vizat activități de verificare și comparare, nu înlocuirea procesului de
validare. Concret, instrumentul a fost folosit pentru:

- revizuirea suitei proprii de teste;
- identificarea unor cazuri-limită sau ramuri insuficient evidențiate;
- propunerea unor teste suplimentare;
- construirea unei suite independente în folderul `teste_ai/`;
- compararea suitei proprii cu suita generată/asistată;
- formularea interpretării rezultatelor obținute prin coverage și mutation
  testing.

Propunerile obținute prin AI au fost păstrate numai după verificare locală.
Validarea finală a fost făcută prin rularea testelor, nu prin acceptarea
automată a răspunsurilor generate.

### 14.1 Prompturi reprezentative

Prompturile de mai jos sunt reformulări sintetice ale solicitărilor folosite în
timpul lucrului. Ele descriu tipul de cerințe transmise instrumentului AI, nu un
transcript complet al interacțiunii:

1. `Analizează proiectul FitnessClassBooking și verifică dacă testele acoperă toate ramurile, condițiile și cazurile invalide.`
2. `Completează test_coverage.py cu testele lipsă, păstrând stilul fișierului.`
3. `Verifică test_boundary_value_analysis.py și test_equivalence_partitioning.py în același mod.`
4. `Verifică test_mutation.py și propune teste care ar putea omorî mutanți neechivalenți.`
5. `Generează o suită separată în teste_ai/ care să arate diferit de testele scrise manual, dar să fie corectă.`
6. `Compară suita proprie cu suita AI și explică diferențele relevante pentru raport.`

### 14.2 Suita AI

Suita AI este în folderul `teste_ai/` și conține **70 de teste**.

| Fișier | Nr. teste | Stil |
| --- | ---: | --- |
| `test_ai_generated_booking.py` | 13 | scenarii de business cu `dataclass` |
| `test_ai_equivalence_and_validation.py` | 21 | parametrizări pentru echivalență și validare |
| `test_ai_boundary_and_structural.py` | 22 | limite, ramuri structurale și rotunjire |
| `test_ai_paths_and_mutation_focus.py` | 14 | proprietăți, drumuri și cazuri orientate pe mutații |

Rulare:

```bash
python -m pytest -q teste_ai
```

Rezultat:

```text
70 passed
```

### 14.3 Comparație între suita proprie și suita AI

| Criteriu | Suita proprie | Suita AI |
| --- | --- | --- |
| Număr teste | 100 | 70 |
| Organizare | pe tehnici de testare | pe scenarii, validări, limite și proprietăți |
| Stil | explicit, didactic, ușor de corelat cu cerința | compact, parametrizat, orientat pe scenarii |
| Scop | demonstrarea strategiilor cerute la curs | perspectivă suplimentară și scenarii alternative |
| Coverage | 100% pe `fitness_class_booking.py` | confirmă comportamentul, dar este rulată separat |
| Mutation focus | fișier dedicat `test_mutation.py` | teste suplimentare pentru egalitate de stringuri, bool și proprietăți |

### 14.4 Studiu de caz: `bool` față de `int`

Analiza asistată a evidențiat un detaliu specific limbajului Python: `bool`
este subclasă de `int` [5]. Din acest motiv, testele verifică explicit că:

- `price_per_session=False` este invalid;
- `package_sessions=True` este invalid;
- `package_sessions=False` este invalid;
- `has_membership=1` este invalid.

Acest tip de caz este important deoarece poate trece neobservat dacă se testează
doar valori invalide evidente, precum stringuri sau valori negative.

### 14.5 Studiu de caz: egalitatea stringurilor

Suita AI include testul:

```python
test_ai_mutation_status_matching_uses_value_equality_for_dynamic_strings
```

Acesta construiește statusurile prin operații de string și verifică faptul că
metoda le compară prin valoare, nu prin identitate. Testul este util pentru
mutanți care ar înlocui `==` cu `is`.

### 14.6 Concluzie privind utilizarea AI

Contribuția instrumentului AI a fost relevantă în special pentru:

- identificarea unor cazuri specifice limbajului Python;
- obținerea unei perspective independente asupra suitei de teste;
- generarea unor teste orientate pe mutații;
- structurarea comparației dintre suita proprie și suita AI.

Limitarea principală observată este dependența de contextul furnizat. Dacă
promptul este incomplet, instrumentul poate presupune detalii care nu există în
implementarea reală. Din acest motiv, documentația și testele finale includ doar
informații confirmate prin cod și prin rulări locale.

## 15. Materiale pentru predare

Materialele importante pentru predare sunt:

- `README.md` - documentația completă a proiectului;
- `TSS_T1_FitnessClassBooking.pptx` - prezentarea PowerPoint de 10 slide-uri;
- `PREZENTARE_TSS.md` - planul textual al celor 10 slide-uri;
- `fitness_class_booking.py` - clasa testată;
- fișierele `test_*.py` - suita principală de teste;
- folderul `screenshots/` - capturi cu rulările finale;
- folderul `logs/` - output-uri text;
- folderul `cosmic_ray/` - artefacte pentru analiza Cosmic Ray;
- `cfg_diagrama.drawio.png` și `cause_effect_graph.png` - diagramele finale.

## 16. Concluzie

Proiectul respectă cerința temei T1 prin testarea unei clase Python cu o suită
unitară organizată pe tehnicile studiate la curs și la laborator. Funcționalitatea
aleasă are un domeniu redus, dar include validări, ramuri și rezultate suficient
de variate pentru a demonstra atât testarea funcțională, cât și testarea
structurală.

Rezultatele finale sunt:

- `100` teste în suita principală;
- `70` teste în suita AI;
- `100%` statement coverage;
- `100%` branch coverage pentru fișierul principal;
- `0` mutanți supraviețuitori în `mutmut`;
- scor aproximativ de omorâre a mutanților de `94.58%` în Cosmic Ray.

Metoda `evaluate_client_package` permite verificarea coerentă a claselor de
echivalență, a valorilor de frontieră, a acoperirii codului, a circuitelor
independente și a comportamentului în fața mutațiilor. Rezultatele obținute
indică o suită stabilă și bine focalizată pe contractul public al clasei.

## 17. Referințe bibliografice

[1] Pytest Development Team, pytest documentation, https://docs.pytest.org/,
Data ultimei accesări: 14 mai 2026.

[2] Batchelder, Ned, coverage.py documentation, https://coverage.readthedocs.io/,
Data ultimei accesări: 14 mai 2026.

[3] Hovmöller, Anders, mutmut documentation, https://mutmut.readthedocs.io/,
Data ultimei accesări: 14 mai 2026.

[4] Cosmic Ray Contributors, Cosmic Ray documentation,
https://cosmic-ray.readthedocs.io/, Data ultimei accesări: 14 mai 2026.

[5] Python Software Foundation, Boolean Type - bool,
https://docs.python.org/3/library/stdtypes.html#boolean-type-bool,
Data ultimei accesări: 14 mai 2026.

[6] Aniche, Maurício, Effective Software Testing: A developer's guide,
Simon and Schuster, 2022.

[7] Khorikov, Vladimir, Unit Testing Principles, Practices, and Patterns,
Simon and Schuster, 2020.

[8] OpenAI, ChatGPT, https://chatgpt.com/, Data generării: 14 mai 2026.
