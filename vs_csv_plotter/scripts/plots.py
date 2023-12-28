# Import local modules
import constants
from scripts import plot_by_diagram_type as plot

# Import third party modiles
import pandas as pd


def plot_participation(csv_data):
    num_participants = len(csv_data)-1
    values = [constants.STUDENTS - num_participants, num_participants]
    labels = ["Non-Participants", "Participants"]
    part_data = pd.Series(values, index=labels)
    plot.pie(part_data, "Participation")
    
    
def plot_age_distribution(csv_data):
    age_counts = csv_data["Altersklasse"].value_counts()
    plot.pie(age_counts, "Age Distribution")
