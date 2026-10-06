#!/bin/bash

# Script per la compilazione di tutti i file .ui dentro la cartella app/ui_generated in python
# Da eseguire ogni volta che si modifica l'interfaccia

set -e

UI_DIR="ui"
OUTPUT_DIR="app/ui_generated"
echo "Avvio compilazione file di interfaccia dalla cartella $UI_DIR nella cartella $OUTPUT_DIR"

mkdir -p "$OUTPUT_DIR"
echo "Compilazione file .ui..."

for ui_file in "$UI_DIR"/*.ui; do
    [ -e "$ui_file" ] || continue

    filename=$(basename "$ui_file" .ui)
    output_file="$OUTPUT_DIR/ui_${filename}.py"   # tutti i file generati contengono un prefisso ui_ per distinguerli

    echo "  $ui_file -> $output_file"
    .venv/bin/pyside6-uic "$ui_file" -o "$output_file"    # Utilizza il virtual environment locale del progetto
done

echo "Compilazione completata."