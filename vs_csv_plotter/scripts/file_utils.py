"""Functions for preparing, processing, and caching data from CSV files."""
# Import built-in modules
import logging
import os
import re

# Import local modules
import constants
import pandas as pd
# Import third party modiles
from cachetools import TTLCache, cached

# 10 minutes in seconds.
_CACHE_TIMEOUT = 600
logging.basicConfig(level=logging.INFO)


def prepare_plot_folder():
    """Create the plot folder if it does not exist."""
    if not os.path.exists(constants.PLOT_FOLDER):
        logging.info("Prepared Plot folder")
        os.makedirs(constants.PLOT_FOLDER)


def concat_from_folder(folder_path=constants.DATA_FOLDER):
    """Concatenate DataFrames from CSV files in a specified folder.

    Parameters:
        folder_path (str, optional): Path to the folder containing CSV files.

    Raises:
        FileNotFoundError: If no CSV file is found in folder.

    Returns:
        pd.DataFrame: Combined DataFrame containing data from all CSV files.
    """
    csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("No CSV Files in Folder {0}.".format(
            os.path.abspath(folder_path)
            )
        )
    df_list = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True)


def replace_ger_eng(csv_data):
    """Replace German with English labels.

    Parameters:
        csv_data (pd.DataFrame): DataFrame containing survey data.

    Returns:
        pd.DataFrame: DataFrame with replaced labels.
    """
    csv_data.replace({
        "Ja": "Yes",
        "Nein": "No",
        "Unentschlossen": "Don't know",
    }, inplace=True)
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
        file
        for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file))
    ]
    newest_timestamp = None
    for file in files:
        timestamp_seconds = os.path.getmtime(os.path.join(folder_path, file))
        timestamp = pd.to_datetime(timestamp_seconds, unit='s')
        if newest_timestamp is None or timestamp > newest_timestamp:
            newest_timestamp = timestamp
    return "CSV File Timestamp: {0}".format(
        newest_timestamp.strftime('%d.%m.%Y - %H:%M:%S'),
    )


def sanitize_filename(name):
    """Sanitize a string to be suitable as a filename.

    Parameters:
        name (str): The input string.

    Returns:
        str: The sanitized string.
    """
    tmp_name = name.replace(">", "over ")
    tmp_name = tmp_name.replace("<", "below ")
    tmp_name = tmp_name.replace("≤", "below or equal ")
    tmp_name = tmp_name.replace(" ", "_")
    return re.sub("[^a-zA-Z0-9_-]", "", tmp_name.lower())
