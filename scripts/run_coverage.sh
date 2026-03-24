#!/usr/bin/env bash
# Rulare teste cu raport de coverage (statement + branch)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
if [[ -z "$PYTHON" ]]; then
    echo "EROARE: python3/python nu a fost gasit. Activati venv-ul."
    exit 1
fi

echo "============================================================"
echo "  TSS T1 – Coverage report"
echo "  Python: $PYTHON"
echo "============================================================"
echo ""

mkdir -p htmlcov

"$PYTHON" -m pytest tests/ \
    --cov=src \
    --cov-branch \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    -v

echo ""
echo "Raport HTML generat in: htmlcov/index.html"
