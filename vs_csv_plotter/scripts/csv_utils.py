# Import built-in modules
import os
import logging

# Import local modules
import constants

# Import third party modiles
import pandas as pd

LOGGER = logging.getLogger(__name__)

def concat_from_folder(folder_path=constants.DATA_FOLDER):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not csv_files:
        LOGGER.error("No CSV Files in Folder")
        return None
    df_list = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def set_timestamp(folder_path=constants.DATA_FOLDER):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    newest_timestamp = None
    for file in files:
        file_path = os.path.join(folder_path, file)
        timestamp_seconds = os.path.getmtime(file_path)
        timestamp_human_readable = pd.to_datetime(timestamp_seconds, unit='s')
        if newest_timestamp is None or timestamp_human_readable > newest_timestamp:
            newest_timestamp = timestamp_human_readable
    constants.TIMESTAMP = newest_timestamp