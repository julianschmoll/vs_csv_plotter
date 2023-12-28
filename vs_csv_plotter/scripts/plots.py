# Import local modules
from scripts import plot_by_diagram_type as plot

    
def plot_age_distribution(csv_data):
    age_counts = csv_data["Altersklasse"].value_counts()
    age_percent = age_counts / age_counts.sum() * 100
    plot.pie(age_percent, "Age Distribution")
