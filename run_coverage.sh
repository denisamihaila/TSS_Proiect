#!/usr/bin/env bash
# Script final pentru proiectul TSS T1 - FitnessClassBooking.
# Ruleaza suita de teste, calculeaza coverage pentru fisierul principal si,
# daca mediul permite, ruleaza analiza de mutatie cu mutmut.
# Dependente: pytest, coverage si mutmut<3 pentru analiza de mutatie.

set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python}"
LOG_DIR="logs"
RUN_MUTMUT="${RUN_MUTMUT:-auto}"
PYTEST_ARGS="${PYTEST_ARGS:--q}"

TEST_FILES=(
    "test_equivalence_partitioning.py"
    "test_boundary_value_analysis.py"
    "test_coverage.py"
    "test_independent_circuits.py"
    "test_mutation.py"
)

mkdir -p "$LOG_DIR"

print_header() {
    echo "========================================="
    echo " TSS T1 - FitnessClassBooking Test Suite"
    echo "========================================="
}

run_pytest() {
    echo ""
    echo "[1/3] Rulare teste unitare..."
    "$PYTHON_BIN" -m pytest $PYTEST_ARGS "${TEST_FILES[@]}" 2>&1 \
        | tee "$LOG_DIR/pytest_output.txt"
}

run_coverage() {
    echo ""
    echo "[2/3] Coverage statement + branch pentru fitness_class_booking.py..."
    {
        "$PYTHON_BIN" -m coverage erase
        "$PYTHON_BIN" -m coverage run --branch -m pytest -q "${TEST_FILES[@]}"
        "$PYTHON_BIN" -m coverage report -m --include="fitness_class_booking.py"
        "$PYTHON_BIN" -m coverage html --include="fitness_class_booking.py"
        echo ""
        echo "Raport HTML generat in: htmlcov/index.html"
    } 2>&1 | tee "$LOG_DIR/coverage_report.txt"
}

mutmut_available() {
    "$PYTHON_BIN" -m mutmut version >/dev/null 2>&1
}

run_mutmut() {
    local runner
    runner="$PYTHON_BIN -m pytest -q ${TEST_FILES[*]}"

    echo ""
    echo "[3/3] Analiza mutanti cu mutmut..."
    {
        "$PYTHON_BIN" -m mutmut run --paths-to-mutate fitness_class_booking.py \
            --tests-dir . \
            --runner "$runner"
        "$PYTHON_BIN" -m mutmut results
    } 2>&1 | tee "$LOG_DIR/mutmut_results.txt"
}

skip_mutmut() {
    local reason="$1"

    echo ""
    echo "[3/3] Analiza mutanti cu mutmut: skipped"
    echo "$reason" | tee "$LOG_DIR/mutmut_results.txt"
}

print_header
run_pytest
run_coverage

case "$RUN_MUTMUT" in
    0|false|False|FALSE|no|No|NO)
        skip_mutmut "Mutmut a fost dezactivat prin RUN_MUTMUT=$RUN_MUTMUT."
        ;;
    1|true|True|TRUE|yes|Yes|YES)
        if mutmut_available; then
            run_mutmut
        else
            echo "Mutmut nu este disponibil in acest mediu." | tee "$LOG_DIR/mutmut_results.txt"
            echo "Pe Windows ruleaza din WSL sau foloseste: RUN_MUTMUT=0 bash run_coverage.sh"
            exit 1
        fi
        ;;
    auto)
        if mutmut_available; then
            run_mutmut
        else
            skip_mutmut "Mutmut nu este disponibil in acest mediu. Pe Windows se ruleaza din WSL."
        fi
        ;;
    *)
        echo "Valoare invalida pentru RUN_MUTMUT: $RUN_MUTMUT"
        echo "Foloseste RUN_MUTMUT=auto, RUN_MUTMUT=1 sau RUN_MUTMUT=0."
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo " Gata."
echo " Logs:"
echo " - $LOG_DIR/pytest_output.txt"
echo " - $LOG_DIR/coverage_report.txt"
echo " - $LOG_DIR/mutmut_results.txt"
echo "========================================="
