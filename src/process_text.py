import requests
from config import API_NINJAS_KEY


def compute_similarity(first_input_text: str, second_input_text: str) -> dict:
    """
    Returns a similarity score between 0 and 1 (1 is similar and 0 is dissimilar) of two given texts.

    Args:
    - first_input_text (str): The first text for comparison.
    - second_input_text (str): The second text for comparison.

    Returns:
    - dict: A dictionary containing the similarity score between the two texts.
    """

    body = {'text_1': first_input_text, 'text_2': second_input_text}
    api_url = 'https://api.api-ninjas.com/v1/textsimilarity'
    response = requests.post(api_url, headers={'X-Api-Key': API_NINJAS_KEY}, json=body)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None