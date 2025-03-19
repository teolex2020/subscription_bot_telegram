import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from bot.handlers.commands import router as commands_router
from bot.handlers.messages import router as messages_router
from bot.handlers.payments import router as payments_router
from bot.utils.logger import logger


async def main():
    logger.info("🚀 Запуск Telegram-бота...")

    # Ініціалізуємо бота
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    # Реєструємо обробники
    dp.include_router(commands_router)
    dp.include_router(messages_router)
    dp.include_router(payments_router)

    logger.info("✅ Бот готовий до роботи!")
    await dp.start_polling(bot)


def register_command_handlers(dp: Dispatcher):
    dp.include_router(commands_router)


def register_message_handlers(dp: Dispatcher):
    dp.include_router(messages_router)


def register_payment_handlers(dp: Dispatcher):
    dp.include_router(payments_router)


if __name__ == "__main__":
    try:
        asyncio.run(main())  # 👈 Правильний спосіб запуску asyncio
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Завершення роботи бота...")