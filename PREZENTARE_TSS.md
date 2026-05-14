# Prezentare TSS - FitnessClassBooking

## Slide 1 - Titlu

T1 Testare unitara in Python  
Clasa: `FitnessClassBooking`  
Metoda testata: `evaluate_client_package`

## Slide 2 - Cerinta proiectului

- testarea unei clase Python cu framework de testare unitara;
- aplicarea strategiilor de testare functionala si structurala;
- cerinta suplimentara: metoda cu minim 3 parametri, bucla, doua conditionale,
  conditie simpla si conditie compusa.

## Slide 3 - De ce am refacut proiectul

- varianta initiala avea prea multe metode testate separat;
- noua varianta se concentreaza pe o singura functionalitate;
- metoda noua este realista pentru o aplicatie de fitness.

## Slide 4 - Functionalitatea aleasa

Metoda evalueaza pachetul de sedinte al unui client.

Statusuri:

- `attended`: sedinta consumata;
- `no_show`: sedinta consumata;
- `cancelled`: sedinta neconsumata.

## Slide 5 - Semnatura metodei

```python
evaluate_client_package(session_history, package_sessions, has_membership)
```

Parametri:

- `session_history`;
- `package_sessions`;
- `has_membership`.

## Slide 6 - Reguli de business

- `attended` si `no_show` consuma sedinte;
- `cancelled` nu consuma sedinte;
- membership aplica reducere de 20%;
- statusul poate fi `active`, `completed_successfully`,
  `completed_with_absences`.

## Slide 7 - Cerinta profesoarei bifata

| Cerinta | Implementare |
| --- | --- |
| 3 parametri | `session_history`, `package_sessions`, `has_membership` |
| bucla | `for session_status in session_history` |
| if cu else | statusul `attended` vs celelalte |
| if fara else | `if has_membership` |
| conditie simpla | `has_membership` |
| conditie compusa | `remaining_sessions == 0 and no_show == 0` |

## Slide 8 - Testare functionala

Partitionare in clase de echivalenta:

- istoric valid gol;
- istoric valid mixt;
- pachet finalizat cu succes;
- pachet finalizat cu absente;
- tipuri invalide;
- status invalid;
- sedinte consumate peste pachet.

## Slide 9 - Valori de frontiera

Frontiere testate:

- `package_sessions = 0`, `1`, `2`;
- `package_sessions = 19`, `20`, `21`;
- o sedinta inainte de finalizare;
- exact la finalizare;
- peste limita pachetului.

## Slide 10 - Testare structurala

Au fost urmarite:

- statement coverage;
- decision coverage;
- condition coverage;
- circuite independente.

## Slide 11 - CFG

Diagrama CFG:

- `evaluate_client_package_cfg.drawio.png`
- `evaluate_client_package_cfg.drawio.svg`

Decizii principale:

- validarea parametrilor;
- validarea statusului;
- ramura `attended`;
- verificarea depasirii pachetului;
- membership;
- status final cu succes.

## Slide 12 - Coverage

Rezultat:

```text
fitness_class_booking.py: 100%
43 statements, 0 missing
26 branches, 0 partial
```

## Slide 13 - Mutmut

Rezultat:

- 95 mutanti verificati;
- 80 mutanti omorati;
- 0 mutanti supravietuitori;
- 15 mutanti suspiciosi;
- 0 timeout, 0 skipped.

Teste suplimentare:

- multiple `attended`;
- multiple `no_show`;
- multiple `cancelled`;
- cost calculat pe pachetul complet;
- discount membership;
- rotunjire cost;
- mesaje publice de eroare.

## Slide 14 - Rezultate finale

- 99 teste;
- toate trec;
- 100% coverage pe fisierul principal;
- 43 statements, 0 missing;
- 26 branches, 0 partial;
- 0 mutanti supravietuitori;
- capturi finale disponibile in `screenshots/`;
- proiect mai simplu si mai usor de prezentat.

## Slide 15 - Concluzie

Noua varianta este mai potrivita pentru cerinta: o singura metoda realista,
suficient de complexa pentru toate strategiile de testare, dar fara sa incarce
proiectul cu functionalitati secundare.
