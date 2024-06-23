import requests
from bs4 import BeautifulSoup
from pprint import pprint


def check_link_validity(url):
    try:
        response = requests.get(url)  # head
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def parse_links(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    links_status = {link: check_link_validity(link) for link in links}
    # pprint(links_status)
    return links_status
