#!/bin/bash

# Change to the directory containing the script
cd "$(dirname "$0")"

echo "Installing dependencies"
python -m pip install .

echo "Generating Plots..."
python vs_csv_plotter/generate_plots.py

echo "Successfully generated plots."
