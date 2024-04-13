import io
import re
from PIL import Image
import requests
from requests.exceptions import HTTPError
from typing import List, Union, Dict
from utils.path_generation import create_file_path, create_file_name
from config import apikey


def process_coordinates(coordinates: List[tuple]) -> List[str]:
    """Process the list of coordinates and invert them.

    Args:
    - coordinates (List[tuple]): List of coordinates in the format (latitude,longitude).
    E.g. [(55.805674,37.594479),(55.805674,37.594479), ...]
    
    Returns:
    - List[str]: A list of inverted coordinates in the format 'latitude,longitude'.
    E.g. ['37.594479,55.805674', '37.594479,55.805674', ...]
    """

    pattern = r"\((\d+\.\d+),(\d+\.\d+)\)"
    coords = re.findall(pattern, coordinates)
    inverted_coordinates = [f"{coord[1]},{coord[0]}" for coord in coords]
    return inverted_coordinates


def get_map(coordinates: List[tuple]) -> bytes:
    """Generate an image of the courier's route on the map.

    Args:
    - coordinates (List[tuple]): List of coordinates in the format (latitude, longitude).

    Returns:
    - bytes: The image data of the courier's route.
    """

    base_url = "https://static-maps.yandex.ru/v1"
    coordinates_list = process_coordinates(coordinates)
    if coordinates_list is not None:
        try:
            parameters = {
                "lang": "ru_RU",
                "pt": f"{coordinates_list[0]},pm2am~{coordinates_list[-1]},pm2bm",
                "pl": ",".join(coordinates_list),
                # API key for accessing the Yandex Static API mapping service
                "apikey": apikey,
            }
            response = requests.get(base_url, params=parameters)
            response.raise_for_status()
            if response.status_code == 200:
                path = create_file_path(module_name=__name__)
                file_path = create_file_name(path=path, file_name="my_map.png")
                in_memory_file = io.BytesIO(response.content)
                im = Image.open(in_memory_file)
                im.save(file_path)
                return response.content

        except HTTPError as ex:
            raise SystemExit(ex)
        except Exception as e:
            print(f"An error occurred while processing the request: {e}")
    