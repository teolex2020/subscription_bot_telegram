from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.utils.logger import logger

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    logger.info(f"📥 Получена команда /start от {message.from_user.username}")
    await message.answer(
        "👋 Привіт! Я бот для продажу підписок на ексклюзивний контент.\n"
        "Щоб оформити підписку, введіть команду /subscribe."
    )


@router.message(Command("subscribe"))
async def subscribe_handler(message: Message):
    logger.info(f"⚙️ Отримана команда /subscribe від {message.from_user.username}")
    await message.answer("💳 Надсилаю інвойс для оформлення підписки...")