import json


def read(file_name: str, fields_list: list) -> list:
    """
    Read JSON data from a file and extract specific fields for each object
    """

    with open(file_name, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)['couriers']
    
    result = []
    for obj in json_data:
        entry = {} # Создаем новый словарь для каждого объекта json
        for field in fields_list:
            entry[field] = obj.get(field)
        result.append(entry)
    return result
