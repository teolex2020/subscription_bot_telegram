from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bot.utils.logger import logger

# Строка підключення до SQLite
DATABASE_URL = "sqlite+aiosqlite:///database.db"

# Створюємо асинхронний движок
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Дозволяє використовувати SQLite у кількох потоках
)

# Створюємо асинхронну сесію
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# Базовий клас для моделі
Base = declarative_base()

# Перевірка успішного підключення до бази даних
async def check_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")  # Перевірка підключення
        logger.info("✅ Успішне підключення до бази даних!")
    except Exception as e:
        logger.error(f"❌ Помилка підключення до бази даних: {e}")

# Асинхронна функція для отримання сесії
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            logger.info("📥 Відкриття нової сесії з базою даних")
            yield session
        except Exception as e:
            logger.error(f"❌ Помилка роботи з сесією: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.info("📤 Сесія з базою даних закрита")