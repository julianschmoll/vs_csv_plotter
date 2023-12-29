"""This module provides utility functions for creating charts."""
# Import built-in modules
import logging
# Import local modules
import constants
from scripts import file_utils
# Import third-party modules
from matplotlib import pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)


def save_or_show_plot(
    title,
    save=constants.SAVE_PLOT,
    show=constants.SHOW_PLOT,
):
    """Save or show a Matplotlib plot based on specified parameters.

    This function allows the user to customize the saving and displaying
    behavior of a Matplotlib plot. The plot title, as well as optional
    parameters to save and/or display the plot, can be specified.

    Parameters:
        title (str): Title of the Matplotlib plot.
        save (bool, optional): Defaults to constants.SAVE_PLOT.
        show (bool, optional): Defaults to constants.SHOW_PLOT.

    """
    plt.title(title, constants.HEADLINE_FONT)
    plt.annotate(
        file_utils.get_timestamp(),
        xy=(1, 0),
        xycoords='figure fraction',
        ha='right',
        va="bottom",
        **constants.FOOTNOTE_FONT
    )
    plt.subplots_adjust(top=0.9, bottom=0.125)
    if save:
        logging.info("Saving {0} Figure...".format(title))
        for extension in constants.PLOT_FILETYPE_LIST:
            plt.savefig("{0}/{1}/{2}.{1}".format(
                constants.PLOT_FOLDER,
                extension,
                file_utils.sanitize_filename(title)
                )
            )
    if show:
        plt.show()
    plt.clf()


def pie(plot_data, title):
    """Generate a pie chart with customized styling.

    Parameters:
        plot_data (pd.Series): Data for the pie chart.
        title (str): Title of the pie chart.

    """
    sorted_data = plot_data.sort_index()
    plt.pie(
        sorted_data,
        labels=sorted_data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=constants.CUSTOM_COLORS,
        textprops=constants.DESCRIPTION_FONT,
    )
    save_or_show_plot(title)


def line_with_mean(plot_data, mean_list, title):
    """Generate a seaborn line plot with mean annotations.

    Args:
        plot_data (pd.DataFrame): DataFrame containing data for plotting.
        mean_list (list): List of tuples with labels and corresponding mean values.
        title (str): Title for the plot.

    """
    sns.set(style="whitegrid")
    set_sns_theme()
    g = sns.displot(
        data=plot_data,
        x="Rating", kind="kde", hue="Age Group",
        common_norm=False,
        facet_kws=dict(margin_titles=True),
        aspect=1.5,
        palette=constants.CUSTOM_COLORS,
        cut=0,
        bw_adjust=0.5,
    )
    g.set(xlim=(1, 10))
    for i, (label, mean_value) in enumerate(mean_list):
        g.ax.axvline(
            x=mean_value,
            linestyle='dashed',
            linewidth=2,
            label=f'Mean ({label})',
            color=constants.CUSTOM_COLORS[i],
        )

    # Calculate the mean of both age groups
    both_mean = plot_data['Rating'].mean()

    # Plot the mean as a line curve
    sns.kdeplot(
        data=plot_data,
        x="Rating",
        common_norm=False,
        bw_adjust=1,
        cut=0,
        color=constants.CUSTOM_COLORS[-1],
        linewidth=1,
        alpha=1,
    )
    g.ax.axvline(
        x=both_mean,
        linestyle='solid',
        linewidth=10,
        alpha=0.5,
        label='Mean (Both)',
        color=constants.CUSTOM_COLORS[-1],
    )

    g.ax.set_yticklabels([f"{tick:.0%}" for tick in g.ax.get_yticks()])
    g.ax.legend()
    g.set_axis_labels(
        "Rating (Scale 1 (no/minor problem) - 10 (cannot be financed))",
        "Percent"
    )
    plt.subplots_adjust(top=0.9, bottom=0.125)
    save_or_show_plot(title)


def set_sns_theme():
    """Set seaboorn theme constants."""
    sns.set_theme(
        font=constants.STANDART_FONTSTYLE.get_family()[0],
        rc={
            'font.size': constants.DESCRIPTION_FONT["fontsize"],
            'axes.labelsize': constants.DESCRIPTION_FONT["fontsize"],
            'axes.titlesize': constants.DESCRIPTION_FONT["fontsize"],
            'xtick.labelsize': constants.DESCRIPTION_FONT["fontsize"],
            'ytick.labelsize': constants.DESCRIPTION_FONT["fontsize"],
            'legend.fontsize': constants.DESCRIPTION_FONT["fontsize"],
            'legend.title_fontsize': constants.DESCRIPTION_FONT["fontsize"],
        }
    )
