# Import local modules
from scripts import plots
from scripts import csv_utils


combined_data = csv_utils.concat_from_folder()
plots.plot_age_distribution(combined_data)
csv_utils.set_timestamp
