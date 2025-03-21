import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from bot.handlers.commands import router as commands_router
from bot.handlers.payments import router as payments_router
from bot.database.db import engine, Base, get_db
from bot.services.subscription_service import remove_expired_users
from bot.utils.logger import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # Правильний імпорт
from apscheduler.triggers.cron import CronTrigger

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Таблиці бази даних створено або оновлено")

async def schedule_tasks(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=remove_expired_users,
        trigger=CronTrigger(hour=0, minute=0),
        args=[bot, get_db],
    )
    scheduler.start()
    logger.info("Планувальник задач запущено")
    return scheduler  # Повертаємо scheduler для можливості зупинки

async def main():
    logger.info("Запуск Telegram-бота...")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Вебхук видалено, переходимо до polling")

    dp.include_router(commands_router)
    dp.include_router(payments_router)

    await init_db()
    scheduler = await schedule_tasks(bot)  # Зберігаємо scheduler
    logger.info("Бот готовий до роботи!")
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()  # Зупиняємо scheduler при завершенні
        logger.info("Планувальник зупинено")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Завершення роботи бота...")