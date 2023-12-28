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
    if not os.path.exists(constants.PLOT_FOLDER):
        os.makedirs(constants.PLOT_FOLDER)
        

def concat_from_folder(folder_path=constants.DATA_FOLDER):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("No CSV Files in Folder {0}.".format(os.path.abspath(folder_path)))
    df_list = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df


@cached(cache=TTLCache(maxsize=1024, ttl=_CACHE_TIMEOUT))
def get_timestamp(folder_path=constants.DATA_FOLDER):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    newest_timestamp = None
    for file in files:
        file_path = os.path.join(folder_path, file)
        timestamp_seconds = os.path.getmtime(file_path)
        timestamp_human_readable = pd.to_datetime(timestamp_seconds, unit='s')
        if newest_timestamp is None or timestamp_human_readable > newest_timestamp:
            newest_timestamp = timestamp_human_readable
    return newest_timestamp

def sanitize_filename(name):
    save_name = re.sub(r"[^a-zA-Z0-9_-]", "", name.replace(" ", "_"))
    return save_name
