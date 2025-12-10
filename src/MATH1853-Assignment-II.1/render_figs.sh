#!/bin/bash

# Traverse all .tex files in figs directory and build them into PDFs
for tex_file in figs/*.tex; do
    if [ -f "$tex_file" ]; then
        echo "Building $tex_file..."
        latexmk -pdf -output-directory=figs "$tex_file"
    fi
done

echo "Done building all figures."