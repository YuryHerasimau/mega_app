import requests
import psutil
from plyer import notification
from time import sleep
from datetime import datetime
from config import OPENWEATHER_API_KEY, CITY


def get_date():
    """
    Get the current date and format it.
    
    Returns:
    - str: The formatted date.
    """

    return f"{datetime.now().strftime('%a, %d %b')}"


def get_weather(city: str) -> str:
    """
    Get the current weather information for a specific city.

    Args:
    - city (str): The name of the city for which weather information is requested.

    Returns:
    - str: A formatted string containing the weather information for the specified city.
    """

    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric')
    data = response.json()
    description = data['weather'][0]['description']
    icon = get_weather_icon(description)
    temperature = data['main']['temp']
    formatted_weather = f"{city}: {icon} {temperature}°C"
    return formatted_weather


def get_weather_icon(description: str) -> str:
    """
    Get the weather icon based on the weather description.

    Args:
    - description (str): The description of the weather.

    Returns:
    - str: The corresponding weather icon based on the description.
    """

    if 'cloud' in description:
        return "☁️"
    elif 'sun' and 'cloud' in description:
        return "⛅"
    elif 'rain' in description:
        return "🌧️"
    elif 'snow' in description:
        return "🌨️"
    elif 'lightning' in description:
        return "🌩️"
    elif 'storm' in description:
        return "⛈️"
    else:
        return "☀️"


def get_currency_rates() -> str:
    """
    Get the currency exchange rates for USD to BYN and USD to RUB.

    Returns:
    - str: A formatted string containing the currency exchange rates.
    """

    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()
    usd_rate = data['rates']['BYN'] # Курс доллара к белорусскому рублю
    rub_rate = data['rates']['RUB'] # Курс доллара к российскому рублю
    formatted_rates = f"USD/BYN {usd_rate}, USD/RUB {rub_rate}"
    return formatted_rates


def get_crypto_rates() -> str:
    """
    Get the current rates for cryptocurrencies (Bitcoin, Ethereum, Litecoin) in USD.

    Returns:
    - str: A formatted string containing the rates for BTC, ETH, and LTC in USD.
    """

    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,litecoin&vs_currencies=usd')
        data = response.json()
        if response.status_code == 200:
            btc_rate = data['bitcoin']['usd']
            eth_rate = data['ethereum']['usd']
            ltc_rate = data['litecoin']['usd']
            return f"BTC: {btc_rate}, ETH: {eth_rate}, LTC: {ltc_rate}"
    except Exception as ex:
        print(f"Request Error: {ex}")
        return None


def check_memory_and_cpu_usage():
    """
    Monitor memory consumption and CPU load. If thresholds are exceeded, raise an alarm.

    Returns:
    - str: A message indicating the status of memory and CPU usage.
    """

    memory_threshold = 80
    cpu_threshold = 60
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=1)
    if memory_usage > memory_threshold or cpu_usage > cpu_threshold:
        return f"Alarm! Memory usage: {memory_usage}% > {memory_threshold}%. CPU usage: {cpu_usage}%"
    else:
        return f"OK. Memory usage: {memory_usage}% < {memory_threshold}%. CPU usage: {cpu_usage}% < {cpu_threshold}%"


def check_battery_usage():
    """
    Check the battery level and notify if it falls below a threshold.

    Returns:
    - str: A message indicating the status of the battery level.
    """

    battery_threshold = 20
    while True:
        battery = psutil.sensors_battery()
        life = battery.percent
        if life < battery_threshold:
            notification.notify(
                title = "Battery Low",
                message = "🐱‍👤 I hacked your PC!\nСonnect to power source IMMEDIATELY!",
                timeout = 10
            )
            return f"Alarm! Battery percentage: {life}%"
        else:
            return f"Battery percentage: {life}%"
        sleep(60)


def show_ticker() -> str:
    """
    Show the ticker with current date, weather, currency rates, crypto rates, memory and CPU usage, and battery status.

    Returns:
    - str: A formatted string containing the ticker information.
    """
    
    current_date = get_date()
    weather = get_weather(CITY)
    currency_rates = get_currency_rates()
    crypto_rates = get_crypto_rates()

    if crypto_rates is None:
        crypto_rates = ""

    memory_cpu_usage = check_memory_and_cpu_usage()
    battery_usage = check_battery_usage()
    return f"📅 {current_date} | 🌡️ {weather} | 💲 {currency_rates} | 💹 {crypto_rates} | 🐱‍💻 {memory_cpu_usage} | 🔋 {battery_usage}"