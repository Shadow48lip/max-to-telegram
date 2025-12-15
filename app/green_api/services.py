import httpx
from pydantic import ValidationError

from env_settings import GREEN_API_URL, GREEN_API_TOKEN, GREEN_API_INSTANCE_ID
from green_api.schemas import MaxMessage, NewMessage
from logging_conf import logger

async def check_max_instance(client: httpx.AsyncClient) -> bool:
    """Проверяет активен ли иснтанс. Если нет, то нет смысла дальше обращаться."""
    # https://green-api.com/v3/docs/api/common-errors/
    url = url_builder("getStateInstance")
    try:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("stateInstance") and data["stateInstance"] == "authorized":
                logger.debug(f"Успех: {data}")
                return True
        else:
            logger.warning(f"HTTP {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        logger.error(f"Ошибка сети: {e}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP-ошибка: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
    return False

async def get_max_messages(client: httpx.AsyncClient, after_delete = True) -> dict | None:
    """Читает сообщения из очереди. А после удаляет оттуда."""
    # {'receiptId': 1, 
    #  'body': {'typeWebhook': 'incomingMessageReceived', 
    #           'instanceData': {'idInstance': 3100400119, 'wid': '79103547767@c.us', 'typeInstance': 'v3'}, 
    #           'timestamp': 1765285691, 'idMessage': '115689763107266127', 
    #           'senderData': {'chatId': '-69308615655644', 'chatName': '6В ИНФОРМАЦИЯ', 'sender': '63270108', 'senderName': 'Анастасия', 'senderContactName': '', 'senderPhoneNumber': 0}, 
    #           'messageData': {'typeMessage': 'extendedTextMessage', 'extendedTextMessageData': {'text': 'В период с 1 октября до 14 декабря 2025 олимпиады для школьников 1-11 классов.  Зарегистрироваться на Олимпиаду 25.foxford.ru\nпроходит по следующим предметам: русский язык, математика.\n  Бесплатно.\n Олимпиада входит в Перечень олимпиад.\nОлимпиада разработана в соответствии с задачами национального проекта «Молодёжь и и направлена на обеспечение развития и успеха каждого ребенка, раскрытие талантов обучающихся.\nЗадания Олимпиады направлены на развитие функциональной грамотности. Участие в Олимпиаде дает\nвозможность попасть в государственный информационный ресурс о детях, проявивших выдающиеся\nспособности. Все участники также получают возможность участвовать в розыгрыше ценных призов от\n«Фоксфорда» и партнеров олимпиады.\nОлимпиада проводится в 2 тура:\n1. Отборочный этап проходит онлайн с 1 октября до 14 декабря 2025 год на платформе\n«Фоксфорда» для учеников 1–11 классов, он включает в себя нестандартные задачи в\nолимпиадном формате.', 'description': 'Участвуй в бесплатной Олимпиаде и выигрывай призы.', 'title': 'Узнай, на что ты способен!', 'previewType': 'None', 'jpegThumbnail': '', 'forwardingScore': 1, 'isForwarded': True}}}}
    # {'receiptId': 2, 
    #     'body': {'typeWebhook': 'incomingMessageReceived', 
    #              'instanceData': {'idInstance': 3100400119, 'wid': '79103547767@c.us', 'typeInstance': 'v3'}, 
    #              'timestamp': 1765285703, 'idMessage': '115689763837649904', 
    #             'senderData': {'chatId': '-69308615655644', 'chatName': '6В ИНФОРМАЦИЯ', 'sender': '63270108', 'senderName': 'Анастасия', 'senderContactName': '', 'senderPhoneNumber': 0}, 
    #             'messageData': {'typeMessage': 'textMessage', 'textMessageData': {'textMessage': 'Олимпиада от учителя русского языка.', 'forwardingScore': 0, 'isForwarded': False}}}}

    url = url_builder("receiveNotification")

    try:
        response = await client.get(url, timeout=10.0, params={"receiveTimeout": 5})
        if response.status_code == 200:
            data = response.json()
            if not data:
                logger.info("Нет сообщений. Ждем дальше...")
                return None
            
            logger.info(f"Успех: {data}")
            # Удаляем полученное уведомление
            if after_delete:
                if await delete_max_message(client, int(data.get("receiptId"))):
                    logger.info("Сообщение удалено из очереди")
            return data
        else:
            logger.warning(f"HTTP {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        logger.error(f"Ошибка сети: {e}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP-ошибка: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
    return None

async def delete_max_message(client: httpx.AsyncClient, message_id: int) -> bool:
    """Удаляет из очереди сообщение"""
    
    url = f"{url_builder("deleteNotification")}/{message_id}"

    try:
        response = await client.delete(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("result") and data["result"] is True:
                return True
            
            logger.error(f"Не удалось удалить: {data}")
            return False
        else:
            logger.warning(f"HTTP {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        logger.error(f"Ошибка сети: {e}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP-ошибка: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
    return False

def url_builder(method: str):
    """ Строит url для запроса """
    url = f"{GREEN_API_URL}/v3/waInstance{GREEN_API_INSTANCE_ID}/{method}/{GREEN_API_TOKEN}"
    return url


def process_max_message(data: dict, chat_ids: list) -> NewMessage | None:
    """
    Подготавливает сообщение для пересылки.
    Если тип поддерживается или из другого чата - вернет None
    """
    
    if "body" not in data:
        logger.error("Сообщение не содержит тела Body")
        return None

    body = data.get("body")
    try:
        max_msg = MaxMessage(**body)
        logger.info("Валидация модели прошла успешно")
    except ValidationError as e:
        logger.error("❌ Ошибки валидации:")
        for err in e.errors():
            print(f"  {err['loc']}: {err['msg']} ({err['type']})")
        return None
    
    if max_msg.senderData.chatId not in chat_ids:
        logger.warning("Пропускаем сообщение, оно не наше.")
        return None
    
    message = ""
    if max_msg.messageData.typeMessage == "textMessage":
        message = max_msg.messageData.textMessageData.get("textMessage")
    if max_msg.messageData.typeMessage == "extendedTextMessage":
        message = max_msg.messageData.extendedTextMessageData.get("text")
    
    file = None
    if max_msg.messageData.typeMessage == "imageMessage":
        file = max_msg.messageData.fileMessageData.get("downloadUrl")

    new_message = NewMessage(
        typeMessage = max_msg.messageData.typeMessage,
        senderName = max_msg.senderData.senderName,
        chatName = max_msg.senderData.chatName,
        file = file,
        message = message,
        raw_data = max_msg,
    )

    return new_message
