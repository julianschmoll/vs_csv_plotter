@echo off

cd /d "%~dp0"
echo Installing dependencies
python -m pip install .

echo Generating Plots...
python vs_csv_plotter\generate_plots.py

echo Succesfully generated plots.
