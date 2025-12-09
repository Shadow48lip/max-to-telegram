import httpx
import logging
from pydantic import ValidationError

from env_settings import GREEN_API_URL, GREEN_API_TOKEN, GREEN_API_INSTANCE_ID
from green_api.schemas import MaxMessage, NewMessage

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

async def get_max_messages(client: httpx.AsyncClient) -> dict | None:
    # 	{
	# 	"type": "incoming",
	# 	"idMessage": "115687812637677830",
	# 	"timestamp": 1765255930,
	# 	"typeMessage": "textMessage",
	# 	"chatId": "-69308615655644",
	# 	"textMessage": "Доброе утро!\nРастёт количество заболевших в школе, пишите пожалуйста сразу, если ребёнок болеет",
	# 	"senderId": "63270108",
	# 	"senderName": "Анастасия",
	# 	"senderContactName": "",
	# 	"deletedMessageId": "",
	# 	"editedMessageId": "",
	# 	"isEdited": false,
	# 	"isDeleted": false
	#   }

    # Testing
    # return {
    #     "receiptId": 1234567,
    #     "body": {
    #         "typeWebhook": "incomingMessageReceived",
    #         "instanceData": {
    #             "idInstance": 310000001,
    #             "wid": "79991234567@c.us",
    #             "typeInstance": "v3"
    #         },
    #         "timestamp": 1588091580,
    #         "idMessage": "126543123451133331119",
    #         "senderData": {
    #             "chatId": "-69308615655644",
    #             "chatName": "Ходабрыш",
    #             "sender": "10000000",
    #             "senderName": "Ходабрыш Пробешёлов",
    #             "senderContactName": "Ходабрыш Пробешёлов",
    #             "senderPhoneNumber": 79876543210
    #         },
    #         "messageData": {
    #             "typeMessage": "textMessage",
    #             "textMessageData": {
    #                 "textMessage": "Привет от Green-API!"
    #             }
    #         }
    #     }
    # }
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
                logging.info("Нет сообщений. Ждем дальше...")
                return None
            
            logging.info(f"Успех: {data}")
            # Удаляем полученное уведомление
            # if await delete_max_message(client, int(data.get("receiptId"))):
            #     logging.info("Сообщение удалено из очереди")
            return data
        else:
            logging.warning(f"HTTP {response.status_code}: {response.text}")
    except httpx.RequestError as e:
        logging.error(f"Ошибка сети: {e}")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP-ошибка: {e}")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
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
            
            logging.error(f"Не удалось удалить: {data}")
            return False
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
    url = f"{GREEN_API_URL}/v3/waInstance{GREEN_API_INSTANCE_ID}/{method}/{GREEN_API_TOKEN}"
    return url


def process_max_message(data: dict, chat_ids: list) -> NewMessage:
    """Разбирает сообщение, удаляет из очереди, если все ОК"""
    if "body" not in data:
        logging.error("Сообщение не соедржит тела Body")
        return None

    body = data.get("body")
    try:
        max_message = MaxMessage(**body)
        logging.info("Валидация модели прошла успешно")
    except ValidationError as e:
        logging.error("❌ Ошибки валидации:")
        for err in e.errors():
            print(f"  {err['loc']}: {err['msg']} ({err['type']})")
        return None
    
    if max_message.senderData.chatId not in chat_ids:
        logging.info("Пропускаем сообщение, оно не наше.")
        return None
    
    if max_message.messageData.typeMessage == "textMessage":
        message = max_message.messageData.textMessageData.get("textMessage")
    if max_message.messageData.typeMessage == "extendedTextMessage":
        message = max_message.messageData.extendedTextMessageData.get("text")

    if not message:
        message = "..."


    new_message = NewMessage(
        typeMessage = max_message.messageData.typeMessage,
        senderName = max_message.senderData.senderName,
        chatName = max_message.senderData.chatName,
        file = max_message.messageData.fileMessageData,
        message = message
    )

    return new_message