# Plan prezentare TSS - 10 slide-uri

Prezentarea este gândită ca material principal pentru susținerea orală.
README-ul rămâne documentația completă, iar slide-urile sintetizează cât mai
mult din el în limita celor 10 slide-uri cerute.

## Slide 1 - Contextul proiectului

**Titlu:** TSS T1 - Testare unitară în Python  
**Proiect:** `FitnessClassBooking`  
**Metodă testată:** `evaluate_client_package`

Informații de inclus:

- disciplina: Testarea Sistemelor Software;
- tema: T1 - testare unitară în Python;
- domeniu ales: pachete de ședințe pentru clase de fitness;
- artefacte importante: cod, teste, README, PowerPoint, capturi, loguri,
  diagrame, rezultate mutation testing.

Mesaj de susținere:

- proiectul este concentrat pe o singură funcționalitate, dar aceasta conține
  suficiente ramuri și validări pentru toate strategiile cerute.

## Slide 2 - Cerințe T1 și mapare pe implementare

Informații de inclus:

- framework folosit: `pytest`;
- strategii cerute:
  - clase de echivalență;
  - valori de frontieră;
  - coverage la nivel de instrucțiune, decizie și condiție;
  - circuite independente;
  - mutation testing;
- cerințe structurale acoperite de metodă:
  - 3 parametri;
  - buclă;
  - `if` cu `else`;
  - `if` fără `else`;
  - condiție simplă;
  - condiție compusă.

Element vizual recomandat:

- tabel „Cerință / Unde apare în cod”.

## Slide 3 - Funcționalitatea testată

Informații de inclus:

- semnătura metodei:

```python
evaluate_client_package(session_history, package_sessions, has_membership)
```

- statusuri acceptate:
  - `attended` - consumă ședință;
  - `no_show` - consumă ședință;
  - `cancelled` - nu consumă ședință;
- membership-ul aplică reducere de 20%;
- rezultate calculate:
  - contoare pentru statusuri;
  - ședințe consumate și rămase;
  - cost total;
  - status final.

Element vizual recomandat:

- tabel cu statusurile și efectul fiecăruia.

## Slide 4 - Validări și reguli de business

Informații de inclus:

- constructor:
  - `class_name` în `{dance, pilates, yoga, zumba}`;
  - `instructor` șir nevid după `strip()`;
  - `price_per_session` număr pozitiv, `bool` respins explicit;
- metodă:
  - `session_history` trebuie să fie listă;
  - `package_sessions` trebuie să fie `int` între 1 și 20;
  - `has_membership` trebuie să fie strict `bool`;
  - statusurile necunoscute produc `ValueError`;
  - consumul nu poate depăși numărul de ședințe din pachet.

Mesaj de susținere:

- validarea separată a lui `bool` este necesară deoarece în Python `bool` este
  subclasă de `int`.

## Slide 5 - Proiectarea suitei principale de teste

Informații de inclus:

| Fișier | Strategie | Nr. teste |
| --- | --- | ---: |
| `test_equivalence_partitioning.py` | clase de echivalență | 22 |
| `test_boundary_value_analysis.py` | valori de frontieră | 16 |
| `test_coverage.py` | instrucțiune / decizie / condiție | 40 |
| `test_independent_circuits.py` | circuite independente | 10 |
| `test_mutation.py` | teste orientate pe mutanți | 11 |

Mesaj de susținere:

- suita principală are 99 de teste și este organizată explicit după tehnicile
  cerute în tema T1.

## Slide 6 - Testare funcțională: echivalență și frontiere

Informații de inclus:

- clase valide:
  - istoric gol;
  - istoric mixt;
  - pachet activ;
  - pachet finalizat cu succes;
  - pachet finalizat cu absențe;
  - membership activ/inactiv;
- clase invalide:
  - tipuri greșite;
  - status necunoscut;
  - pachet în afara intervalului;
  - consum peste pachet;
- frontiere:
  - `0`, `1`, `2`;
  - `19`, `20`, `21`;
  - preț zero, negativ și pozitiv foarte mic.

Element vizual recomandat:

- bandă cu valorile `0 1 2 19 20 21`.

## Slide 7 - Testare structurală, CFG și coverage

Informații de inclus:

- ramuri acoperite:
  - validări de intrare;
  - status invalid;
  - `attended`;
  - `no_show`;
  - `cancelled`;
  - membership;
  - status final;
  - depășire pachet;
- diagrame:
  - `cfg_diagrama.drawio.png`;
  - `cause_effect_graph.png`;
- rezultat coverage:
  - 43 statements;
  - 0 missing;
  - 26 branches;
  - 0 partial branches;
  - 100% coverage.

Element vizual recomandat:

- captură `03_coverage_report_100_percent.png` și una dintre diagrame.

## Slide 8 - Mutation testing: mutmut și Cosmic Ray

Informații de inclus:

- `mutmut`:
  - 95/95 mutanți verificați;
  - 80 killed;
  - 15 suspicious;
  - 0 survived;
  - 0 timeout, 0 skipped;
- `Cosmic Ray`:
  - 166 mutanți finalizați;
  - 9 survived;
  - rată supraviețuire 5.42%;
  - scor aproximativ 94.58%;
- interpretare:
  - `Suspicious` în mutmut nu este același lucru cu `Survived`;
  - Cosmic Ray are operatori diferiți, deci oferă o verificare complementară.

Element vizual recomandat:

- captura `05_mutmut_run.png`;
- tabel comparativ mutmut / Cosmic Ray.

## Slide 9 - Utilizarea AI și comparația suitei AI

Informații de inclus:

- ChatGPT/Codex a fost utilizat ca instrument de analiză și verificare;
- suita AI este separată în `teste_ai/`;
- rezultat: 70 teste trecute;
- comparație:
  - suita proprie: 99 teste, organizată pe tehnici;
  - suita AI: 70 teste, organizată pe scenarii, validări și proprietăți;
- exemple relevante:
  - `bool` vs `int`;
  - string equality vs identitate;
  - statusuri construite dinamic;
  - scenarii agregate cu `dataclass`.

Element vizual recomandat:

- captura `07_pytest_ai_70_passed.png`;
- tabel „Suita proprie / Suita AI”.

## Slide 10 - Rezultate finale și livrabile

Informații de inclus:

- rezultate:
  - `99 passed` în suita principală;
  - `70 passed` în suita AI;
  - `100%` coverage;
  - `0` mutanți `survived` în mutmut;
  - `94.58%` scor aproximativ Cosmic Ray;
- livrabile:
  - `README.md` - documentația completă;
  - `TSS_T1_FitnessClassBooking.pptx` - prezentarea;
  - `screenshots/`, `logs/`, `cosmic_ray/`;
  - diagramele finale;
  - înregistrarea de ecran pentru demo.

Mesaj final:

- proiectul respectă cerința T1 și combină testare funcțională, structurală,
  mutation testing și analiză asistată de AI.
