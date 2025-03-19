from sqlalchemy import Column, Integer, String, Enum
from bot.database.db import Base
import enum

# Enum для статуса подписки
class SubscriptionStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'

class Subscription(Base):
    __tablename__ = 'subscriptions'  # 👈 Множественное число — правильный стиль

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)

    # Ограничения на длину строки + Enum для строгих значений
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.INACTIVE)

    def activate(self):
        self.status = SubscriptionStatus.ACTIVE

    def deactivate(self):
        self.status = SubscriptionStatus.INACTIVE

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, status={self.status.value})>"
