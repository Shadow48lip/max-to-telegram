import httpx
import logging

from env_settings import GREEN_API_URL, GREEN_API_TOKEN, GREEN_API_INSTANCE_ID

async def check_max_instance(client: httpx.AsyncClient) -> bool:
    """Проверяет активен ли иснтанс. Если нет, то нет смысла дальше обращаться."""
    # https://green-api.com/v3/docs/api/common-errors/
    url = url_builder("getStateInstance")
    try:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("stateInstance") and data["stateInstance"] == "authorized":
                logging.debug(f"Успех: {data}")
                return True
        else:
            logging.warning(f"HTTP {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        logging.error(f"Ошибка сети: {e}")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP-ошибка: {e}")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
    return False

async def get_max_messages(client: httpx.AsyncClient, chat_id: str = None):

    url = url_builder("receiveNotification")

    try:
        response = await client.get(url, timeout=10.0, params={"receiveTimeout": 5})
        if response.status_code == 200:
            data = response.json()
            if not data:
                logging.info("Нет сообщений. Ждем дальше...")
                return False
            
            logging.info(f"Успех: {data}")
            return True
        else:
            logging.warning(f"HTTP {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        logging.error(f"Ошибка сети: {e}")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP-ошибка: {e}")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
    return False

def url_builder(method: str):
    """ Строит url для запроса """
    # TODO подставить из переменных окружения
    url = f"{GREEN_API_URL}/v3/waInstance{GREEN_API_INSTANCE_ID}/{method}/{GREEN_API_TOKEN}"
    return url

