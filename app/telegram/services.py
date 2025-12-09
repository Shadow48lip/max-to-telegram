import logging

from aiogram import Bot

from env_settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS


# Инициализируйте бот с токеном
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_tg_text_message(msg):

    for chat_id in TELEGRAM_CHAT_IDS:
        try:
            message = await bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
            logging.info(f"Сообщение отправлено, ID: {message.message_id}")
        except Exception as e:
            logging.error(f"Ошибка: {e}")
