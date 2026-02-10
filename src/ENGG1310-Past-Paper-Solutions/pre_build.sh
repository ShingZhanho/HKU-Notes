#!/bin/bash

# This script pre-compiles all TikZ standalone figures in the 'figs' directory.

FIGS_DIR="figs"
for fig in "$FIGS_DIR"/*.tex; do
    if [ -f "$fig" ]; then
        echo "Compiling $fig..."
        pdflatex -output-directory="$FIGS_DIR" "$fig"
    fi
done