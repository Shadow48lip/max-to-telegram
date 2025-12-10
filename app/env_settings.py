from environs import Env
import logging

# Инициализация
env = Env()
env.read_env()  # загружаем .env

# Чтение и преобразование
# Автоматически преобразует строку в уровень logging
LOG_LEVEL = env.log_level("LOG_LEVEL", logging.INFO)

GREEN_API_URL = env("GREEN_API_URL")
GREEN_API_INSTANCE_ID = env.int("GREEN_API_INSTANCE_ID")
GREEN_API_TOKEN = env("GREEN_API_TOKEN")
MAX_CHAT_IDS = env.list("MAX_CHAT_IDS")
TELEGRAM_CHAT_IDS = env.list("TELEGRAM_CHAT_IDS")
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")

# Финальная проверка (выбросит исключение, если есть ошибки)
env.seal()
