from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from bot.utils.logger import logger

# Строка подключения к базе данных с использованием asyncmy
DATABASE_URL = f"mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаём асинхронный движок с конфигурацией пула соединений
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,          # Максимум 10 соединений в пуле
    max_overflow=5,        # Разрешить до 5 дополнительных соединений
    pool_pre_ping=True,    # Проверка соединений перед использованием
)

# Создаём асинхронную сессию
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# Базовый класс для модели
Base = declarative_base()

# Проверка успешного подключения к базе данных
async def check_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")  # Проверка подключения
        logger.info("✅ Успешное подключение к базе данных!")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к базе данных: {e}")

# Асинхронная функция для получения сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            logger.info("📥 Открытие новой сессии с базой данных")
            yield session
        except Exception as e:
            logger.error(f"❌ Ошибка работы с сессией: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.info("📤 Сессия с базой данных закрыта")