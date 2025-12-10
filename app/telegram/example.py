# Через бота @getidsbot — отправьте ему ссылку на группу или переforwardьте любое сообщение из неё.

from aiogram import Bot, Dispatcher
from aiogram.types import Message


TELEGRAM_BOT_TOKEN="8077578307:AAG-DH55dSONff0pZFexATpXo9cfscp1cmg"
TELEGRAM_CHAT_IDS=['-1003343697233/53', '-1003343697233']
TELEGRAM_TOPIC_ID=53


# Инициализируйте бот с токеном
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def send_to_group():
    text = "Привет из бота!"

    for chat_id in TELEGRAM_CHAT_IDS:
        topic_id = None

        if "/" in chat_id:
            chat_id, topic_id = chat_id.split("/")

        try:
            message = await bot.send_message(chat_id=chat_id, text=text, message_thread_id=topic_id)
            print(f"Сообщение отправлено, CHAT: {chat_id}, ID: {message.message_id}")
        except Exception as e:
            print(f"Ошибка: {e}")



# узнать id группы где есть бот
@dp.message()
async def catch_chat_id(message: Message):
    print(f"chat_id группы: {message.chat.id}")
    print(f"thread группы: {message.message_thread_id}")
    print(f"Название: {message.chat.title}")


# Запуск (например, в main)
import asyncio
# asyncio.run(send_to_group())
# asyncio.run(send_to_group())
dp.run_polling(bot)


