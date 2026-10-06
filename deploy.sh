#!/bin/bash

set -e

echo "=============================="
echo " Deploy applicazione"
echo "=============================="

echo ""
echo "[1/2] Compilazione UI..."
./compile-ui.sh

echo ""
echo "[2/2] Creazione applicazione..."
.venv/bin/pyside6-deploy main.py

echo ""
echo "=============================="
echo " Deploy completato"
echo "=============================="