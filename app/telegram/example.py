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


######
###### Пример как совмести обработку ответов боту ####
######



import asyncio
import httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Настройки
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
API_URL = "https://ваш-api.example.com/events"
CHECK_INTERVAL = 10  # секунд между проверками API

class BotApp:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.client = httpx.AsyncClient()
        
        # Хранилище для отслеживания сообщений бота (чтобы ловить ответы)
        # Для продакшена используйте БД (SQLite, Redis) вместо self.sent_messages, если нужно сохранять состояние между перезапусками.
        self.sent_messages = {}  # {message_id: контекст}

    async def check_external_api(self):
        """Бесконечный цикл: опрашивает API и отправляет уведомления."""
        while True:
            try:
                response = await self.client.get(API_URL)
                data = response.json()
                
                # Предположим, API возвращает список новых событий
                for event in data.get("events", []):
                    # Отправляем сообщение через бота
                    message = await self.bot.send_message(
                        chat_id=event["chat_id"],
                        text=f"Новое событие: {event['title']}"
                    )
                    
                    # Запоминаем ID сообщения, чтобы отслеживать ответы
                    self.sent_messages[message.message_id] = {
                        "event_id": event["id"],
                        "user_id": event["user_id"]
                    }
            
            except Exception as e:
                print(f"Ошибка API: {e}")
            
            await asyncio.sleep(CHECK_INTERVAL)

    async def setup_handlers(self):
        """Настраивает обработчики сообщений."""
        
        # Обработчик команд (например, /start)
        @self.dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            await message.answer("Бот запущен!")
        
        # Обработчик ответов на сообщения бота
        @self.dp.message()
        async def handle_reply(message: types.Message):
            # Проверяем, является ли это ответом на сообщение бота
            if message.reply_to_message and message.reply_to_message.from_user.id == self.bot.id:
                bot_msg_id = message.reply_to_message.message_id
                if bot_msg_id in self.sent_messages:
                    context = self.sent_messages[bot_msg_id]
                    print(
                        f"Получен ответ на событие {context['event_id']} "
                        f"от пользователя {message.from_user.id}: {message.text}"
                    )
                    
                    # Здесь можно выполнить действия:
                    # - обновить статус события в БД
                    # - отправить уведомление в другой чат
                    # - вызвать API
                    await self.handle_user_response(context, message)

    async def handle_user_response(self, context: dict, message: types.Message):
        """Обрабатывает ответ пользователя на сообщение бота."""
        print(f"Обработка ответа для события {context['event_id']}: {message.text}")
        # Ваш код здесь
        # Например:
        # await self.client.post("https://ваш-api.example.com/response", json={...})

    async def run(self):
        """Запускает оба процесса: мониторинг API и обработку сообщений."""
        # Настраиваем обработчики
        await self.setup_handlers()
        
        # Запускаем polling бота (будет работать параллельно)
        await self.dp.start_polling(self.bot)
        
        # Одновременно запускаем мониторинг API
        # (в отдельном task, чтобы не блокировало polling)
        api_task = asyncio.create_task(self.check_external_api())
        
        try:
            # Ждём завершения polling (обычно никогда)
            await self.dp.stop_polling()
        finally:
            api_task.cancel()

# Запуск приложения
if __name__ == "__main__":
    app = BotApp()
    asyncio.run(app.run())