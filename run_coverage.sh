#!/usr/bin/env bash
# script pentru rulat toate testele + coverage + mutmut
# se rulează din WSL cu venv-ul activat

set -e  # oprește la prima eroare

echo "========================================="
echo " TSS T1 – FitnessClassBooking Test Suite"
echo "========================================="

# Instalare dependențe
echo ""
echo "[1/5] Instalare dependențe..."
pip install pytest coverage "mutmut<3" --quiet

# Rulare teste cu pytest
echo ""
echo "[2/5] Rulare teste..."
python -m pytest test_equivalence_partitioning.py \
                 test_boundary_value_analysis.py \
                 test_coverage.py \
                 test_independent_circuits.py \
                 test_mutation.py \
                 -v

# 3. Coverage – statement + branch
echo ""
echo "[3/5] Analiză acoperire (statement + branch)..."
python -m coverage run --branch -m pytest \
    test_equivalence_partitioning.py \
    test_boundary_value_analysis.py \
    test_coverage.py \
    test_independent_circuits.py \
    test_mutation.py

# Afișare rezultate în terminal
echo ""
echo "[4/5] Raport acoperire..."
python -m coverage report -m --include="fitness_class_booking.py"

# Raport HTML
python -m coverage html --include="fitness_class_booking.py"
echo "Raport HTML generat în: htmlcov/index.html"

# Analiză mutanți (din WSL)
echo ""
echo "[5/5] Analiză mutanți (mutmut)..."
python -m mutmut run --paths-to-mutate fitness_class_booking.py --tests-dir .
python -m mutmut results

echo ""
echo "========================================="
echo " Gata! Raportul se află în htmlcov/index.html"
echo "========================================="
