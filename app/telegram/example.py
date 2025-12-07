# Через бота @getidsbot — отправьте ему ссылку на группу или переforwardьте любое сообщение из неё.

from aiogram import Bot
from aiogram.types import Message


# Инициализируйте бот с токеном
bot = Bot(token="ВАШ_ТОКЕН_БОТА")


async def send_to_group():
    chat_id = -1001234567890  # ID группы (обязательно отрицательное для супергрупп)
    text = "Привет из бота!"


    try:
        message = await bot.send_message(chat_id=chat_id, text=text)
        print(f"Сообщение отправлено, ID: {message.message_id}")
    except Exception as e:
        print(f"Ошибка: {e}")


# Запуск (например, в main)
import asyncio
asyncio.run(send_to_group())