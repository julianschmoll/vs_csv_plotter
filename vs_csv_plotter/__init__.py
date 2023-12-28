"""Initialize vs_csv_plotter"""
# Import builtin modules
import os


# Create the 'plot' folder
plot_folder = os.path.join("plot")
os.makedirs(plot_folder, exist_ok=True)

# Create the 'data/csv' folder
data_csv_folder = os.path.join("data", "csv")
os.makedirs(data_csv_folder, exist_ok=True)
