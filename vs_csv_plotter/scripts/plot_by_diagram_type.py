# import build-in modules
import os

# Import local modules
import constants

# Import third-party modules
from matplotlib import pyplot as plt
from datetime import datetime


def pie(data, title, save=constants.SAVE_PLOT, show=constants.SHOW_PLOT):
    plt.clf()
    plt.pie(
        data, 
        labels=data.index, 
        autopct="%1.1f%%", 
        startangle=90,
        colors=constants.CUSTOM_COLORS, 
        textprops=constants.DESCRIPTION_FONT
    )
    plt.title(title, constants.HEADLINE_FONT)
    plt.annotate(
            str(datetime.now()),
            xy = (0.5, -0.1),
            xycoords='axes fraction',
            ha='center',
            va="center",
            fontsize=constants.FOOTNOTE_FONT["fontsize"]
    )
    if save:
        plt.savefig("{0}/{1}.svg".format(constants.PLOT_FOLDER, title.replace(" ", "_")))
    if show:
        plt.show()
        