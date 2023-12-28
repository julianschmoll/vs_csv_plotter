"""Plots from current survey."""
# Import local modules
import constants
# Import third party modules
import pandas as pd
from scripts import plot_by_diagram_type as plot


def plot_financial_impact(csv_data):
    """Generate a line plot comparing the financial impact ratings.

    Parameters:
        csv_data (pd.DataFrame): DataFrame with survey data.

    """
    row_index = (
        "Wie stark würde dich das vollsolidarische bundesweite Semesterticket "
        + "finanziell treffen? (Skala 1 (kein/kleines Problem) - 10 (nicht finanzierbar))"
    )
    over_26_data = csv_data[csv_data["Altersklasse"] == "> 26"]
    under_26_data = csv_data[csv_data["Altersklasse"] == "≤ 26"]
    plot_data_over_26 = pd.DataFrame({
        'Rating': over_26_data[row_index],
        'Age Group': "> 26"
    })
    plot_data_under_26 = pd.DataFrame({
        'Rating': under_26_data[row_index],
        'Age Group': "≤ 26"
    })
    mean_over_26 = over_26_data[row_index].mean()
    mean_under_26 = under_26_data[row_index].mean()
    mean_list = [("> 26", mean_over_26), ("≤ 26", mean_under_26)]
    plot_data = pd.concat([plot_data_over_26, plot_data_under_26])
    plot.line_with_mean(plot_data, mean_list, "Financial Impact")


def plot_participation(csv_data):
    """Plot the participation compared to all students.

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    """
    num_participants = len(csv_data)-1
    plot_values = [constants.STUDENTS - num_participants, num_participants]
    labels = ["Non-Participants", "Participants"]
    part_data = pd.Series(plot_values, index=labels)
    plot.pie(part_data, "Participation")


def plot_age_distribution(csv_data):
    """Plot the age distribution based on survey data.

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    """
    age_counts = csv_data["Altersklasse"].value_counts()
    plot.pie(age_counts, "Age Distribution")


def plot_ticket_data(csv_data):  # noqa: WPS210 As splitting up wouldn't make sense
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
        + "Würdest du das Jugendticket BW beziehen wenn du berechtigt wärst?"
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
