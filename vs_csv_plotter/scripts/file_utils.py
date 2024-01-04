"""Functions for preparing, processing, and caching data from CSV files."""
# Import built-in modules
import locale
import logging
import os
import re
import getpass
from datetime import datetime

# Import local modules
import constants

# Import third-party modules
from cachetools import TTLCache, cached
import pandas as pd
import requests


# 10 minutes in seconds.
_CACHE_TIMEOUT = 600
logging.basicConfig(level=logging.INFO)


def prepare_plot_folder():
    """Create the plot folder if it does not exist."""
    logging.info("Prepared Plot folder")
    os.makedirs(constants.PLOT_FOLDER, exist_ok=True)
    for extension in constants.PLOT_FILETYPE_LIST:
        os.makedirs(
            os.path.join(constants.PLOT_FOLDER, extension),
            exist_ok=True
        )
        print("created", os.path.join(constants.PLOT_FOLDER, extension))


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
        timestamp = pd.to_datetime(timestamp_seconds, unit="s")
        if newest_timestamp is None or timestamp > newest_timestamp:
            newest_timestamp = timestamp
    return "CSV File Timestamp: {0} UTC".format(
        newest_timestamp.strftime("%d.%m.%Y - %H:%M:%S"),
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


def download_file(url, folder_path, username, password):
    """Downloads a file from a given URL and saves it to a specified folder.

    Parameters:
        url (str): The URL of the file to download.
        folder_path (str): The path of the folder where the file will be saved.
        username (str): The username for authentication.
        password (str): The password for authentication.

    """
    response = requests.get(url, auth=(username, password), timeout=20)
    file_name = "{0}.csv".format(url.split("/")[-1])
    with open(f"{folder_path}/{file_name}", "wb") as file:
        file.write(response.content)


def download_csv_data():
    """Prompts the user for their username and password, then downloads CSV files from list.

    URLs are defined in `constants.CSV_DOWNLOAD_LIST`, files are saved in `constants.DATA_FOLDER`.

    """
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    for url in constants.CSV_DOWNLOAD_LIST:
        download_file(url, constants.DATA_FOLDER, constants.USERNAME, constants.PASSWORD)


def convert_timestamp(timestamp):
    """Convert String in CSV to valid Timestamp.
    
    Args:
        timestamp (str): CSV Timestamp
        
    Returns:
        timestamp (str): Timestamp which can be used for plotting
    """
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
    pattern = re.compile(r"\w+, (?P<day>\d{1,2})\. (?P<month>\w+) (?P<year>\d{4}) um (?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}) GMT\+0:00")
    match = re.match(pattern, timestamp)
    if not match:
        print(f"Timestamp {timestamp} does not match the expected format.")
        locale.setlocale(locale.LC_TIME, "C")
        return None
    month_map = {
        "Januar": 1, "Februar": 2, "März": 3, "April": 4, "Mai": 5, "Juni": 6,
        "Juli": 7, "August": 8, "September": 9, "Oktober": 10, "November": 11, "Dezember": 12
    }
    dt = datetime(
        int(match.group("year")),
        month_map[match.group("month")],
        int(match.group("day")),
        int(match.group("hour")),
        int(match.group("minute")),
        int(match.group("second"))
    )
    locale.setlocale(locale.LC_TIME, "C")
    return dt

