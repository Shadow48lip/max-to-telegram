# Через бота @getidsbot — отправьте ему ссылку на группу или переforwardьте любое сообщение из неё.

from aiogram import Bot, Dispatcher
from aiogram.types import Message


TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_IDS=0


# Инициализируйте бот с токеном
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def send_to_group():
    text = "Привет из бота!"


    try:
        message = await bot.send_message(chat_id=TELEGRAM_CHAT_IDS, text=text)
        print(f"Сообщение отправлено, ID: {message.message_id}")
    except Exception as e:
        print(f"Ошибка: {e}")



# узнать id группы где есть бот
@dp.message()
async def catch_chat_id(message: Message):
    print(f"chat_id группы: {message.chat.id}")
    print(f"Название: {message.chat.title}")


# Запуск (например, в main)
import asyncio
asyncio.run(send_to_group())
# dp.run_polling(bot)