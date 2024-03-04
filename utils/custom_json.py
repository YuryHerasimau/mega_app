import json


FILENAME = "couriers.json"
FIELDS_LIST = ["user_id", "external_id", "mood", "user"]


def read(FILENAME: str, FIELDS_LIST: list) -> list:
    """
    Read JSON data from a file and extract specific fields for each object
    """
    with open(FILENAME, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)['couriers']
    
    result = []
    for obj in json_data:
        entry = {} # Создаем новый словарь для каждого объекта json
        for field in FIELDS_LIST:
            entry[field] = obj.get(field)
        result.append(entry)
    return result
