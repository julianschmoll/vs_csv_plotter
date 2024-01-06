"""Plots from current survey."""
# Import local modules
import constants
from scripts import file_utils
from scripts import plot_by_diagram_type as plot

# Import third-party modules
import pandas as pd


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
        "Rating": over_26_data[row_index].value_counts() / len(over_26_data),
        "Age Group": "> 26"
    })
    plot_data_under_26 = pd.DataFrame({
        "Rating": under_26_data[row_index].value_counts() /len(under_26_data),
        "Age Group": "≤ 26"
    })
    mean = csv_data[row_index].mean()
    mean_over_26 = over_26_data[row_index].mean()
    mean_under_26 = under_26_data[row_index].mean()
    mean_list = [("> 26", mean_over_26), ("≤ 26", mean_under_26)]
    plot_data = pd.concat([plot_data_over_26, plot_data_under_26])
    plot.line_with_mean(
        plot_data,
        "Rating",
        "Self rated financial Impact of solidarity ticket",
        plot_data_key = "Age Group",
        x_value_label = "Rating (Scale 1 (no/minor problem) - 10 (cannot be financed))",
        y_value_label = "Percent",
        mean_list = mean_list,
        mean=mean
    )


def plot_participation(csv_data):
    """Plot the participation compared to all students.

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    """
    num_participants = len(csv_data)-1
    plot_values = [constants.STUDENTS - num_participants, num_participants]
    labels = ["Non-Participants", "Participants"]
    part_data = pd.Series(plot_values, index=labels)
    plot.pie(part_data, "Participation of all HdM students")


def plot_age_distribution(csv_data):
    """Plot the age distribution based on survey data.

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    """
    age_counts = csv_data["Altersklasse"].value_counts()
    plot.pie(age_counts, "Age Distribution of participants")


def plot_ticket_data(csv_data):  # noqa: WPS210 As splitting up wouldn"t make sense
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

    support_with_d_ticket = over_26_data[over_26_data[row_index] == "Yes"]
    support_with_d_ticket_counts = support_with_d_ticket[d_ticket_index].value_counts()

    plot.pie(
        over_26_count, "Would you buy a JugendBW-Ticket if eligible? (>26)"
    )
    plot.pie(
        over_26_d_ticket_count, "Do you own a D-Ticket? (>26)"
    )
    plot.pie(
        combined_under_26, "Do you currently have a JugendBW-Ticket? (≤26)"
    )
    plot.pie(
        support_with_d_ticket_counts,
        "Owning a D-Ticket while being interested in JugendBW-Ticket? (>26)"
    )


def plot_support_data(csv_data):
    """Plot general support for Ticket.
    
    1. Everyone
    2. below 26
    3. above 26

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    """
    row_index = (
        "Würdest du ein vollsolidarisches Deutschlandticket unterstützen?"
    )

    wealth_index = (
        "Wie stark würde dich das vollsolidarische bundesweite Semesterticket "
        +"finanziell treffen? (Skala 1 (kein/kleines Problem) - 10 (nicht finanzierbar))"
    )

    support_counts = {
        ">26": csv_data[csv_data["Altersklasse"] == "> 26"][row_index].value_counts(),
        "All Ages": csv_data[row_index].value_counts(),
        "≤26": csv_data[csv_data["Altersklasse"] == "≤ 26"][row_index].value_counts(),
        "Financially not affected (Self Rated <4)": csv_data[csv_data[wealth_index] < 4][row_index].value_counts(),
        "Financially affected (Self Rated >7)": csv_data[csv_data[wealth_index] > 7][row_index].value_counts(),
        "Financially affected (Self Rated >7) (>26)": csv_data[(csv_data[wealth_index] > 7) & (csv_data["Altersklasse"] == "> 26")][row_index].value_counts(),
        "Financially not affected (Self Rated <4) (>26)": csv_data[(csv_data[wealth_index] < 4) & (csv_data["Altersklasse"] == "> 26")][row_index].value_counts(),
        "Financially affected (Self Rated >7) (≤26)": csv_data[(csv_data[wealth_index] > 7) & (csv_data["Altersklasse"] == "≤ 26")][row_index].value_counts(),
        "Financially not affected (Self Rated <4) (≤26)": csv_data[(csv_data[wealth_index] < 4) & (csv_data["Altersklasse"] == "≤ 26")][row_index].value_counts(),
    }

    for label, data_count in support_counts.items():
        plot.pie(data_count, f"Would you support a full solidarity ticket for Germany? ({label})")


def plot_support_data_vs_financial_impact(csv_data):
    """Plot support for full solidarity ticket vs. financial impact.

    This function generates a line plot comparing the support for a full solidarity ticket
    with the financial impact ratings, for both age groups.

    Parameters:
        csv_data (pd.DataFrame): DataFrame with survey data.

    """
    row_index = (
        "Würdest du ein vollsolidarisches Deutschlandticket unterstützen?"
    )

    wealth_index = (
        "Wie stark würde dich das vollsolidarische bundesweite Semesterticket "
        +"finanziell treffen? (Skala 1 (kein/kleines Problem) - 10 (nicht finanzierbar))"
    )

    csv_dict = {
        "(All Ages)": csv_data,
        "(>26)":csv_data[csv_data["Altersklasse"] == "> 26"],
        "(≤26)":csv_data[csv_data["Altersklasse"] == "≤ 26"]
    }
    for label, csv_data in csv_dict.items():
        df = pd.DataFrame()
        for wealth_value in range(1, 11):
            data = csv_data[csv_data[wealth_index] == wealth_value]
            support_count = data[row_index].value_counts().reset_index()
            support_count.columns = [row_index, "count"]
            support_count["relative_count"] = support_count["count"] / len(data)
            support_count["wealth_index"] = wealth_value
            df = pd.concat([df, support_count], ignore_index=True)

        categories = df[row_index].unique()
        title = f"Support for full solidarity ticket over financial situation {label} (self Rated)"
        x_value = "wealth_index"
        y_value = "relative_count"
        x_label = "Rating (Scale 1 (no/minor problem) - 10 (cannot be financed))"
        y_label = "Percent"

        plot.plot_stack_chart(row_index, df, categories, title, x_value, y_value, x_label, y_label)


def plot_participation_over_time(data):
    """Plot participation over time.

    This function generates a line plot comparing the support for a full solidarity ticket
    with the financial impact ratings, for both age groups.

    Parameters:
        csv_data (pd.DataFrame): DataFrame with survey data.

    """
    df = pd.DataFrame()
    df["Zeitstempel"] = data["Zeitstempel"].apply(file_utils.convert_timestamp)
    df = df.sort_values(by="Zeitstempel")
    df["Participation"] = range(1, len(df) + 1)
    plot.plot_line_chart(
        df=df,
        categories=["Participation"],
        title="Participation Over Time",
        x_value="Zeitstempel",
        y_value="Participation",
        x_label="Time",
        y_label="Cumulative Number of Participants",
        xlim=(min(df["Zeitstempel"]), max(df["Zeitstempel"])),
        ylim=(0, max(df["Participation"]) + 10)
    )
