# Cosmic Ray notes

Rulare facuta in copia proiectului, pentru a nu atinge fisierele principale.

## Comenzi

```powershell
cd C:\Users\alexn\Documents\GitHub\TSS_Proiect\copy_project
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip pytest cosmic-ray
.\.venv\Scripts\cosmic-ray.exe baseline cosmic-ray.toml --session-file cosmic-ray-baseline-fixed.sqlite
.\.venv\Scripts\cosmic-ray.exe init --force cosmic-ray.toml cosmic-ray.sqlite
.\.venv\Scripts\cosmic-ray.exe exec cosmic-ray.toml cosmic-ray.sqlite
.\.venv\Scripts\cr-report.exe cosmic-ray.sqlite
.\.venv\Scripts\cr-report.exe cosmic-ray.sqlite --surviving-only --show-diff > cosmic-ray-survivors.txt
.\.venv\Scripts\cr-rate.exe cosmic-ray.sqlite
```

## Rezultat

- Mutanti generati: 166
- Mutanti finalizati: 166
- Mutanti supravietuitori: 9
- Rata supravietuire: 5.42%
- Scor aproximativ omorare mutanti: 94.58%

Mutantii supravietuitori sunt listati in `cosmic-ray-survivors.txt`.
