# Cosmic Ray notes

Acest folder pastreaza artefactele relevante pentru rularea Cosmic Ray.
Copia completa a proiectului nu este necesara pentru analiza de mutatie si a
fost eliminata ca sa nu fie colectate teste duplicate de `pytest`.

Cosmic Ray este un tool de mutation testing, similar ca scop cu `mutmut`.
Rezultatul este folosit ca analiza suplimentara/comparativa.

## Comenzi

Comenzile se ruleaza din radacina proiectului.

```powershell
cd D:\Licenta\TSS_Proiect
python -m pip install pytest cosmic-ray
cosmic-ray baseline cosmic_ray\cosmic-ray.toml --session-file cosmic_ray\cosmic-ray-baseline.sqlite
cosmic-ray init --force cosmic_ray\cosmic-ray.toml cosmic_ray\cosmic-ray.sqlite
cosmic-ray exec cosmic_ray\cosmic-ray.toml cosmic_ray\cosmic-ray.sqlite
cr-report cosmic_ray\cosmic-ray.sqlite > cosmic_ray\cosmic-ray-report.txt
cr-report cosmic_ray\cosmic-ray.sqlite --surviving-only --show-diff > cosmic_ray\cosmic-ray-survivors.txt
cr-rate cosmic_ray\cosmic-ray.sqlite
```

## Rezultat

- Mutanti generati: 166
- Mutanti finalizati: 166
- Mutanti supravietuitori: 9
- Rata supravietuire: 5.42%
- Scor aproximativ omorare mutanti: 94.58%

Mutantii supravietuitori sunt listati in `cosmic-ray-survivors.txt`.

O parte dintre mutantii supravietuitori sunt probabil echivalenti sau foarte
apropiati de comportamentul original, de exemplu comparatii de forma
`remaining_sessions == 0` mutate in `remaining_sessions <= 0`, in conditiile
in care codul nu permite valori negative pentru `remaining_sessions`.
