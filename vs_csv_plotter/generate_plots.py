"""Generate Plots."""
# Import local modules
from scripts import file_utils, plots

class PlotGenerator:
    def __init__(self):
        self.combined_data = None

    def generate_plots(self):
        """Generate Plots"""
        self.combined_data = file_utils.replace_ger_eng(file_utils.concat_from_folder())
        file_utils.prepare_plot_folder()
        plots.plot_participation(self.combined_data)
        plots.plot_age_distribution(self.combined_data)
        plots.plot_ticket_data(self.combined_data)

if __name__ == "__main__":
    plot_generator = PlotGenerator()
    plot_generator.generate_plots()