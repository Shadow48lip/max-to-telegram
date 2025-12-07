import asyncio
import httpx
import logging

from green_api.services import check_max_instance, get_max_messages

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')


async def main():
    print("Hello from max-to-telegram!")

    # Создаём асинхронный клиент (переиспользуется для всех запросов)
    async with httpx.AsyncClient(timeout=6) as client:
        logging.info("Проверка инстанса при старте ...")
        if await check_max_instance(client):
            while True:
                logging.info("Отправляю запрос...")
                result = await get_max_messages(client, "-69308615655644")
                # logging.info(f"Ответ: {result}")

                
                # Пауза между запросами (секунда)
                await asyncio.sleep(5)
        else:
            logging.error("Старт прерван. Состояние Инстанса не нормальное.")


if __name__ == "__main__":
    asyncio.run(main())