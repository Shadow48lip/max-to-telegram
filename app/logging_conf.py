import logging

from env_settings import LOG_LEVEL

# Настройка логирования
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s | %(message)s')
logger = logging.getLogger(__name__)

# Настройка логов для httpx
logging.getLogger("httpx").setLevel(LOG_LEVEL)
logging.getLogger("httpcore").setLevel(LOG_LEVEL)