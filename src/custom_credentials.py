import random
import string


def generate_password(password_length: str) -> str:
    """
    Generate a random password of a specified length using letters and digits.

    Parameters:
    - password_length (int): The length of the password to generate.

    Returns:
    - password (str): The randomly generated password.
    """
    
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for i in range(password_length))
    return password


def multiple(number_of_passwords: int, password_length: str, username_base: str) -> list:
    """
    Generate multiple credentials consisting of a username base and a random password.

    Parameters:
    - number_of_passwords (int): The number of credentials to generate.
    - password_length (int): The length of each password.
    - username_base (str): The base username to use in the credentials.

    Returns:
    - list: A list of credentials in the format 'username_base{n}/password'.
    """
    
    credentials = []
    for n in range(number_of_passwords):
        credentials.append(f"{username_base}{n}/{generate_password(password_length)}")
    return credentials
