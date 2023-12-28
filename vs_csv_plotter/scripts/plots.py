"""Plots from current survey"""
# Import local modules
import constants
from scripts import plot_by_diagram_type as plot

# Import third party modiles
import pandas as pd


def plot_participation(csv_data):
    """Plot the participation compared to all students.

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    """
    num_participants = len(csv_data)-1
    values = [constants.STUDENTS - num_participants, num_participants]
    labels = ["Non-Participants", "Participants"]
    part_data = pd.Series(values, index=labels)
    plot.pie(part_data, "Participation")


def plot_age_distribution(csv_data):
    """Plot the age distribution based on survey data.

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    """
    age_counts = csv_data["Altersklasse"].value_counts()
    plot.pie(age_counts, "Age Distribution")


def plot_ticket_data(csv_data):
    """Plot ticket-related data based on survey responses.

    This function generates three pie charts illustrating ticket-related
    information based on the survey responses:
    1. "Would you buy the JugendBW-Ticket if eligible? (>26)"
    2. "Do you own the D-Ticket? (>26)"
    3. "Do you currently have the JugendBW-Ticket? (≤26)"

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    """
    row_index = (
        "Beziehst du aktuell das Jugendticket BW / "
        "Würdest du das Jugendticket BW beziehen wenn du berechtigt wärst?"
    )
    d_ticket_index = "Beziehst du aktuell das Deutschlandticket (49 € Ticket)?"

    over_26_data = csv_data[csv_data["Altersklasse"] == "> 26"]
    under_26_data = csv_data[csv_data["Altersklasse"] == "≤ 26"]

    over_26_count = over_26_data[row_index].value_counts()
    over_26_d_ticket_count = over_26_data[d_ticket_index].value_counts()

    under_26_count = under_26_data[row_index].value_counts()
    under_26_no_youth_ticket = under_26_data[under_26_data[row_index] == "No"]
    under_26_d_ticket = under_26_no_youth_ticket[d_ticket_index].value_counts()
    removed_no = under_26_count.drop("No", errors="ignore")
    under_26_d_ticket = under_26_d_ticket.rename(index={"Yes": "No, D-Ticket"})
    combined_under_26 = removed_no.add(under_26_d_ticket, fill_value=0)

    plot.pie(
        over_26_count, "Would you buy the JugendBW-Ticket if eligible? (>26)"
    )
    plot.pie(over_26_d_ticket_count, "Do you own the D-Ticket? (>26)")
    plot.pie(
        combined_under_26, "Do you currently have the JugendBW-Ticket? (≤26)"
    )
