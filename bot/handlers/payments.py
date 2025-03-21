from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message, LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramAPIError
from config import PAYMENT_PROVIDER_TOKEN, CURRENCY, SUBSCRIPTION_PRICE
from bot.utils.logger import logger
from bot.services.subscription_service import activate_subscription
from bot.database.db import get_db

router = Router()

# Інлайн-клавіатура з кнопкою "Спробувати ще раз"
retry_button = InlineKeyboardButton(text="Спробувати ще раз", callback_data="subscribe")
restart_button = InlineKeyboardButton(text="Повернутися до початку", callback_data="restart")
retry_keyboard = InlineKeyboardMarkup(inline_keyboard=[[retry_button], [restart_button]])

async def send_invoice(message: Message):
    try:
        chat_id = message.chat.id
        logger.info(f"🔎 Перевірка chat_id: {chat_id}")

        prices = [LabeledPrice(label="Підписка", amount=SUBSCRIPTION_PRICE)]
        await message.bot.send_invoice(
            chat_id=chat_id,
            title="Підписка на контент",
            description="Отримай доступ до преміум-контенту на місяць.",
            payload="subscription",
            provider_token=PAYMENT_PROVIDER_TOKEN,
            currency=CURRENCY,
            prices=prices,
            start_parameter="subscription-start"
        )
        logger.info(f"📩 Інвойс для користувача {message.from_user.id} відправлений!")
    except TelegramAPIError as e:
        logger.error(f"❌ Помилка при відправленні інвойсу: {e}")
        await message.answer(
            "❌ Виникла помилка при відправленні інвойсу. Спробуйте ще раз.",
            reply_markup=retry_keyboard
        )

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
        await pre_checkout_query.answer(ok=True)
    except TelegramAPIError as e:
        logger.error(f"❌ Помилка при перевірці оплати: {e}")

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    try:
        user_id = message.from_user.id
        async for db in get_db():
            subscription = await activate_subscription(db, message.bot, user_id)
            if subscription and subscription.invite_link:
                channel_button = InlineKeyboardButton(text="Перейти до каналу", url=subscription.invite_link)
                channel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[channel_button], [restart_button]])
                await message.answer(
                    "✅ Підписка успішно оформлена! Дякуємо за покупку! 🎉\n"
                    "Натисни кнопку нижче, щоб перейти до преміум-каналу (дійсне 1 день):",
                    reply_markup=channel_keyboard
                )
                logger.info(f"✅ Оплата від користувача {user_id} підтверджена, підписка активована!")
            else:
                await message.answer(
                    "❌ Помилка при активації підписки або генерації запрошення. Зверніться до підтримки.",
                    reply_markup=retry_keyboard
                )
                logger.error(f"❌ Не вдалося активувати підписку для користувача {user_id}")
    except TelegramAPIError as e:
        logger.error(f"❌ Помилка при підтвердженні оплати: {e}")
        await message.answer(
            "❌ Виникла помилка при підтвердженні оплати. Зверніться до підтримки.",
            reply_markup=retry_keyboard
        )