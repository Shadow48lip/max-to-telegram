
from aiogram import Bot

from env_settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS
from logging_conf import logger


# Инициализируйте бот с токеном
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_tg_text_message(msg):

    for chat_id in TELEGRAM_CHAT_IDS:
        try:
            message = await bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
            logger.warning(f"Сообщение отправлено, ID: {message.message_id}")
        except Exception as e:
            logger.error(f"Ошибка: {e}")
