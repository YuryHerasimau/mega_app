import random
from datetime import datetime
import uuid
import csv


ID = uuid.uuid4()
DATE = datetime.today().date()
ACTIONS = ['parse', 'filter', 'sort']
action = random.choice(ACTIONS)


with open('data.txt') as data_file:
    data = data_file.read()


def generate(data, action):
    with open('config.csv', 'w', newline='') as csv_file:
        headers = ['id', 'date', 'action', 'data']
        writer = csv.DictWriter(csv_file, headers)
        config_data = {'id': ID, 'date': DATE, 'action': action, 'data': data}
        writer.writeheader()
        writer.writerow(config_data)


if __name__ == '__main__':
    generate(data, action)