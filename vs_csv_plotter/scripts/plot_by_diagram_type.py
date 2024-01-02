"""This module provides utility functions for creating charts."""
# Import built-in modules
import logging

# Import local modules
import constants
from scripts import file_utils

# Import third-party modules
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import make_interp_spline


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
        xycoords="figure fraction",
        ha="right",
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
    plt.rcParams["font.size"] = constants.DESCRIPTION_FONT["fontsize"]
    plt.rcParams["font.family"] = constants.STANDART_FONTSTYLE.get_family()[0]
    sorted_data = plot_data.sort_index()
    _, _, autopct = plt.pie(
        sorted_data,
        labels=sorted_data.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=constants.CUSTOM_COLORS,
        textprops={"color": constants.TEXTCOLOR},
    )
    for autopct in autopct:
        plt.annotate(
            autopct.get_text(),
            xy=autopct.get_position(),
            xycoords="data",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", facecolor=constants.BACKGROUNDCOLOR, alpha=0.3),
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
    mean_list = None,
    mean = None
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
            sns.lineplot(
                data=subset_data[x_axis_key], 
                color=color,
                label=f"{plot_data_key} {plot_data_label}",
                linewidth=constants.PLOTWIDTH/4
            )
    x = np.arange(len(plot_data[x_axis_key]))
    y = plot_data[x_axis_key]
    spl = make_interp_spline(x, y, k=3)
    smoothed_x = np.linspace(x.min(), x.max(), 300)
    smoothed_y = spl(smoothed_x)
    sns.lineplot(
        x=smoothed_x,
        y=smoothed_y,
        color=constants.CUSTOM_COLORS[-1],
        label="Average Smoothed",
        linewidth=constants.PLOTWIDTH/4
    )
    if mean_list:
        for i, (label, mean_value) in enumerate(mean_list):
            plt.axvline(
                x=mean_value,
                linestyle="dashed",
                linewidth=constants.PLOTWIDTH/4,
                label=f"Mean ({label})",
                color=constants.CUSTOM_COLORS[i],
            )
    if mean:
        plt.axvline(
            x=mean,
            linestyle="dashed",
            linewidth=constants.PLOTWIDTH/2,
            alpha=0.5,
            label="Mean",
            color=constants.CUSTOM_COLORS[-1],
        )
    plt.xlim(1, 10)
    plt.ylim(0, 0.25)
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


def plot_line_chart(row_index, df, categories, title, x_value, y_value, x_label, y_label, xlim=(1, 10), ylim=(0, 1)):
    """Generate plot of a line chart.
    Args:
        row_index (str): The column in the DataFrame used as the category.
        df (pd.DataFrame): The DataFrame containing the data.
        categories (list): List of categories for the chart.
        title (str): Title of the chart.
        x_value (str): The column in the DataFrame used as the x-axis values.
        y_value (str): The column in the DataFrame used as the y-axis values.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        xlim (tuple): Tuple specifying the x-axis limits (default: (1, 10)).
        ylim (tuple): Tuple specifying the y-axis limits (default: (0, 1)).
    """
    plt.figure(figsize=(constants.PLOTHEIGHT, constants.PLOTWIDTH))
    sns.set(style="darkgrid")
    set_sns_theme()

    for i, category in enumerate(categories):
        plt.plot(df[x_value],
                 df[y_value],
                 linewidth=constants.PLOTWIDTH/4,
                 label=category,
                 color=constants.CUSTOM_COLORS[i]
                 )

    plt.xlim(*xlim)
    plt.ylim(*ylim)
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


def plot_stack_chart(row_index, df, categories, title, x_value, y_value, x_label, y_label, xlim=(1, 10), ylim=(0, 1)):
    """Generate a stack chart.
    Args:
        row_index (str): The column in the DataFrame used as the category.
        df (pd.DataFrame): The DataFrame containing the data.
        categories (list): List of categories for the chart.
        title (str): Title of the chart.
        x_value (str): The column in the DataFrame used as the x-axis values.
        y_value (str): The column in the DataFrame used as the y-axis values.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        xlim (tuple): Tuple specifying the x-axis limits (default: (1, 10)).
        ylim (tuple): Tuple specifying the y-axis limits (default: (0, 1)).
    """
    plt.figure(figsize=(constants.PLOTHEIGHT, constants.PLOTWIDTH))
    sns.set(style="darkgrid")
    set_sns_theme()
    x_data = df[x_value]
    y_data = [
        np.interp(
            x_data, df[df[row_index] == category][x_value],
            df[df[row_index] == category][y_value]
        ) for category in categories
    ]
    hatch_patterns = ["//", "\\", "||"]
    for i, category_data in enumerate(y_data):
        if i == 0:
            plt.fill_between(
                x_data,
                0,
                category_data,
                label=categories[i],
                color=constants.CUSTOM_COLORS[i],
                hatch = hatch_patterns[i]
            )
        else:
            plt.fill_between(
                x_data,
                np.sum(y_data[:i],axis=0),
                np.sum(y_data[:i+1], axis=0),
                label=categories[i],
                color=constants.CUSTOM_COLORS[i],
                hatch = hatch_patterns[i]
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
                "font.size",
                "axes.labelsize",
                "axes.titlesize",
                "xtick.labelsize",
                "ytick.labelsize",
                "legend.fontsize",
                "legend.title_fontsize"
            ]
        }
    )
