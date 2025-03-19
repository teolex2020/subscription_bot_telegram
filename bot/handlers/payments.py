from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message, LabeledPrice
from aiogram.exceptions import TelegramAPIError
from config import PAYMENT_PROVIDER_TOKEN, CURRENCY, BOT_TOKEN
from bot.utils.logger import logger

router = Router()

@router.message(F.text == "/subscribe")
async def send_invoice(message: Message):

    try:
        chat_id = message.chat.id
        logger.info(f"🔎 Перевірка chat_id: {chat_id}")

        prices = [LabeledPrice(label="Підписка", amount=50000)]
        await message.bot.send_invoice(
            chat_id=chat_id,
            title="Підписка на контент",
            description="Отримайте доступ до преміум-контенту на місяць.",
            payload="subscription",
            provider_token=PAYMENT_PROVIDER_TOKEN,
            currency="UAH",
            prices=prices,
            start_parameter="subscription-start"
        )
        logger.info(f"📩 Інвойс для користувача {message.from_user.id} відправлений!")
    except TelegramAPIError as e:
        logger.error(f"❌ Помилка при відправленні інвойсу: {e}")

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
        await pre_checkout_query.answer(ok=True)
    except TelegramAPIError as e:
        print(f"❌ Помилка при перевірці оплати: {e}")

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    try:
        await message.answer("✅ Підписка успішно оформлена!")
        logger.info(f"✅ Оплата від користувача {message.from_user.id} підтверджена!")
    except TelegramAPIError as e:
        logger.error(f"❌ Помилка при підтвердженні оплати: {e}")