#!/usr/bin/env bash
# Rulare mutation testing cu mutmut 2.x
# Necesita: Linux / WSL cu venv activat si mutmut 2.x instalat
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || true)
if [[ -z "$PYTHON" ]]; then
    echo "EROARE: python3/python nu a fost gasit."
    echo "Activati venv-ul: source .venv/bin/activate"
    exit 1
fi

echo "============================================================"
echo "  TSS T1 – Mutation Testing cu mutmut"
echo "  Python: $PYTHON"
echo "============================================================"
echo ""

# Verificare mutmut instalat – importul modulului e metoda corecta;
# apelul "python -m mutmut" fara subcomanda returneaza exit code != 0
# chiar si cand e instalat, ceea ce ar face check-ul sa esueze fals.
if ! "$PYTHON" -c "import mutmut" 2>/dev/null; then
    echo "EROARE: mutmut nu este instalat."
    echo "Ruleaza: pip install 'mutmut>=2.4.0,<3.0.0'"
    exit 1
fi

echo "Pasul 1/2: Generare si evaluare mutanti..."
# mutmut run returneaza exit code 1 daca exista survivori – normal, nu e eroare fatala
"$PYTHON" -m mutmut run || true

echo ""
echo "Pasul 2/2: Rezultate..."
"$PYTHON" -m mutmut results

echo ""
echo "Pentru detalii despre un mutant specific: $PYTHON -m mutmut show <id>"
