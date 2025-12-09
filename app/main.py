import asyncio
import httpx
import logging

from green_api.services import check_max_instance, get_max_messages, process_max_message
from telegram.services import send_tg_text_message
from env_settings import MAX_CHAT_IDS

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')


async def main():
    pause_time = 5

    # Создаём асинхронный клиент (переиспользуется для всех запросов)
    async with httpx.AsyncClient(timeout=6) as client:
        logging.info("Проверка инстанса при старте ...")
        if await check_max_instance(client):
            while True:
                logging.info("Отправляю запрос...")
                result = await get_max_messages(client)
                if not result:
                    await asyncio.sleep(pause_time)
                    continue

                
                logging.info("Получено сообщение!")
                # logging.info(result)
                # logging.info(f"Ответ: {result}")
                msg = process_max_message(result, MAX_CHAT_IDS)
                if not msg:
                    await asyncio.sleep(1)
                    continue

                if msg.typeMessage == "imageMessage":
                    logging.info("Пересылаем картинку")
                    logging.info(msg)
                else:
                    logging.info("Пересылаем текстовое сообщение")
                    formatted_msg = f"👀<b>{msg.senderName}</b> [{msg.chatName}]:\n\n{msg.message}"
                    await send_tg_text_message(formatted_msg)
                

                
                # TODO техническая пауза. Убрать потом!
                await asyncio.sleep(1)
        else:
            logging.error("Старт прерван. Состояние Инстанса не нормальное.")


if __name__ == "__main__":
    asyncio.run(main())