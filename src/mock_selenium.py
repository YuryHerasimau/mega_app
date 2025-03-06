import json
import time
# from seleniumwire import undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options


VALID_STATUS_CODES = [200, 201, 204, 400, 401, 403, 404, 500, 502, 503]


def init_driver():
    """
    Инициализация драйвера с настройками.
    :return: Экземпляр selenium-wire драйвера.
    """
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    # driver = uc.Chrome(options=options) # version_main=133
    driver = webdriver.Chrome(options=options)
    return driver


def show_request_urls(driver, target_url):
    """
    Показывает URL всех запросов, сделанных на целевой странице.
    :param driver: Экземпляр selenium-wire драйвера.
    :param target_url: Целевой URL.
    :return: Список URL запросов.
    """
    driver.get(target_url)
    urls = [{'url': request.url} for request in driver.requests]
    return urls


def mock_requests(driver, mock_config):
    """
    Универсальная функция для мокирования запросов.
    :param driver: Экземпляр selenium-wire драйвера.
    :param mock_config: Словарь с конфигурацией для мокирования.
    """
    def interceptor(request):                
        # Проверяем, соответствует ли запрос конфигурации
        if "request_url" in mock_config and "method" in mock_config:
            if mock_config["request_url"] in request.url and request.method == mock_config["method"]:
                # Если действие — модификация URL
                if mock_config.get("action") == "modify_url":
                    if mock_config["modify_url"]["from"] in request.url:
                        request.url = request.url.replace(
                            mock_config["modify_url"]["from"],
                            mock_config["modify_url"]["to"]
                        )
                        print(f"URL modified: {request.url}")

                # Если действие — мок-ответ
                elif mock_config.get("action") == "mock_response":
                    status_code = mock_config["response"]["status_code"]
                    if status_code not in VALID_STATUS_CODES:
                        print(f"Invalid status code: {status_code}. Skipping request.")
                        return

                    else:
                        request.create_response(
                            status_code=status_code,
                            headers=mock_config["response"]["headers"],
                            body=json.dumps(mock_config["response"]["body"])
                        )
                        print(f"Mock response sent for: {request.url}")

    # Устанавливаем перехватчик
    driver.request_interceptor = interceptor


def mock_multiple_requests(driver, mock_configs):
    """
    Мокирование нескольких эндпоинтов.
    :param driver: Экземпляр selenium-wire драйвера.
    :param mock_configs: Список конфигураций для мокирования.
    """
    for config in mock_configs:
        mock_requests(driver, config)


def main():
    driver = init_driver()

    # Конфигурация для мокирования GET-запроса (подмена URL)
    mock_config_get = {
        "request_url": "https://logistics.bsl.dev/api/companies",
        "method": "GET",
        "action": "modify_url",
        "modify_url": {
            "from": "fe6e9cd6-3bee-4256-8854-387756db8195",
            "to": "null"
        }
    }

    # Конфигурация для мокирования POST-запроса (мок-ответ)
    mock_config_post = {
        "request_url": "https://logistics.bsl.dev/api/company",
        "method": "POST",
        "action": "mock_response",
        "response": {
            "status_code": 500,
            "headers": {"Content-Type": "application/json"},
            "body": {"status": "mocked response"}
        }
    }

    # Конфигурация для мокирования GET-запроса (мок-ответ)
    mock_config_get_2 = {
        "request_url": "https://logistics.bsl.dev/api/companies?page=1&per_page=10",
        "method": "GET",
        "action": "mock_response",
        "response": {
            "status_code": 403,
            "headers": {"Content-Type": "application/json"},
            "body": {"error": "Not Bad :)"}
        }
    }

    # Устанавливаем мокирование для GET и POST
    mock_requests(driver, mock_config_get)
    mock_requests(driver, mock_config_post)

    # Открываем страницу
    driver.get("https://logistics.bsl.dev")
    time.sleep(60)

    driver.close()

if __name__ == "__main__":
    main()
