import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")
CURRENCY = os.getenv('CURRENCY', 'USD')
SUBSCRIPTION_PRICE = int(os.getenv('SUBSCRIPTION_PRICE', 50000))

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'tgbot_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', '12345')
DB_NAME = os.getenv('DB_NAME', 'telegram_bot')