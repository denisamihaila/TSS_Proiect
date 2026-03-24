#!/usr/bin/env bash
# Generare toate rapoartele: teste + coverage + mutation
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || true)
if [[ -z "$PYTHON" ]]; then
    echo "EROARE: python3/python nu a fost gasit. Activati venv-ul."
    exit 1
fi

echo "============================================================"
echo "  TSS T1 – Generare rapoarte complete"
echo "  Python: $PYTHON"
echo "============================================================"
echo ""

mkdir -p htmlcov reports

# ---------------------------------------------------------------------------
# 1. Teste + Coverage
# ---------------------------------------------------------------------------
echo "[1/2] Rulare teste cu coverage..."
"$PYTHON" -m pytest tests/ \
    --cov=src \
    --cov-branch \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-report=xml:reports/coverage.xml \
    -q

echo ""
echo "Coverage HTML: htmlcov/index.html"
echo "Coverage XML:  reports/coverage.xml"
echo ""

# ---------------------------------------------------------------------------
# 2. Mutation testing (optional – ruleaza numai pe Linux/WSL)
# ---------------------------------------------------------------------------
if [[ "$(uname -s)" == "Linux" ]]; then
    echo "[2/2] Rulare mutation testing..."

    # Verificare mutmut
    if ! "$PYTHON" -c "import mutmut" 2>/dev/null; then
        echo "  mutmut nu este instalat – sarit."
        echo "  Instaleaza cu: pip install 'mutmut>=2.4.0,<3.0.0'"
    else
        # mutmut run returneaza exit code 1 cand exista survivori.
        # Folosim || true ca scriptul sa continue si sa scrie raportul.
        "$PYTHON" -m mutmut run || true

        "$PYTHON" -m mutmut results > reports/mutation_results.txt 2>&1 || true
        echo "  Mutation results: reports/mutation_results.txt"
        cat reports/mutation_results.txt
    fi
else
    echo "[2/2] Mutation testing sarit (necesita Linux/WSL)."
    echo "      Comanda: bash scripts/run_mutation.sh"
fi

echo ""
echo "Toate rapoartele disponibile au fost generate."
