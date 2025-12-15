
from aiogram import Bot

from env_settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS
from logging_conf import logger


# Инициализируйте бот с токеном
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_tg_text_message(msg):
    for chat_id in TELEGRAM_CHAT_IDS:
        topic_id = None
        if "/" in chat_id:
            chat_id, topic_id = chat_id.split("/")

        try:
            message = await bot.send_message(chat_id=chat_id, text=msg, message_thread_id=topic_id,parse_mode="HTML")
            logger.warning(f"Сообщение отправлено. CHAT: {chat_id}, ID: {message.message_id}")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения в Telegram: {e}")

async def send_tg_photo(url: str, description: str = ""):
    for chat_id in TELEGRAM_CHAT_IDS:
        topic_id = None
        if "/" in chat_id:
            chat_id, topic_id = chat_id.split("/")
        
        try:
            message = await bot.send_photo(chat_id=chat_id, photo=url, caption=description, message_thread_id=topic_id,parse_mode="HTML")
            logger.warning(f"Сообщение отправлено. CHAT: {chat_id}, ID: {message.message_id}")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения в Telegram: {e}")
