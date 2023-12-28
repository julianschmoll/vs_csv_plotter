"""This module provides utility functions for creating charts."""
# Import built-in modules
import logging
# Import local modules
import constants
# Import third-party modules
from matplotlib import pyplot as plt
from scripts import file_utils

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
        xy=(0.5, -0.1),
        xycoords='axes fraction',
        ha='center',
        va="center",
        **constants.FOOTNOTE_FONT
    )
    if save:
        logging.info("Saving {0} Figure...".format(title))
        plt.savefig("{0}/{1}.svg".format(
            constants.PLOT_FOLDER,
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
