# Plan prezentare TSS - 10 slide-uri

Prezentarea PowerPoint trebuie să fie un rezumat al documentației din
`README.md`. Fiecare slide are rolul de a susține oral proiectul, nu de a copia
integral documentația.

## Slide 1 - Titlu și context

**Titlu:** TSS T1 - Testare unitară în Python  
**Proiect:** FitnessClassBooking  
**Funcționalitate testată:** evaluarea unui pachet de ședințe fitness

Conținut recomandat:

- disciplina: Testarea Sistemelor Software;
- tema: T1 - testare unitară în Python;
- clasa testată: `FitnessClassBooking`;
- metoda principală: `evaluate_client_package`.

## Slide 2 - Cerință și alegerea funcționalității

Conținut recomandat:

- framework de testare unitară în Python: `pytest`;
- strategii cerute: echivalență, frontiere, coverage, circuite independente,
  mutation testing;
- metoda are 3 parametri, buclă, `if` cu `else`, `if` fără `else`, condiție
  simplă și condiție compusă;
- domeniu ales: pachet de ședințe pentru o clasă de fitness.

Mesaj oral:

- proiectul este concentrat pe o singură metodă, dar metoda este suficient de
  complexă pentru toate strategiile.

## Slide 3 - Modelul de business

Conținut recomandat:

- statusuri în istoric:
  - `attended` consumă ședință;
  - `no_show` consumă ședință;
  - `cancelled` nu consumă ședință;
- membership-ul aplică reducere de `20%`;
- status final:
  - `active`;
  - `completed_successfully`;
  - `completed_with_absences`.

Element vizual:

- tabel scurt cu cele trei statusuri și efectul fiecăruia.

## Slide 4 - Structura metodei și validări

Conținut recomandat:

- semnătura metodei:

```python
evaluate_client_package(session_history, package_sessions, has_membership)
```

- validări:
  - `session_history` trebuie să fie listă;
  - `package_sessions` trebuie să fie `int` între `1` și `20`;
  - `has_membership` trebuie să fie `bool`;
  - fiecare status trebuie să fie valid;
  - consumul nu poate depăși pachetul.

Mesaj oral:

- `bool` este tratat separat deoarece în Python este subclasă de `int`.

## Slide 5 - Testare funcțională

Conținut recomandat:

- `test_equivalence_partitioning.py`: 22 teste;
- `test_boundary_value_analysis.py`: 16 teste;
- clase valide: istoric gol, istoric mixt, pachet finalizat, membership;
- clase invalide: tipuri greșite, status necunoscut, consum peste pachet;
- frontiere: `0`, `1`, `2`, `19`, `20`, `21`.

Element vizual:

- tabel cu fișierele și numărul de teste.

## Slide 6 - Testare structurală și diagrame

Conținut recomandat:

- `test_coverage.py`: 40 teste;
- `test_independent_circuits.py`: 10 teste;
- acoperire urmărită: instrucțiune, decizie, condiție;
- circuite independente pentru drumurile principale;
- diagrame:
  - `cfg_diagrama.drawio.png`;
  - `cause_effect_graph.png`.

Element vizual:

- diagrama CFG sau un crop/rezumat al acesteia.

## Slide 7 - Coverage: rezultat 100%

Conținut recomandat:

- comandă:

```bash
python -m coverage report -m --include="fitness_class_booking.py"
```

- rezultat:
  - `43` statements;
  - `0` missing;
  - `26` branches;
  - `0` partial branches;
  - `100%` coverage.

Mesaj oral:

- coverage-ul arată că toate instrucțiunile și ramurile au fost executate, dar
  de aceea a fost folosit și mutation testing.

## Slide 8 - Mutation testing: mutmut și Cosmic Ray

Conținut recomandat:

- `test_mutation.py`: 11 teste;
- `mutmut`:
  - `95/95` mutanți verificați;
  - `80` killed;
  - `15` suspicious;
  - `0` survived;
- Cosmic Ray:
  - `166` mutanți finalizați;
  - `9` survived;
  - scor aproximativ `94.58%`.

Mesaj oral:

- `Suspicious` în mutmut nu înseamnă `Survived`;
- Cosmic Ray folosește operatori diferiți și oferă o perspectivă suplimentară.

## Slide 9 - Suita AI și comparația cu suita proprie

Conținut recomandat:

- AI folosit: ChatGPT/Codex;
- suita AI este separată în `teste_ai/`;
- rezultat: `70 passed`;
- comparație:
  - suita proprie: 99 teste, organizată pe tehnici;
  - suita AI: 70 teste, organizată pe scenarii și proprietăți;
  - AI-ul a ajutat la cazuri precum `bool` vs `int` și string equality.

Mesaj oral:

- AI-ul a fost folosit ca instrument de analiză și completare, iar rezultatele
  au fost validate prin rularea testelor.

## Slide 10 - Rezultate finale și concluzie

Conținut recomandat:

- `99 passed` în suita principală;
- `70 passed` în suita AI;
- `100%` coverage pe `fitness_class_booking.py`;
- `0` mutanți supraviețuitori în mutmut;
- `94.58%` scor aproximativ Cosmic Ray;
- documentația completă este în `README.md`;
- proiectul este pregătit pentru demonstrația video.

Mesaj final:

- metoda este compactă, dar acoperă toate cerințele;
- testele combină testare funcțională, structurală și mutation testing;
- README-ul conține documentația completă și referințele.
