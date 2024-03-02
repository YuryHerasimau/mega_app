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
    entry = {}

    for obj in json_data:
        for field in FIELDS_LIST:
            entry[field] = obj.get(field)
        result.append(entry)
    return result


# if __name__ == "__main__":
#     print(read(FILENAME, FIELDS_LIST))