#!/bin/bash
# Working directory: src/COMP2120-Assignment4
# Prepare attachments for COMP2120 Assignment 4

echo "Preparing attachments..."

cd .COPY
echo "Current directory: $(pwd)"
ls -la

echo "Zipping..."
zip -r ../COMP2120-Assignment4_Attachments.zip .
echo "File created."
echo "$(ls -la .. | grep ".zip")"

echo "Cleaning up..."
rm -rf ./*

cd ..
echo "Current directory: $(pwd)"
echo "Moving zip file to .COPY/ directory..."
mv COMP2120-Assignment4_Attachments.zip ./.COPY/
echo "Done."
echo "$(ls -la .COPY/)"