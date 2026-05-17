# Cosmic Ray notes

Acest folder pastreaza artefactele relevante pentru rularea Cosmic Ray.
Cosmic Ray este un tool de mutation testing, similar ca scop cu `mutmut`.

## Comenzi

```powershell

cd D:\Licenta\TSS_Proiect

# Instalare Cosmic Ray
python -m pip install pytest cosmic-ray

# Ruleaza testele pe codul original si masoara durata
cosmic-ray baseline cosmic_ray\cosmic-ray.toml --session-file cosmic_ray\cosmic-ray-baseline.sqlite

# Genereaza toti mutantii posibili si ii salveaza in baza de date 
cosmic-ray init --force cosmic_ray\cosmic-ray.toml cosmic_ray\cosmic-ray.sqlite

# Ruleaza testele pentru fiecare mutant si inregistreaza rezultatul (killed / survived / timeout)
cosmic-ray exec cosmic_ray\cosmic-ray.toml cosmic_ray\cosmic-ray.sqlite

# Exporta raportul complet cu toti mutantii si statusul lor
cr-report cosmic_ray\cosmic-ray.sqlite > cosmic_ray\cosmic-ray-report.txt

# Exporta doar mutantii supravietuitori cu diff-ul exact fata de codul original
cr-report cosmic_ray\cosmic-ray.sqlite --surviving-only --show-diff > cosmic_ray\cosmic-ray-survivors.txt

# Calculeaza si afiseaza scorul final
cr-rate cosmic_ray\cosmic-ray.sqlite
```

## Rezultat

- Mutanti generati: 166
- Mutanti finalizati: 166 (niciunul nu a produs timeout)
- Mutanti ucisi: 157
- Mutanti supravietuitori: 9
- Rata supravietuire: 5.42%
- Scor aproximativ omorare mutanti: 94.58%

Mutantii supravietuitori sunt listati in `cosmic-ray-survivors.txt`.

O parte dintre mutantii supravietuitori sunt echivalenti sau foarte
apropiati de comportamentul original, de exemplu comparatii de forma
`remaining_sessions == 0` mutate in `remaining_sessions <= 0`, in conditiile
in care codul nu permite valori negative pentru `remaining_sessions`.
