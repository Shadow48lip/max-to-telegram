from typing import Literal
from pydantic import BaseModel

class MaxSender(BaseModel):
    chatId: str
    chatName: str
    sender: str
    chatName: str
    senderName: str
    senderContactName: str

class MaxMessageData(BaseModel):
    # typeMessage: Literal['textMessage', 'extendedTextMessage', "imageMessage"]
    typeMessage: Literal["textMessage", "extendedTextMessage", "imageMessage"]
    textMessageData: dict = None
        # "textMessage": "Я использую GREEN-API для отправки этого сообщения!"
    extendedTextMessageData: dict = None
        # "text": "Я использую GREEN-API для отправки этого сообщения! Документация на сайте https://green-api.com/",
        # "description": "Сервис GREEN-API — интеграция с MAX на любом языке программирования: PHP, JavaScript, 1С, Python, Java, C#, VBA.",
        # "title": "Доступный MAX API для отправки сообщений | Сервис GREEN-API",
        # "forwardingScore": 0,
        # "isForwarded": false
    fileMessageData: dict = None
        # "downloadUrl": "https://sw-media-3100.storage.yandexcloud.net/3100000000/15697d2c-397c-4fd0-8e1a-8be95f753aae.webp",
        # "caption": "",
        # "fileName": "15697d2c-397c-4fd0-8e1a-8be95f753aae.webp",
        # "jpegThumbnail": "UklGRjoAAABXRUJQVlA4IC4AAACwAwCdASoyADIAPm0skkYkIqGhLggAgA2JaQAAZAEm0xUUDzF5wAD++yGAAAAA",
        # "isAnimated": false,
        # "mimeType": "image/webp",
        # "forwardingScore": 0,
        # "isForwarded": false


class MaxMessage(BaseModel):
    typeWebhook: str
    instanceData: dict
    timestamp: int
    idMessage: str
    senderData: MaxSender
    messageData: MaxMessageData

class NewMessage(BaseModel):
    """Очищенное сообщение, подготовленное к пересылке"""
    typeMessage: str
    senderName: str
    chatName: str
    file: dict | None = None
    message: str = None
    raw_data: dict
