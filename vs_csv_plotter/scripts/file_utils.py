"""This module provides functions for preparing, processing, and caching data
from CSV files.
"""
# Import built-in modules
import os
import logging
import re

# Import local modules
import constants

# Import third party modiles
from cachetools import TTLCache
from cachetools import cached
import pandas as pd

# 10 minutes in seconds.
_CACHE_TIMEOUT = 600
LOGGER = logging.getLogger(__name__)


def prepare_plot_folder():
    """Create the plot folder if it does not exist."""
    if not os.path.exists(constants.PLOT_FOLDER):
        os.makedirs(constants.PLOT_FOLDER)


def concat_from_folder(folder_path=constants.DATA_FOLDER):
    """Concatenate DataFrames from CSV files in a specified folder.

    Parameters:
        folder_path (str, optional): Path to the folder containing CSV files.
                                     Defaults to constants.DATA_FOLDER.

    Returns:
        pd.DataFrame: Combined DataFrame containing data from all CSV files.
    """
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("No CSV Files in Folder {0}.".format(
            os.path.abspath(folder_path))
        )
    df_list = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df


def replace_ger_eng(csv_data):
    """Replace German with English labels.

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    Returns:
        pd.DataFrame: DataFrame with replaced labels.
    """
    csv_data.replace({"Ja": "Yes", "Nein": "No"}, inplace=True)
    return csv_data


@cached(cache=TTLCache(maxsize=1024, ttl=_CACHE_TIMEOUT))
def get_timestamp(folder_path=constants.DATA_FOLDER):
    """Retrieve the timestamp of the newest CSV file in a folder.

    Parameters:
        folder_path (str, optional): Path to the folder containing CSV files.
                                     Defaults to constants.DATA_FOLDER.

    Returns:
        str: Timestamp formatted as "CSV File Timestamp.
    """
    files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    newest_timestamp = None
    for file in files:
        file_path = os.path.join(folder_path, file)
        timestamp_seconds = os.path.getmtime(file_path)
        timestamp = pd.to_datetime(timestamp_seconds, unit='s')
        if newest_timestamp is None or timestamp > newest_timestamp:
            newest_timestamp = timestamp
    return "CSV File Timestamp: {0}".format(
        newest_timestamp.strftime('%d.%m.%Y - %H:%M:%S')
    )


def sanitize_filename(name):
    """Sanitize a string to be suitable as a filename.

    Parameters:
        name (str): The input string.

    Returns:
        str: The sanitized string.
    """
    save_name = re.sub(r"[^a-zA-Z0-9_-]", "", name.replace(" ", "_"))
    return save_name
