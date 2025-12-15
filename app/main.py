import asyncio
import httpx

from green_api.services import check_max_instance, get_max_messages, process_max_message
from telegram.services import send_tg_photo, send_tg_text_message
from env_settings import MAX_CHAT_IDS
from logging_conf import logger


async def main():
    pause_time = 5

    # Создаём асинхронный клиент (переиспользуется для всех запросов)
    async with httpx.AsyncClient(timeout=6) as client:
        if await check_max_instance(client):
            logger.warning("Проверка инстанса при старте прошла успешно!")
            while True:
                logger.info("Отправляю запрос...")
                result = await get_max_messages(client, after_delete=True)
                if not result:
                    await asyncio.sleep(pause_time)
                    continue
                
                logger.warning("Получено новое сообщение!")
                logger.debug(result)
                # Очищает нужно нам сообщение
                msg = process_max_message(result, MAX_CHAT_IDS)
                if not msg:
                    await asyncio.sleep(1)
                    continue

                if msg.typeMessage == "textMessage" or msg.typeMessage == "extendedTextMessage":
                    logger.warning("Пересылаем текстовое сообщение")
                    formatted_msg = f"👀<b>{msg.senderName}</b> [{msg.chatName}]:\n\n{msg.message}"
                    await send_tg_text_message(formatted_msg)
                elif msg.typeMessage == "imageMessage":
                    logger.warning("Пересылаем картинку.")
                    formatted_msg = f"👀<b>{msg.senderName}</b> [{msg.chatName}]:\n\n{msg.message}"
                    await send_tg_photo(msg.file, formatted_msg)
                else:
                    logger.warning("Неизвестный тип сообщения!")
                    logger.warning(msg.raw_data)
                
                # TODO техническая пауза. Убрать потом!
                await asyncio.sleep(1)
        else:
            logger.error("Старт прерван. Состояние Инстанса не нормальное.")


if __name__ == "__main__":
    # иначе httpx рассыпается по ctrl+c
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Скрипт прерван пользователем.")
    except Exception as e:
        logger.critical(f"Невосстановимая ошибка: {e}")
