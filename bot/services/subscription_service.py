from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from bot.models.subscription import Subscription
from bot.utils.logger import logger
from aiogram import Bot
from config import PREMIUM_CHANNEL_ID
from datetime import datetime, timedelta

# Отримуємо підписку користувача
async def get_subscription(db: AsyncSession, user_id: int):
    logger.info(f"🔎 Отримуємо підписку для користувача {user_id}")
    try:
        result = await db.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        subscription = result.scalar()
        if subscription:
            if subscription.is_active():
                logger.info(f"✅ Підписка для користувача {user_id} активна: {subscription}")
            else:
                logger.info(f"⚠️ Підписка для користувача {user_id} неактивна або прострочена: {subscription}")
        else:
            logger.warning(f"⚠️ Підписка для користувача {user_id} не знайдена")
        return subscription
    except SQLAlchemyError as e:
        logger.error(f"❌ Помилка при отриманні підписки для користувача {user_id}: {e}")
        return None

# Створюємо нову підписку
async def create_subscription(db: AsyncSession, user_id: int):
    logger.info(f"➕ Створюємо підписку для користувача {user_id}")
    try:
        subscription = Subscription(user_id=user_id)
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        logger.info(f"✅ Підписка для користувача {user_id} успішно створена")
        return subscription
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"❌ Помилка при створенні підписки для користувача {user_id}: {e}")
        return None

# Генеруємо запрошення до каналу
async def generate_invite_link(bot: Bot, user_id: int) -> str:
    try:
        invite = await bot.create_chat_invite_link(
            chat_id=PREMIUM_CHANNEL_ID,
            expire_date=int((datetime.utcnow() + timedelta(days=1)).timestamp()),
            member_limit=1
        )
        logger.info(f"🔗 Запрошення для користувача {user_id} згенеровано: {invite.invite_link}")
        return invite.invite_link
    except Exception as e:
        logger.error(f"❌ Помилка при генерації запрошення для користувача {user_id}: {e}")
        return None

# Активація підписки після успішної оплати
async def activate_subscription(db: AsyncSession, bot: Bot, user_id: int):
    logger.info(f"🚀 Активація підписки для користувача {user_id}")
    try:
        subscription = await get_subscription(db, user_id)
        if not subscription:
            subscription = await create_subscription(db, user_id)
            if not subscription:
                return None
        subscription.activate()
        invite_link = await generate_invite_link(bot, user_id)
        if invite_link:
            subscription.invite_link = invite_link
        else:
            logger.error(f"❌ Не вдалося згенерувати запрошення для користувача {user_id}")
            return None
        await db.commit()
        await db.refresh(subscription)
        logger.info(f"✅ Підписка для користувача {user_id} активована до {subscription.expiration_date}")
        return subscription
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"❌ Помилка при активації підписки для користувача {user_id}: {e}")
        return None

# Видаляємо користувачів із каналу після закінчення підписки
async def remove_expired_users(bot: Bot, get_db_func):
    logger.info("🔍 Перевірка прострочених підписок...")
    async for db in get_db_func():  # Отримуємо сесію під час виконання
        try:
            result = await db.execute(select(Subscription))
            subscriptions = result.scalars().all()
            for subscription in subscriptions:
                if subscription.expiration_date and subscription.expiration_date < datetime.utcnow():
                    try:
                        await bot.ban_chat_member(chat_id=PREMIUM_CHANNEL_ID, user_id=subscription.user_id)
                        subscription.deactivate()
                        await db.commit()
                        logger.info(f"🚫 Користувач {subscription.user_id} видалений з каналу через закінчення підписки")
                    except Exception as e:
                        logger.error(f"❌ Помилка при видаленні користувача {subscription.user_id}: {e}")
        except SQLAlchemyError as e:
            logger.error(f"❌ Помилка при перевірці прострочених підписок: {e}")