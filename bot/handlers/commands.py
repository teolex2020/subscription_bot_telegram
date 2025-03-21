from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from bot.handlers.payments import send_invoice
from bot.services.subscription_service import get_subscription
from bot.database.db import get_db
from bot.utils.logger import logger

router = Router()

# Інлайн-клавіатура з кнопкою "Розпочати"
start_button = InlineKeyboardButton(text="Розпочати", callback_data="start_subscription")
start_keyboard = InlineKeyboardMarkup(inline_keyboard=[[start_button]])

# Інлайн-клавіатура з кнопкою "Підписатися"
subscribe_button = InlineKeyboardButton(text="Підписатися", callback_data="subscribe")
subscribe_keyboard = InlineKeyboardMarkup(inline_keyboard=[[subscribe_button]])

@router.message(Command("start"))
async def start_handler(message: Message):
    logger.info(f"📥 Отримана команда /start від {message.from_user.username}")
    await message.answer(
        "👋 Привіт! Я бот для продажу підписок на ексклюзивний контент.\n"
        "Натисни 'Розпочати', щоб дізнатися більше!",
        reply_markup=start_keyboard
    )

@router.message(Command("check_access"))
async def check_access_handler(message: Message):
    logger.info(f"📥 Отримана команда /check_access від {message.from_user.username}")
    user_id = message.from_user.id
    async for db in get_db():
        subscription = await get_subscription(db, user_id)
        if subscription and subscription.is_active() and subscription.invite_link:
            channel_button = InlineKeyboardButton(text="Перейти до каналу", url=subscription.invite_link)
            channel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[channel_button]])
            await message.answer(
                f"✅ У вас є активна підписка до {subscription.expiration_date.strftime('%Y-%m-%d %H:%M:%S')}!\n"
                "Натисни кнопку нижче, щоб перейти до преміум-каналу:",
                reply_markup=channel_keyboard
            )
        else:
            await message.answer(
                "❌ У вас немає активної підписки. Оформіть підписку, натиснувши /start."
            )

@router.callback_query(lambda c: c.data == "start_subscription")
async def show_benefits_handler(callback_query: types.CallbackQuery):
    logger.info(f"⚙️ Користувач {callback_query.from_user.username} натиснув кнопку 'Розпочати'")
    await callback_query.message.answer(
        "✨ Після оформлення підписки ти отримаєш:\n"
        "- Доступ до ексклюзивного контенту\n"
        "- Щотижневі оновлення\n"
        "- Персональні рекомендації\n\n"
        "Готовий? Натисни 'Підписатися'!",
        reply_markup=subscribe_keyboard
    )
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "subscribe")
async def subscribe_handler(callback_query: types.CallbackQuery):
    logger.info(f"⚙️ Користувач {callback_query.from_user.username} натиснув кнопку 'Підписатися'")
    user_id = callback_query.from_user.id
    async for db in get_db():
        subscription = await get_subscription(db, user_id)
        if subscription and subscription.is_active():
            channel_button = InlineKeyboardButton(text="Перейти до каналу", url=subscription.invite_link)
            channel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[channel_button]])
            await callback_query.message.answer(
                f"✅ У вас уже є активна підписка до {subscription.expiration_date.strftime('%Y-%m-%d %H:%M:%S')}!\n"
                "Натисни кнопку нижче, щоб перейти до преміум-каналу:",
                reply_markup=channel_keyboard
            )
            await callback_query.answer()
            return
    await send_invoice(callback_query.message)
    await callback_query.answer()

@router.callback_query(lambda c: c.data == "restart")
async def restart_handler(callback_query: types.CallbackQuery):
    logger.info(f"⚙️ Користувач {callback_query.from_user.username} натиснув кнопку 'Повернутися до початку'")
    await callback_query.message.answer(
        "👋 Привіт! Я бот для продажу підписок на ексклюзивний контент.\n"
        "Натисни 'Розпочати', щоб дізнатися більше!",
        reply_markup=start_keyboard
    )
    await callback_query.answer()