"""Main generation script."""
# Import local modules
from scripts import file_utils, plots

combined_data = file_utils.replace_ger_eng(file_utils.concat_from_folder())
file_utils.prepare_plot_folder()
plots.plot_participation(combined_data)
plots.plot_age_distribution(combined_data)
plots.plot_ticket_data(combined_data)
