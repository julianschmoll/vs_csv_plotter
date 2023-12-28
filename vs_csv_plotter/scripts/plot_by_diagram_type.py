# Import local modules
import constants
from scripts import file_utils

# Import third-party modules
from matplotlib import pyplot as plt


def save_or_show_plot(title, save=constants.SAVE_PLOT, show=constants.SHOW_PLOT):
    plt.title(title, constants.HEADLINE_FONT)
    plt.annotate(
            str(file_utils.get_timestamp()),
            xy = (0.5, -0.1),
            xycoords='axes fraction',
            ha='center',
            va="center",
            **constants.FOOTNOTE_FONT
    )
    if save:
        plt.savefig("{0}/{1}.svg".format(constants.PLOT_FOLDER, file_utils.sanitize_filename(title)))
    if show:
        plt.show()
    plt.clf()


def pie(data, title):
    sorted_data = data.sort_index()
    plt.pie(
        sorted_data, 
        labels=sorted_data.index, 
        autopct="%1.1f%%", 
        startangle=90,
        colors=constants.CUSTOM_COLORS, 
        textprops=constants.DESCRIPTION_FONT
    )
    save_or_show_plot(title)
