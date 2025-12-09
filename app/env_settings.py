from environs import Env

# Инициализация
env = Env()
env.read_env()  # загружаем .env

# Чтение и преобразование
GREEN_API_URL = env("GREEN_API_URL")
GREEN_API_INSTANCE_ID = env.int("GREEN_API_INSTANCE_ID")
GREEN_API_TOKEN = env("GREEN_API_TOKEN")
MAX_CHAT_IDS = env.list("MAX_CHAT_IDS")
TELEGRAM_CHAT_IDS = env.list("TELEGRAM_CHAT_IDS")
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")

# Финальная проверка (выбросит исключение, если есть ошибки)
env.seal()
