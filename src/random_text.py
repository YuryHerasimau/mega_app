import random
import string


def generate(qty_chars: int, random_length: bool) -> str:
    """
    Generate a random text with the specified quantity of characters.

    Args:
    - qty_chars (int): The desired quantity of characters for the random text.
    - random_length (bool): Flag to indicate whether to generate a random length text.

    Returns:
    - str: The randomly generated text with the specified quantity of characters.
    """

    if random_length:
        qty_chars = random.randint(5, 5000)  # Генерация случайного числа символов
    letters = string.ascii_letters + string.digits + string.punctuation
    random_text = "".join(random.choice(letters) for i in range(qty_chars))
    # while len(random_text) < qty_chars:
    #     random_text += random.choice(letters)
    return random_text
