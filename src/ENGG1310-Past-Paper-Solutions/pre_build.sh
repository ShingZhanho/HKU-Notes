#!/bin/bash

# This script pre-compiles all TikZ standalone figures in the 'figs' directory.

FIGS_DIR="figs"
for fig in "$FIGS_DIR"/*.tex; do
    if [ -f "$fig" ]; then
        pdf="${fig%.tex}.pdf"
        # Only compile if PDF doesn't exist or if .tex is newer than .pdf
        if [ ! -f "$pdf" ] || [ "$fig" -nt "$pdf" ]; then
            echo "Compiling $fig..."
            pdflatex -interaction=batchmode -output-directory="$FIGS_DIR" "$fig"
        fi
    fi
done