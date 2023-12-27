# import build-in modules
import os

# Import local modules
import constants

# Import third-party modules
from matplotlib import pyplot as plt
from datetime import datetime


def prepare_plot_folder():
    if not os.path.exists(constants.PLOT_FOLDER):
        os.makedirs(constants.PLOT_FOLDER)
    
def plot_age_distribution(csv_data, save=constants.SAVE_PLOT, show=constants.SHOW_PLOT):
    age_counts = csv_data["Altersklasse"].value_counts()
    age_percent = age_counts / age_counts.sum() * 100
    plt.pie(
        age_percent, 
        labels=age_percent.index, 
        autopct="%1.1f%%", 
        startangle=90,
        colors=constants.CUSTOM_COLORS, 
        textprops=constants.DESCRIPTION_FONT
    )
    plt.title("Percentage Distribution of Age", constants.HEADLINE_FONT)
    plt.annotate(
            str(datetime.now()),
            xy = (0.5, -0.1),
            xycoords='axes fraction',
            ha='center',
            va="center",
            fontsize=constants.FOOTNOTE_FONT["fontsize"]
    )

    if save:
        plt.savefig("{0}/age_distribution.svg".format(constants.PLOT_FOLDER))
    if show:
        plt.show()
