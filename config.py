import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN")
CURRENCY = os.getenv('CURRENCY', 'USD')
SUBSCRIPTION_PRICE = int(os.getenv('SUBSCRIPTION_PRICE', 50000))

PREMIUM_CHANNEL_ID = os.getenv("PREMIUM_CHANNEL_ID")