from typing import List
import os
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from utils.path_generation import create_file_path, create_file_name


path = create_file_path(module_name=__name__)


def get_url(url: str) -> str:
    """
    Get the HTML content of the specified URL using a headless Chrome browser.

    :param url: The URL to fetch the HTML content from.
    :return: The HTML content of the page.
    """

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    print("Loading...")
    # get the HTML code of the page after it has loaded
    res = driver.execute_script("return document.documentElement.outerHTML")
    return res


def get_img_links(res: str) -> List[str]:
    """
    Extract image links from the HTML content.

    :param res: The HTML content to parse for image links.
    :return: A list of image links found in the HTML content.
    """

    soup = BeautifulSoup(res, "lxml")
    imglinks = soup.find_all("img", src=True)
    return imglinks


def download_img(img_link: str, start_index: int = 1) -> None:
    """
    Download an image from the given image link and save it to a file.

    :param img_link: The URL of the image to download.
    :param start_index: The starting index for naming the downloaded image file.
    """

    try:
        extensions = [".jpeg", ".jpg", ".png", ".gif"]
        extension = ".jpg"
        for image_extension in extensions:
            if img_link.find(image_extension) > 0:
                extension = image_extension
                break
        img_data = requests.get(img_link).content

        file_name = str(start_index) + extension
        file_path = create_file_name(path=path, file_name=file_name)

        with open(file_path, "wb+") as f:
            f.write(img_data)
        f.close()
    except Exception:
        pass


def parse(url: str, start_index: int = 1) -> None:
    """
    Parse the given URL to extract image links and download the images.

    :param url: The URL to parse image links.
    :param start_index: The starting index for naming the downloaded image files.
    """

    result = get_url(url)
    img_links = get_img_links(result)

    for idx, img_link in enumerate(img_links, start=start_index):
        img_link = img_link["src"]
        print("Downloading... ", img_link)
        if img_link:
            download_img(img_link, idx)
    print("Download Complete!!")
