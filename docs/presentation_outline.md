# Outline Prezentare – TSS T1: Testare Unitara in Python

**Durata estimata:** 10-15 minute
**Numar slide-uri:** 10

---

## Slide 1 – Titlu si echipa

**Titlu:** Testare Unitara in Python – BankAccount
**Subtitlu:** TSS T1 – Demonstrarea strategiilor de testare

**Continut:**
- Titlul proiectului si tema TSS
- Numele studentului / echipei
- Facultatea si grupul
- Data prezentarii

**Resursa vizuala:** Diagrama structurii proiectului (docs/diagrams/project_structure.mmd)

---

## Slide 2 – Scopul proiectului si alegerea aplicatiei

**Titlu:** De ce BankAccount?

**Bullet-uri:**
- Aplicatie cu logica de business clara si reguli bine definite
- Suficiente ramuri si conditii pentru toate strategiile de testare
- Validari multiple in constructor → material pentru condition coverage
- Metode cu decizii in serie → material pentru basis path testing
- Constante modificabile → material ideal pentru mutation testing

**Resursa vizuala:** Tabel cu metodele clasei si numarul de decizii per metoda

| Metoda           | Decizii | V(G) |
|------------------|---------|------|
| `deposit`        | 3       | 4    |
| `withdraw`       | 4       | 5    |
| `is_eligible_for_loan` | 5 | 6  |
| `apply_interest` | 1       | 2    |

---

## Slide 3 – Arhitectura proiectului

**Titlu:** Structura repository-ului

**Bullet-uri:**
- `src/bank_account.py` – SUT (System Under Test)
- `tests/test_bank_account.py` – suita principala (strategii 1-6)
- `tests/test_bank_account_additional_mutation.py` – strategia 7
- `docs/` – documentatie, diagrame CFG, tabele de analiza
- `scripts/` – automatizare rulare teste si rapoarte

**Resursa vizuala:** Diagrama Mermaid din docs/diagrams/project_structure.mmd

---

## Slide 4 – Strategia 1: Clase de echivalenta

**Titlu:** Partitionare in Clase de Echivalenta

**Bullet-uri:**
- Impartim domeniul de intrare in clase cu comportament similar
- Testam un reprezentant din fiecare clasa
- Exemplu `deposit`: valid (0<x<1M), zero, negativ, peste limita, non-numeric
- Exemplu `is_eligible_for_loan`: 5 clase de respingere + 1 clasa valida
- Total: **~35 teste** din aceasta strategie

**Resursa vizuala:** Tabelul din docs/tables/equivalence_classes.md (deposit)

---

## Slide 5 – Strategia 2: Valori de frontiera

**Titlu:** Analiza Valorilor de Frontiera

**Bullet-uri:**
- Testam valorile exact la frontiera si imediat in jurul ei
- Frontierea inferioara deposit: 0.00 (invalid), 0.01 (valid)
- Frontiera superioara deposit: 999_999.99 (valid), **1_000_000.00** (invalid)
- Overdraft checking: exact -500 (valid), -500.01 (invalid)
- Pragul tranzactii credit: 4 (invalid), **5** (valid), 6 (valid)

**Resursa vizuala:** Tabelul din docs/tables/boundary_values.md (deposit + transactions)

---

## Slide 6 – Strategii White-box: CFG si Basis Paths

**Titlu:** Decision/Condition Coverage si Basis Path Testing

**Bullet-uri:**
- **Decision coverage**: fiecare `if` evaluat atat True cat si False
- **Condition coverage**: fiecare sub-conditie dintr-o expresie compusa testata independent
  - ex: `not isinstance(owner, str) OR not owner.strip()` → 2 sub-conditii
- **Basis paths**: V(G) = 5 pentru `withdraw`, V(G) = 6 pentru `is_eligible_for_loan`
- Fiecare test are numele care indica explicit strategia: `test_withdraw_basis_path_p3_...`

**Resursa vizuala:** CFG-ul din docs/diagrams/cfg_withdraw.mmd

---

## Slide 7 – Coverage

**Titlu:** Rezultate Coverage

**Bullet-uri:**
- Tool: pytest-cov (wrapper peste coverage.py)
- **Statement coverage: 100%** la `src/bank_account.py`
- Decision si condition coverage: demonstrate prin analiza testelor (nu masurate direct de tool)
- coverage.py masoara instructiuni si ramuri, nu conditii individuale
- Comanda: `pytest --cov=src --cov-report=term-missing --cov-report=html`

**Resursa vizuala:**
`[Screenshot: pytest coverage report - 100% statements]`

---

## Slide 8 – Strategia 7: Mutation Testing

**Titlu:** Mutation Testing cu mutmut

**Bullet-uri:**
- Tool: mutmut 2.x (rulat in WSL/Linux)
- mutmut genereaza automat variatii ale codului (mutatii) si ruleaza testele
- Mutant **supravietuitor** = test insuficient de puternic
- **Mutant #1**: `>=` → `>` in deposit → permis 1_000_000 → omorat de test boundary exact
- **Mutant #2**: `<` → `<=` in loan eligibility → respins tx=5 → omorat de test boundary exact
- Scor final: `[Complete after local execution]`

**Resursa vizuala:**
`[Screenshot: mutmut results]`
Tabelul din docs/tables/mutation_analysis.md

---

## Slide 9 – Rolul AI in realizarea proiectului

**Titlu:** Utilizarea instrumentelor AI

**Bullet-uri:**
- **Instrument folosit:** Claude (Anthropic) prin Claude Code CLI
- **Utilizare la generarea codului:** scheletul initial al clasei BankAccount
- **Utilizare la generarea testelor:** structura testelor per strategie
- **Utilizare la documentatie:** generarea tabelelor si README-ului academic
- **Validare manuala:** toate testele au fost verificate, corectate si adaptate
  la specificatiile exacte ale temei; logica suitei a ramas responsabilitatea studentului

---

## Slide 10 – Concluzii

**Titlu:** Concluzii si lectii invatate

**Bullet-uri:**
- Statement coverage 100% nu garanteaza absenta bug-urilor (cf. mutation testing)
- Basis path testing ofera minimul necesar pentru acoperire completa a ramurilor
- Mutation testing identifica "gaurile" invizibile ale suitei de teste
- Alegerea frontierelor (= sau <, >= sau >) este critica si frecvent gresita
- Tool-urile (pytest-cov, mutmut) automatizeaza masurarea, dar analiza ramane umana

**Resursa vizuala:** Tabel comparativ al strategiilor

| Strategie           | Ce garanteaza                  | Limitari                       |
|---------------------|--------------------------------|--------------------------------|
| Clase echivalenta   | Acoperire logica a domeniului  | Nu testeaza frontierele exacte |
| Valori frontiera    | Detectie erori off-by-one      | Necesita cunoasterea frontierelor |
| Statement coverage  | Orice linie executata          | Nu detecta toate ramurile      |
| Decision coverage   | Ambele ramuri ale fiecarui if  | Nu detecta conditii compuse    |
| Condition coverage  | Fiecare sub-conditie           | Poate lasa cai netestate       |
| Basis paths         | Minimul de cai independente    | Nu acopera combinatii rare     |
| Mutation testing    | Calitatea testelor existente   | Lent, necesita curatarea manuala a echivalentilor |
