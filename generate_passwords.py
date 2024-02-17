import random
import string
# import secrets


def generate_password():
    # letters = string.ascii_lowercase
    # return ''.join(random.choice(letters) for _ in range(10))
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(10))


def multiple(number):
    username_base = 'user'
    credentials = []
    for i in range(number):
        credentials.append(f"{username_base}{i}/{generate_password()}")
    print(credentials)
    return credentials