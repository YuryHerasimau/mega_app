from typing import List
import random
from datetime import datetime
import uuid
import csv
from utils.path_generation import create_file_path, create_file_name


ID = uuid.uuid4()
DATE = datetime.today().date()
ACTIONS = ["parse", "filter", "sort"]
action = random.choice(ACTIONS)

path = create_file_path(module_name=__name__)


def generate(data: str, action: str) -> None:
    """
    Generate a configuration entry in a CSV file based on the provided data and action.

    Parameters:
    - data (str): The data to be included in the configuration.
    - action (str): The action associated with the configuration (e.g., 'parse', 'filter', 'sort').

    Returns:
    - None: The function does not return anything.

    This function creates a CSV file 'config.csv' and writes a configuration entry with the following headers:
    - 'id': A unique identifier generated using uuid4.
    - 'date': The current date.
    - 'action': The randomly chosen action from ['parse', 'filter', 'sort'].
    - 'data': The data provided as input to the function.

    Example Usage:
    generate(data="Sample data", action="filter")
    """

    file_name = f"{ID}_{DATE}_{action}.csv"
    file_path = create_file_name(path=path, file_name=file_name)

    with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
        headers = ["id", "date", "action", "data"]
        writer = csv.DictWriter(csv_file, headers)
        config_data = {"id": ID, "date": DATE, "action": action, "data": data}
        writer.writeheader()
        writer.writerow(config_data)


def create_or_update_csv(data: List[str], file_name: str, fieldnames: List[str]) -> None:
    """
    Create or update a CSV file with the provided data.

    Parameters:
    - data: A list of strings containing the data to be written to the CSV file.
    - file_name: The name of the CSV file to be created or updated.
    - fieldnames: A list of strings representing the field names in the CSV file.
    """
    
    file_name = f"{file_name}.csv"
    file_path = create_file_name(path=path, file_name=file_name)

    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames)
        csv_writer.writeheader()
        csv_writer.writerow(dict(zip(fieldnames, data)))
