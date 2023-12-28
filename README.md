# vs_csv_plotter
Plotter for CSV from VS Cloud

## Usage

1. Add CSV data in `data/csv` 
1. Optional: change `scripts/plots.py` to fulfill your needs and add desired plot functions to `generate_plots/main()`. 
1. Optional: Change plot style or make adjustments in `constants.py`.
1. Run either `generate_plots.cmd` or `generate_plots.sh`. This installs all dependencies specified in `setup.py` and executed `generate_plots.py`.
1. Desired plots are in folder specified in `constants`.

## Installation

This is only nessecary for developing: To install the dependencies for this project, you can use either `requirements.txt` or `setup.py`.

### Using `requirements.txt`

```bash
pip install -r requirements.txt
```

### Using `setup.py`
```bash
pip install .
```

Now you should be able to change/add code with every third party package being correctly resolved.

## Contributing

If you want to contribute to this project, follow these steps:

1. Fork the project.
1. Create a new branch.
1. Make your changes and submit a pull request.
