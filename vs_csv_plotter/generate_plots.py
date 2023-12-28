"""Generate Plots."""
# Import local modules
from scripts import file_utils, plots

class PlotGenerator:
    """Generates Plots-"""
    def __init__(self):
        self.gather_data()
        file_utils.prepare_plot_folder()

    def gather_data(self):
        """Gather Data from CSV Folder."""
        self.combined_data = file_utils.replace_ger_eng(file_utils.concat_from_folder())

    def generate_plots(self):
        """Generate Plots"""
        plots.plot_participation(self.combined_data)
        plots.plot_age_distribution(self.combined_data)
        plots.plot_ticket_data(self.combined_data)
        plots.plot_support_data(self.combined_data)
        plots.plot_financial_impact(self.combined_data)

if __name__ == "__main__":
    plot_generator = PlotGenerator()
    plot_generator.generate_plots()
