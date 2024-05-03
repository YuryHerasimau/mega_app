import os
from dotenv import load_dotenv


load_dotenv()

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
API_NINJAS_KEY = os.getenv("API_NINJAS_KEY")
CITY = os.getenv("CITY")
