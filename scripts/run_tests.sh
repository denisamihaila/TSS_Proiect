#!/usr/bin/env bash
# Rulare suita completa de teste (fara coverage)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Detectare python3 sau python
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
if [[ -z "$PYTHON" ]]; then
    echo "EROARE: python3/python nu a fost gasit in PATH."
    echo "Activati venv-ul: source .venv/bin/activate"
    exit 1
fi

echo "============================================================"
echo "  TSS T1 – Rulare teste unitare"
echo "  Python: $PYTHON"
echo "============================================================"
echo ""

"$PYTHON" -m pytest tests/ -v --tb=short

echo ""
echo "Rulare finalizata."
