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
    plt.gca().xaxis.label.set_color(constants.TEXTCOLOR)
    plt.gca().yaxis.label.set_color(constants.TEXTCOLOR)
    plt.gca().title.set_color(constants.TEXTCOLOR)

    if save:
        for extension in constants.PLOT_FILETYPE_LIST:
            fig_file = "{0}/{1}/{2}.{1}".format(
                constants.PLOT_FOLDER,
                extension,
                file_utils.sanitize_filename(title)
            )
            plt.savefig(fig_file, facecolor=constants.BACKGROUNDCOLOR)
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
    _, _, autopct = plt.pie(
        sorted_data,
        labels=sorted_data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=constants.CUSTOM_COLORS,
        textprops={'color': constants.TEXTCOLOR},
    )
    for autopct in autopct:
        plt.annotate(
            autopct.get_text(),
            xy=autopct.get_position(),
            xycoords='data',
            ha='center',
            va='center',
            bbox=dict(boxstyle='round', facecolor=constants.BACKGROUNDCOLOR, alpha=0.3),
            color = constants.TEXTCOLOR
        )
    plt.gca().set_facecolor(constants.BACKGROUNDCOLOR) 
    save_or_show_plot(title)


def line_with_mean(
    plot_data,
    x_axis_key,
    title,
    plot_data_key = None,
    x_value_label = "x",
    y_value_label = "y",
    mean_list = [],
):
    """Generate a seaborn line plot with mean annotations.

    Args:
        plot_data (pd.DataFrame): DataFrame containing data for plotting.
        mean_list (list): List of tuples with labels and corresponding mean values.
        title (str): Title for the plot.

    """
    plt.figure(figsize=(constants.PLOTHEIGHT, constants.PLOTWIDTH))
    sns.set(style="darkgrid") 
    set_sns_theme()
    if plot_data_key:
        for plot_data_label, color in zip(plot_data[plot_data_key].unique(), constants.CUSTOM_COLORS):
            subset_data = plot_data[plot_data[plot_data_key] == plot_data_label]
            sns.kdeplot(
                data=subset_data,
                x=x_axis_key,
                common_norm=False,
                color=color,
                label=f'{plot_data_key} {plot_data_label}',
                cut=0,
                bw_adjust=0.75,
                linewidth=constants.PLOTWIDTH/4,
            )
    both_mean = plot_data[x_axis_key].mean()
    sns.kdeplot(
        data=plot_data,
        x=x_axis_key,
        common_norm=False,
        bw_adjust=1.5,
        cut=0,
        color=constants.CUSTOM_COLORS[-1],
        linewidth=constants.PLOTWIDTH/4,
        alpha=1,
        label="Average smooted"
    )
    if mean_list:
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
    plt.gca().xaxis.label.set_color(constants.TEXTCOLOR)
    plt.gca().yaxis.label.set_color(constants.TEXTCOLOR)
    plt.gca().title.set_color(constants.TEXTCOLOR)
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_color(constants.TEXTCOLOR)
    legend.get_frame().set_facecolor(constants.BACKGROUNDCOLOR)
    plt.tick_params(axis="x", colors=constants.TEXTCOLOR)
    plt.tick_params(axis="y", colors=constants.TEXTCOLOR)
    plt.xlabel(x_value_label, color=constants.TEXTCOLOR)
    plt.ylabel(y_value_label, color=constants.TEXTCOLOR)
    plt.gca().set_facecolor(constants.BACKGROUNDCOLOR)
    plt.subplots_adjust(top=0.9, bottom=0.125)
    save_or_show_plot(title)


def plot_line_chart(row_index, df, categories, title, x_value, y_value, x_label, y_label, xlim=(1, 10), ylim=(0,1)):
    plt.figure(figsize=(constants.PLOTHEIGHT, constants.PLOTWIDTH))
    sns.set(style="darkgrid")
    set_sns_theme()
    for i, category in enumerate(categories):
        category_data = df[df[row_index] == category]
        plt.plot(category_data[x_value],
                 category_data[y_value],
                 linewidth=constants.PLOTWIDTH/4,
                 label=category,
                 color=constants.CUSTOM_COLORS[i]
        )
    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.yticks(list(plt.yticks()[0]), [f"{tick:.0%}" for tick in plt.yticks()[0]])
    plt.gca().xaxis.label.set_color(constants.TEXTCOLOR)
    plt.gca().yaxis.label.set_color(constants.TEXTCOLOR)
    plt.gca().title.set_color(constants.TEXTCOLOR)
    legend = plt.legend()
    for text in legend.get_texts():
        text.set_color(constants.TEXTCOLOR)
    legend.get_frame().set_facecolor(constants.BACKGROUNDCOLOR)
    plt.tick_params(axis="x", colors=constants.TEXTCOLOR)
    plt.tick_params(axis="y", colors=constants.TEXTCOLOR)
    plt.xlabel(x_label, color=constants.TEXTCOLOR)
    plt.ylabel(y_label, color=constants.TEXTCOLOR)
    plt.gca().set_facecolor(constants.BACKGROUNDCOLOR)
    plt.subplots_adjust(top=0.9, bottom=0.125)
    save_or_show_plot(title)


def set_sns_theme():
    """Set seaborn theme constants."""
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
