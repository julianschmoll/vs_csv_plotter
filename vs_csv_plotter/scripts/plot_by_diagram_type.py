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


def save_or_show_plot(title, save=constants.SAVE_PLOT, show=constants.SHOW_PLOT):
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
        for extension in constants.PLOT_FILETYPE_LIST:
            fig_file = "{0}/{1}/{2}.{1}".format(
                constants.PLOT_FOLDER,
                extension,
                file_utils.sanitize_filename(title)
            )
            plt.savefig(fig_file)
            logging.info("Saved {0}".format(fig_file))
    if show:
        plt.show()

    plt.clf()


def pie(plot_data, title):
    """Generate a pie chart with customized styling.

    Parameters:
        plot_data (pd.Series): Data for the pie chart.
        title (str): Title of the pie chart.

    """
    plt.figure(figsize=(constants.PLOTHEIGHT, constants.PLOTWIDTH))
    plt.rcParams['font.size'] = constants.DESCRIPTION_FONT['fontsize']
    plt.rcParams['font.family'] = constants.STANDART_FONTSTYLE.get_family()[0]
    sorted_data = plot_data.sort_index()
    plt.pie(
        sorted_data,
        labels=sorted_data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=constants.CUSTOM_COLORS,
    )
    save_or_show_plot(title)


def line_with_mean(plot_data, mean_list, title):
    """Generate a seaborn line plot with mean annotations.

    Args:
        plot_data (pd.DataFrame): DataFrame containing data for plotting.
        mean_list (list): List of tuples with labels and corresponding mean values.
        title (str): Title for the plot.

    """
    plt.figure(figsize=(constants.PLOTHEIGHT, constants.PLOTWIDTH))
    sns.set(style="whitegrid")
    set_sns_theme()

    for age_group, color in zip(plot_data['Age Group'].unique(), constants.CUSTOM_COLORS):
        subset_data = plot_data[plot_data['Age Group'] == age_group]
        sns.kdeplot(
            data=subset_data,
            x="Rating",
            common_norm=False,
            color=color,
            label=f'Age Group {age_group}',
            cut=0,
            bw_adjust=0.75,
            linewidth=constants.PLOTWIDTH/4,
        )
    both_mean = plot_data['Rating'].mean()
    sns.kdeplot(
        data=plot_data,
        x="Rating",
        common_norm=False,
        bw_adjust=1.5,
        cut=0,
        color=constants.CUSTOM_COLORS[-1],
        linewidth=constants.PLOTWIDTH/4,
        alpha=1,
        label="All ages smooted"
    )
    for i, (label, mean_value) in enumerate(mean_list):
        plt.axvline(
            x=mean_value,
            linestyle='dashed',
            linewidth=constants.PLOTWIDTH/4,
            label=f'Mean ({label})',
            color=constants.CUSTOM_COLORS[i],
        )
    plt.axvline(
        x=both_mean,
        linestyle='dashed',
        linewidth=constants.PLOTWIDTH/2,
        alpha=0.5,
        label='Mean',
        color=constants.CUSTOM_COLORS[-1],
    )

    plt.xlim(1, 10)
    plt.yticks([tick for tick in plt.yticks()[0]], [f"{tick:.0%}" for tick in plt.yticks()[0]])
    plt.legend()
    plt.xlabel("Rating (Scale 1 (no/minor problem) - 10 (cannot be financed))")
    plt.ylabel("Percent")

    plt.subplots_adjust(top=0.9, bottom=0.125)
    save_or_show_plot(title)


def set_sns_theme():
    """Set seaboorn theme constants."""
    sns.set_theme(
        font=constants.STANDART_FONTSTYLE.get_family()[0],
        rc={
            key: constants.DESCRIPTION_FONT["fontsize"]
            for key in [
                'font.size',
                'axes.labelsize',
                'axes.titlesize',
                'xtick.labelsize',
                'ytick.labelsize',
                'legend.fontsize',
                'legend.title_fontsize'
            ]
        }
    )
