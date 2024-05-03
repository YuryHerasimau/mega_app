import requests
from typing import List, Tuple
from datetime import datetime, timedelta
from config import NEWSAPI_KEY
import random


QUERY_LIST = ["QA инженер", "QA automation testing", "test automation", "тестировщик"]
random_query = random.choice(QUERY_LIST)


def get_news(query: str) -> List[Tuple[str, str]]:
    """
    Get news articles related to a specific query.

    Args:
    - query (str): The query term to search for news articles.

    Returns:
    - List[Tuple[str, str]]: A list of tuples containing the title and URL of news articles.
    """

    current_date = datetime.now().date()
    one_month_ago = current_date - timedelta(days=30)
    response = requests.get(
        f"https://newsapi.org/v2/everything?q={query}&from={one_month_ago}&sortBy=publishedAt&apiKey={NEWSAPI_KEY}"
    )
    data = response.json()
    news_data = []
    if data["status"] == "ok" and data["totalResults"] > 0:
        for article in data["articles"]:
            news_data.append((article["title"], article["url"]))
        return news_data
    else:
        return [("No news", "#")]


def show_news() -> List[Tuple[str, str]]:
    """
    Show news articles based on a random query.

    Returns:
    - List[Tuple[str, str]]: A list of tuples containing the title and URL of news articles.
    """

    news = get_news(random_query)
    return news
