from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from bot.models.subscription import Subscription
from bot.utils.logger import logger

# Получаем подписку пользователя
async def get_subscription(db: AsyncSession, user_id: int):
    logger.info(f"🔎 Получаем подписку для пользователя {user_id}")
    try:
        result = await db.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        subscription = result.scalar()
        if subscription:
            logger.info(f"✅ Подписка для пользователя {user_id} найдена: {subscription}")
        else:
            logger.warning(f"⚠️ Подписка для пользователя {user_id} не найдена")
        return subscription
    except SQLAlchemyError as e:
        logger.error(f"❌ Ошибка при получении подписки для пользователя {user_id}: {e}")
        return None

# Создаём новую подписку
async def create_subscription(db: AsyncSession, user_id: int):
    logger.info(f"➕ Создаём подписку для пользователя {user_id}")
    try:
        subscription = Subscription(user_id=user_id)
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        logger.info(f"✅ Подписка для пользователя {user_id} успешно создана")
        return subscription
    except SQLAlchemyError as e:
        await db.rollback()  # Откатываем изменения в случае ошибки
        logger.error(f"❌ Ошибка при создании подписки для пользователя {user_id}: {e}")
        return None

# ✅ Активация подписки после успешной оплаты
async def activate_subscription(db: AsyncSession, user_id: int):
    logger.info(f"🚀 Активация подписки для пользователя {user_id}")
    try:
        subscription = await get_subscription(db, user_id)
        if subscription:
            subscription.status = "active"
            subscription.payment_status = "paid"
            await db.commit()
            await db.refresh(subscription)
            logger.info(f"✅ Подписка для пользователя {user_id} активирована")
            return subscription
        else:
            logger.warning(f"⚠️ Подписка для пользователя {user_id} не найдена")
            return None
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"❌ Ошибка при активации подписки для пользователя {user_id}: {e}")
        return None
