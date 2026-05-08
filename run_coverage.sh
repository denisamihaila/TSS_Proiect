#!/usr/bin/env bash
# Script pentru rulat testele principale + coverage + mutmut.
# Se ruleaza din WSL cu venv-ul activat.

set -e

echo "========================================="
echo " TSS T1 - FitnessClassBooking Test Suite"
echo "========================================="

echo ""
echo "[1/5] Instalare dependente..."
pip install pytest coverage "mutmut<3" --quiet

echo ""
echo "[2/5] Rulare teste..."
python -m pytest test_equivalence_partitioning.py \
                 test_boundary_value_analysis.py \
                 test_coverage.py \
                 test_independent_circuits.py \
                 test_mutation.py \
                 -v

echo ""
echo "[3/5] Analiza acoperire (statement + branch)..."
python -m coverage run --branch -m pytest \
    test_equivalence_partitioning.py \
    test_boundary_value_analysis.py \
    test_coverage.py \
    test_independent_circuits.py \
    test_mutation.py

echo ""
echo "[4/5] Raport acoperire..."
python -m coverage report -m --include="fitness_class_booking.py"
python -m coverage html --include="fitness_class_booking.py"
echo "Raport HTML generat in: htmlcov/index.html"

echo ""
echo "[5/5] Analiza mutanti (mutmut)..."
python -m mutmut run --paths-to-mutate fitness_class_booking.py \
    --tests-dir . \
    --runner "python -m pytest -q"
python -m mutmut results

echo ""
echo "========================================="
echo " Gata! Raportul se afla in htmlcov/index.html"
echo "========================================="
