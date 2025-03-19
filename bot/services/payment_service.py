from telegram import LabeledPrice
from config import PAYMENT_PROVIDER_TOKEN, CURRENCY, SUBSCRIPTION_PRICE
from bot.utils.logger import logger

def create_payment(chat_id):
    if not PAYMENT_PROVIDER_TOKEN:
        logger.error("❌ PAYMENT_PROVIDER_TOKEN отсутствует в конфигурации!")
        raise ValueError("PAYMENT_PROVIDER_TOKEN отсутствует в конфигурации!")

    if not CURRENCY:
        logger.error("❌ Валюта не указана в конфигурации!")
        raise ValueError("Валюта не указана в конфигурации!")

    if not SUBSCRIPTION_PRICE or SUBSCRIPTION_PRICE <= 0:
        logger.error("❌ Неверная цена подписки!")
        raise ValueError("Неверная цена подписки!")

    try:
        title = "Подписка на эксклюзивный контент"
        description = "Получите доступ к эксклюзивным материалам на месяц."
        payload = f"subscription-{chat_id}"
        prices = [LabeledPrice("Подписка", SUBSCRIPTION_PRICE)]

        logger.info(f"✅ Создание инвойса для пользователя {chat_id} на сумму {SUBSCRIPTION_PRICE / 100:.2f} {CURRENCY}")

        return {
            "chat_id": chat_id,
            "title": title,
            "description": description,
            "payload": payload,
            "provider_token": PAYMENT_PROVIDER_TOKEN,
            "currency": CURRENCY,
            "prices": prices,
            "start_parameter": "subscribe-payment"
        }
    except Exception as e:
        logger.error(f"❌ Ошибка при создании платежа: {e}")
        raise