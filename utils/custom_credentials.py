import random
import string


def generate_password() -> str:
    """
    Generate password from random lowercase letters and digits
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(10))


def multiple(number: int) -> list:
    """
    Generate a pair of login and password based on the input number
    """
    username_base = 'user'
    credentials = []
    for i in range(number):
        credentials.append(f"{username_base}{i}/{generate_password()}")
    return credentials
