from faker import Faker
from faker.providers.date_time import Provider


def generate(data_type: str, locale: str) -> list:
    """
    Generate fake data based on the specified data_type
    """
    
    fake = Faker(locale)
    data_types = {
        'name': fake.name,
        'phone_number': fake.phone_number,
        'address': fake.address,
        'email': fake.email,
        'country': fake.country,
        'city': fake.city,
        'text': fake.text,
        'ipv4': fake.ipv4_private,
        'user_agent': fake.chrome,
        'company': fake.company,
        'credit_card': fake.credit_card_full,
        'geo': fake.location_on_land
    }
    qty = 10

    if data_type in data_types:
        fake_method = data_types[data_type]
        return [fake_method() for _ in range(qty)]
    else:
        return 'Invalid data_type'