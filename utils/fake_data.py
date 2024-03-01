import json
from faker import Faker
from faker.providers import internet, credit_card


def generate(data_type: str) -> str | list:
    """
    Generate fake data based on the specified data_type
    """
    fake = Faker()

    if data_type == 'name':
        return fake.name()

    if data_type == 'address':
        return fake.address() #.split('\n')

    if data_type == 'text':
        return fake.text()

    if data_type == 'ipv4':
        fake.add_provider(internet)
        ip_list = []
        for _ in range(5):
            ip_list.append(fake.ipv4_private())
        return ip_list

    if data_type == 'user_agent':
        user_agents_list = []
        for _ in range(5):
            user_agents_list.append(fake.chrome())
        return user_agents_list

    if data_type == 'credit_card':
        return fake.credit_card_full() #.split('\n')

    if data_type == 'geo':
        geo = fake.location_on_land()
        return json.dumps(geo)