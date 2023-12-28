# Import local modules
from scripts import plots
from scripts import file_utils


combined_data = file_utils.concat_from_folder()
file_utils.prepare_plot_folder()
plots.plot_participation(combined_data)
plots.plot_age_distribution(combined_data)
plots.plot_youth_ticket_data(combined_data)
