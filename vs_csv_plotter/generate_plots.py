# Import local modules
from scripts import plots
from scripts.file_utils import replace_ger_eng
from scripts.file_utils import concat_from_folder
from scripts.file_utils import prepare_plot_folder


combined_data = replace_ger_eng(concat_from_folder())
prepare_plot_folder()
plots.plot_participation(combined_data)
plots.plot_age_distribution(combined_data)
plots.plot_ticket_data(combined_data)
